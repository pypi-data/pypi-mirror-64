# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2012 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

# pylint: enable=E1101

from decimal import Decimal
import collections

from kiwi.currency import currency
from storm.references import Reference, ReferenceSet
from storm.expr import And, Join, Eq
from zope.interface import implementer

from stoqlib.database.properties import (UnicodeCol, DateTimeCol,
                                         PriceCol, QuantityCol, IdentifierCol,
                                         IdCol, EnumCol)
from stoqlib.domain.base import Domain, IdentifiableDomain
from stoqlib.domain.events import StockOperationConfirmedEvent
from stoqlib.domain.fiscal import Invoice, FiscalBookEntry
from stoqlib.domain.interfaces import IInvoiceItem, IInvoice
from stoqlib.domain.payment.method import PaymentMethod
from stoqlib.domain.payment.payment import Payment
from stoqlib.domain.person import LoginUser, Branch
from stoqlib.domain.product import StockTransactionHistory
from stoqlib.domain.taxes import check_tax_info_presence
from stoqlib.lib.dateutils import localnow
from stoqlib.lib.defaults import quantize
from stoqlib.lib.parameters import sysparam
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext


@implementer(IInvoiceItem)
class ReturnedSaleItem(Domain):
    """An item of a :class:`returned sale <ReturnedSale>`

    Note that objects of this type should never be created manually, only by
    calling :meth:`Sale.create_sale_return_adapter`
    """

    __storm_table__ = 'returned_sale_item'

    #: the returned quantity
    quantity = QuantityCol(default=0)

    #: The price which this :obj:`.sale_item` was sold.
    #: When creating this object, if *price* is not passed to the
    #: contructor, it defaults to :obj:`.sale_item.price` or
    #: :obj:`.sellable.price`
    price = PriceCol()

    sale_item_id = IdCol(default=None)

    #: the returned |saleitem|
    sale_item = Reference(sale_item_id, 'SaleItem.id')

    sellable_id = IdCol()

    #: The returned |sellable|
    #: Note that if :obj:`.sale_item` != ``None``, this is the same as
    #: :obj:`.sale_item.sellable`
    sellable = Reference(sellable_id, 'Sellable.id')

    batch_id = IdCol()

    #: If the sellable is a storable, the |batch| that it was removed from
    batch = Reference(batch_id, 'StorableBatch.id')

    returned_sale_id = IdCol()

    #: the |returnedsale| which this item belongs
    returned_sale = Reference(returned_sale_id, 'ReturnedSale.id')

    #: Id of ICMS tax in product tax template
    icms_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemIcms` tax for *self*
    icms_info = Reference(icms_info_id, 'InvoiceItemIcms.id')

    #: Id of IPI tax in product tax template
    ipi_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemIpi` tax fo *self*
    ipi_info = Reference(ipi_info_id, 'InvoiceItemIpi.id')

    #: Id of PIS tax in product tax template
    pis_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemPis` tax fo *self*
    pis_info = Reference(pis_info_id, 'InvoiceItemPis.id')

    #: Id of COFINS tax in product tax template
    cofins_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemCofins` tax fo *self*
    cofins_info = Reference(cofins_info_id, 'InvoiceItemCofins.id')

    item_discount = Decimal('0')

    parent_item_id = IdCol()
    parent_item = Reference(parent_item_id, 'ReturnedSaleItem.id')

    children_items = ReferenceSet('id', 'ReturnedSaleItem.parent_item_id',
                                  order_by='ReturnedSaleItem.te_id')

    def __init__(self, store, returned_sale: 'ReturnedSale', **kwargs):
        # TODO: Add batch logic here. (get if from sale_item or check if was
        # passed togheter with sellable)
        sale_item = kwargs.get('sale_item')
        sellable = kwargs.get('sellable')

        if not sale_item and not sellable:
            raise ValueError(
                "A sale_item or a sellable is mandatory to create this object")
        elif sale_item and sellable and sale_item.sellable != sellable:
            raise ValueError(
                "sellable must be the same as sale_item.sellable")
        elif sale_item and not sellable:
            sellable = sale_item.sellable
            kwargs['sellable'] = sellable

        if not 'price' in kwargs:
            # sale_item.price takes priority over sellable.price
            kwargs['price'] = sale_item.price if sale_item else sellable.price

        check_tax_info_presence(kwargs, store)

        super(ReturnedSaleItem, self).__init__(store=store, **kwargs)
        self.returned_sale = returned_sale

        product = self.sellable.product
        if product:
            self.ipi_info.set_item_tax(self)
            self.icms_info.set_item_tax(self)
            self.pis_info.set_item_tax(self)
            self.cofins_info.set_item_tax(self)

    @property
    def total(self):
        """The total being returned

        This is the same as :obj:`.price` * :obj:`.quantity`
        """
        return quantize(self.price * self.quantity)

    #
    # IInvoiceItem implementation
    #

    @property
    def base_price(self):
        return self.price

    @property
    def parent(self):
        return self.returned_sale

    @property
    def cfop_code(self):
        return u'1202'

    #
    #  Public API
    #

    def get_total(self):
        return self.total

    def return_(self, user: LoginUser):
        """Do the real return of this item

        When calling this, the real return will happen, that is,
        if :obj:`.sellable` is a |product|, it's stock will be
        increased on *branch*.
        """
        storable = self.sellable.product_storable
        if storable:
            storable.increase_stock(self.quantity, self.returned_sale.branch,
                                    StockTransactionHistory.TYPE_RETURNED_SALE,
                                    self.id, user, batch=self.batch)
        if self.sale_item:
            self.sale_item.quantity_decreased -= self.quantity

    def undo(self, user: LoginUser):
        """Undo this item return.

        This is the oposite of the return, ie, the item will be removed back
        from stock and the sale item decreased quantity will be restored.
        """
        storable = self.sellable.product_storable
        if storable:
            storable.decrease_stock(self.quantity, self.returned_sale.branch,
                                    StockTransactionHistory.TYPE_UNDO_RETURNED_SALE,
                                    self.id, user, batch=self.batch)
        if self.sale_item:
            self.sale_item.quantity_decreased += self.quantity

    def maybe_remove(self):
        """Will eventualy remove the object from database"""
        for child in self.children_items:
            # Make sure to remove children before remove itself
            if child.can_remove():
                self.store.remove(child)
        if self.can_remove():
            self.store.remove(self)

    def can_remove(self):
        """Check if the ReturnedSaleItem can be removed from database

        If the item is a package, check if all of its children are being
        returned
        """
        product = self.sellable.product
        if product and product.is_package and not bool(self.quantity):
            return not any(bool(child.quantity) for child in self.children_items)
        return not bool(self.quantity)

    def get_component_quantity(self, parent):
        for component in parent.sellable.product.get_components():
            if self.sellable.product == component.component:
                return component.quantity


@implementer(IInvoice)
class ReturnedSale(IdentifiableDomain):
    """Holds information about a returned |sale|.

    This can be:
      * *trade*, a |client| is returning the |sale| and buying something
        new with that credit. In that case the returning sale is :obj:`.sale` and the
        replacement |sale| is in :obj:`.new_sale`.
      * *return sale* or *devolution*, a |client| is returning the |sale|
        without making a new |sale|.

    Normally the old sale which is returned is :obj:`.sale`, however it
    might be ``None`` in some situations for example, if the |sale| was done
    at a different |branch| that hasn't been synchronized or is using another
    system.
    """

    __storm_table__ = 'returned_sale'

    #: This returned sale was received on another branch, but is not yet
    #: confirmed. A product goes back to stock only after confirmation
    STATUS_PENDING = u'pending'

    #: This return was confirmed, meaning the product stock was increased.
    STATUS_CONFIRMED = u'confirmed'

    #: This returned sale was canceled, ie, The product stock is decreased back
    #: and the original sale still have the products.
    STATUS_CANCELLED = 'cancelled'

    statuses = collections.OrderedDict([
        (STATUS_PENDING, _(u'Pending')),
        (STATUS_CONFIRMED, _(u'Confirmed')),
        (STATUS_CANCELLED, _(u'Cancelled')),
    ])

    #: A numeric identifier for this object. This value should be used instead of
    #: :obj:`Domain.id` when displaying a numerical representation of this object to
    #: the user, in dialogs, lists, reports and such.
    identifier = IdentifierCol()

    #: Status of the returned sale
    status = EnumCol(default=STATUS_PENDING)

    #: the date this return was done
    return_date = DateTimeCol(default_factory=localnow)

    #: the date that the |returned sale| with the status pending was received
    confirm_date = DateTimeCol(default=None)

    # When this returned sale was undone
    undo_date = DateTimeCol(default=None)

    #: the reason why this return was made
    reason = UnicodeCol(default=u'')

    #: The reason this returned sale was undone
    undo_reason = UnicodeCol(default=u'')

    sale_id = IdCol(default=None)

    #: the |sale| we're returning
    sale = Reference(sale_id, 'Sale.id')

    new_sale_id = IdCol(default=None)

    #: if not ``None``, :obj:`.sale` was traded for this |sale|
    new_sale = Reference(new_sale_id, 'Sale.id')

    responsible_id = IdCol()

    #: the |loginuser| responsible for doing this return
    responsible = Reference(responsible_id, 'LoginUser.id')

    confirm_responsible_id = IdCol()

    #: the |loginuser| responsible for receiving the pending return
    confirm_responsible = Reference(confirm_responsible_id, 'LoginUser.id')

    undo_responsible_id = IdCol()
    #: the |loginuser| responsible for undoing this returned sale.
    undo_responsible = Reference(undo_responsible_id, 'LoginUser.id')

    branch_id = IdCol()

    #: the |branch| in which this return happened
    branch = Reference(branch_id, 'Branch.id')

    station_id = IdCol(allow_none=False)
    #: The station this object was created at
    station = Reference(station_id, 'BranchStation.id')

    #: a list of all items returned in this return
    returned_items = ReferenceSet('id', 'ReturnedSaleItem.returned_sale_id',
                                  order_by='ReturnedSaleItem.te_id')

    #: |payments| generated by this returned sale
    payments = None

    #: |transporter| used in returned sale
    transporter = None

    invoice_id = IdCol()

    #: The |invoice| generated by the returned sale
    invoice = Reference(invoice_id, 'Invoice.id')

    def __init__(self, store, branch: Branch, **kwargs):
        kwargs['invoice'] = Invoice(store=store, invoice_type=Invoice.TYPE_IN, branch=branch)
        super(ReturnedSale, self).__init__(store=store, branch=branch, **kwargs)

    @property
    def group(self):
        """|paymentgroup| for this return sale.

        Can return:
          * For a *trade*, use the |paymentgroup| from
            the replacement |sale|.
          * For a *devolution*, use the |paymentgroup| from
            the returned |sale|.
        """
        if self.new_sale:
            return self.new_sale.group
        if self.sale:
            return self.sale.group
        return None

    @property
    def client(self):
        """The |client| of this return

        Note that this is the same as :obj:`.sale.client`
        """
        return self.sale and self.sale.client

    @property
    def sale_total(self):
        """The current total amount of the |sale|.

        This is calculated by getting the
        :attr:`total amount <stoqlib.domain.sale.Sale.total_amount>` of the
        returned sale and subtracting the sum of :obj:`.returned_total` of
        all existing returns for the same sale.
        """
        if not self.sale:
            return currency(0)

        query = And(ReturnedSale.sale_id == self.sale.id,
                    ReturnedSale.status == ReturnedSale.STATUS_CONFIRMED)
        returned = self.store.find(ReturnedSale, query)
        # This will sum the total already returned for this sale,
        # excluiding *self* within the same store
        returned_total = sum([returned_sale.returned_total for returned_sale in
                              returned if returned_sale != self])

        return currency(self.sale.total_amount - returned_total)

    @property
    def paid_total(self):
        """The total paid for this sale

        Note that this is the same as
        :meth:`stoqlib.domain.sale.Sale.get_total_paid`
        """
        if not self.sale:
            return currency(0)

        return self.sale.get_total_paid()

    @property
    def returned_total(self):
        """The total being returned on this return

        This is done by summing the :attr:`ReturnedSaleItem.total` of
        all of this :obj:`returned items <.returned_items>`
        """
        return currency(sum([item.total for item in self.returned_items]))

    @property
    def total_amount(self):
        """The total amount for this return

        See :meth:`.return_` for details of how this is used.
        """
        return currency(self.sale_total -
                        self.paid_total -
                        self.returned_total)

    @property
    def total_amount_abs(self):
        """The absolute total amount for this return

        This is the same as abs(:attr:`.total_amount`). Useful for
        displaying it on a gui, just changing it's label to show if
        it's 'overpaid' or 'missing'.
        """
        return currency(abs(self.total_amount))

    #
    #  IContainer implementation
    #

    def get_items(self):
        return self.returned_items

    def remove_item(self, item):
        item.returned_sale = None
        self.store.maybe_remove(item)

    #
    # IInvoice implementation
    #

    @property
    def comments(self):
        return self.reason

    @property
    def discount_value(self):
        return currency(0)

    @property
    def invoice_subtotal(self):
        return self.returned_total

    @property
    def invoice_total(self):
        return self.returned_total

    @property
    def recipient(self):
        if self.sale and self.sale.client:
            return self.sale.client.person
        elif self.new_sale and self.new_sale.client:
            return self.new_sale.client.person
        return None

    @property
    def operation_nature(self):
        # TODO: Save the operation nature in new returned_sale table field.
        return _(u"Sale Return")

    #
    #  Public API
    #

    @classmethod
    def get_pending_returned_sales(cls, store, branch):
        """Returns a list of pending |returned_sale|

        :param store: a store
        :param branch: the |branch| where the sale was made
        """
        from stoqlib.domain.sale import Sale

        tables = [cls, Join(Sale, cls.sale_id == Sale.id)]
        # We want the returned_sale which sale was made on the branch
        # So we are comparing Sale.branch with |branch| to build the query
        return store.using(*tables).find(cls, And(cls.status == cls.STATUS_PENDING,
                                                  Sale.branch == branch))

    def is_pending(self):
        return self.status == ReturnedSale.STATUS_PENDING

    def is_undone(self):
        return self.status == ReturnedSale.STATUS_CANCELLED

    def can_undo(self):
        return self.status == ReturnedSale.STATUS_CONFIRMED

    def return_(self, user: LoginUser, method_name=u'money'):
        """Do the return of this returned sale.

        :param unicode method_name: The name of the payment method that will be
          used to create this payment.

        If :attr:`.total_amount` is:
          * > 0, the client is returning more than it paid, we will create
            a |payment| with that value so the |client| can be reversed.
          * == 0, the |client| is returning the same amount that needs to be paid,
            so existing payments will be cancelled and the |client| doesn't
            owe anything to us.
          * < 0, than the payments need to be readjusted before calling this.

        .. seealso: :meth:`stoqlib.domain.sale.Sale.return_` as that will be
           called after that payment logic is done.
        """
        assert self.sale and self.sale.can_return()
        self._clean_not_used_items()
        self._create_return_payment(method_name, self.returned_total)

        # FIXME: For now, we are not reverting the comission as there is a
        # lot of things to consider. See bug 5215 for information about it.
        self._revert_fiscal_entry()

        self.sale.return_(self)

        # Save operation_nature and branch in Invoice table.
        self.invoice.operation_nature = self.operation_nature
        self.invoice.branch = self.branch

        if self.sale.branch == self.branch:
            self.confirm(user)

    def trade(self, responsible: LoginUser):
        """Do a trade for this return

        Almost the same as :meth:`.return_`, but unlike it, this won't
        generate reversed payments to the client. Instead, it'll
        generate an inpayment using :obj:`.returned_total` value,
        so it can be used as an "already paid quantity" on :obj:`.new_sale`.
        """
        assert self.new_sale
        if self.sale:
            assert self.sale.can_return()
        self._clean_not_used_items()

        store = self.store
        group = self.group
        method = PaymentMethod.get_by_name(store, u'trade')
        description = _(u'Traded items for sale %s') % (
            self.new_sale.identifier, )
        value = self.returned_total

        value_as_discount = sysparam.get_bool('USE_TRADE_AS_DISCOUNT')
        if value_as_discount:
            self.new_sale.discount_value = self.returned_total
        else:
            payment = method.create_payment(self.branch, self.station, Payment.TYPE_IN, group,
                                            value, description=description)
            payment.set_pending()
            payment.pay()
            self._revert_fiscal_entry()

        if self.sale:
            self.sale.return_(self)
            if self.sale.branch == self.branch:
                self.confirm(responsible)
        else:
            # When trade items without a registered sale, confirm the
            # new returned sale.
            self.confirm(responsible)

    def remove(self):
        """Remove this return and it's items from the database"""
        # XXX: Why do we remove this object from the database
        # We must remove children_items before we remove its parent_item
        for item in self.returned_items.find(Eq(ReturnedSaleItem.parent_item_id, None)):
            [self.remove_item(child) for child in getattr(item, 'children_items')]
            self.remove_item(item)
        self.store.remove(self)

    def confirm(self, responsible: LoginUser):
        """Receive the returned_sale_items from a pending |returned_sale|

        :param responsible: the |login_user| that received the pending returned sale
        """
        assert self.status == self.STATUS_PENDING
        old_status = self.status
        self._return_items(responsible)
        self.status = self.STATUS_CONFIRMED
        self.confirm_responsible = responsible
        self.confirm_date = localnow()
        StockOperationConfirmedEvent.emit(self, old_status)

    def undo(self, user: LoginUser, reason):
        """Undo this returned sale.

        This includes removing the returned items from stock again (updating the
        quantity decreased on the sale).

        :param reason: The reason for this operation.
        """
        assert self.can_undo()
        for item in self.get_items():
            item.undo(user)

        payment = self._get_cancel_candidate_payment(pending_only=True)
        if payment:
            # If there are pending out payments which match the returned value
            # and those payments are all of the same method, we can just cancel any of
            # these payments right away.
            payment.cancel()
        else:
            # We now need to create a new in payment for the total amount of this
            # returned sale.
            payment = self._get_cancel_candidate_payment()
            method = payment.method if payment else PaymentMethod.get_by_name(self.store, 'money')
            description = _(u'%s return undone for sale %s') % (
                method.description, self.sale.identifier)
            payment = method.create_payment(self.branch, self.station, Payment.TYPE_IN,
                                            payment_group=self.group,
                                            value=self.returned_total,
                                            description=description,
                                            ignore_max_installments=True)
            payment.set_pending()
            payment.pay()

        self.status = self.STATUS_CANCELLED
        self.cancel_date = localnow()
        self.undo_reason = reason

        # if the sale status is returned, we must reset it to confirmed (only
        # confirmed sales can be returned)
        if self.sale.is_returned():
            self.sale.set_not_returned(self.responsible)

    #
    #  Private
    #

    def _create_return_payment(self, method_name, value):
        method = PaymentMethod.get_by_name(self.store, method_name)
        description = _(u'%s returned for sale %s') % (method.description,
                                                       self.sale.identifier)
        payment = method.create_payment(self.branch, self.station, Payment.TYPE_OUT,
                                        payment_group=self.group,
                                        value=value,
                                        description=description)
        payment.set_pending()
        if method_name == u'credit':
            payment.pay()

    def _get_cancel_candidate_payment(self, pending_only=False):
        """Try to find a payment to cancel for a canceled operation

        If the user cancels or undoes an operation - e.g. undoing a returned sale -
        we can either cancel the pending payment, or create a reversal payment for its
        value.

        :param pending_only: If True, this will consider only pending payments.
        """
        queries = [Payment.payment_type == Payment.TYPE_OUT,
                   Payment.value == self.returned_total]
        if pending_only:
            queries.append(Payment.status == Payment.STATUS_PENDING)

        # We search for the payments which are correspondent to our operation aiming to
        # finding which payment methods are involved.
        payments = list(self.sale.payments.find(And(*queries)))
        methods = set(payment.method.method_name for payment in payments)

        # If and only if there is only one method from all the payments found, then any of the
        # payments can be cancelled or reversed.
        if len(methods) == 1:
            return payments[0]

        return

    def _return_items(self, user: LoginUser):
        # We must have at least one item to return
        assert self.returned_items.count()

        for item in self.returned_items:
            item.return_(user)

    def _get_returned_percentage(self):
        return Decimal(self.returned_total / self.sale.total_amount)

    def _clean_not_used_items(self):
        query = Eq(ReturnedSaleItem.parent_item_id, None)
        for item in self.returned_items.find(query):
            item.maybe_remove()

    def _revert_fiscal_entry(self):
        entry = self.store.find(FiscalBookEntry,
                                payment_group=self.group,
                                is_reversal=False).one()
        if not entry:
            return

        # FIXME: Instead of doing a partial reversion of fiscal entries,
        # we should be reverting the exact tax for each returned item.
        returned_percentage = self._get_returned_percentage()
        entry.reverse_entry(
            self.invoice.invoice_number,
            icms_value=entry.icms_value * returned_percentage,
            iss_value=entry.iss_value * returned_percentage,
            ipi_value=entry.ipi_value * returned_percentage)
