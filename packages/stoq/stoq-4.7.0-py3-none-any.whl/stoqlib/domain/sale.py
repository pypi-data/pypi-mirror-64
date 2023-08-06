# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

#
# Copyright (C) 2005-2014 Async Open Source <http://www.async.com.br>
# All rights reserved
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., or visit: http://www.gnu.org/.
#
# Author(s): Stoq Team <stoq-devel@async.com.br>
#
"""
Domain objects related to the sale process in Stoq.

Sale object and related objects implementation """

# pylint: enable=E1101

import collections
from decimal import Decimal

from kiwi.currency import currency
from kiwi.python import Settable
from stoqdrivers.enum import TaxType
from storm.expr import (And, Avg, Count, LeftJoin, Join, Max, In,
                        Or, Sum, Alias, Select, Cast, Eq, Coalesce, Ne)
from storm.info import ClassAlias
from storm.references import Reference, ReferenceSet
from zope.interface import implementer

from stoqlib.database.expr import (Concat, Date, Distinct, Field, NullIf,
                                   Round, TransactionTimestamp)
from stoqlib.database.properties import (UnicodeCol, DateTimeCol, IntCol,
                                         PriceCol, QuantityCol, IdentifierCol,
                                         IdCol, BoolCol, EnumCol, TimeCol)
from stoqlib.database.viewable import Viewable
from stoqlib.domain.address import Address, CityLocation
from stoqlib.domain.base import Domain, IdentifiableDomain
from stoqlib.domain.costcenter import CostCenter
from stoqlib.domain.event import Event
from stoqlib.domain.events import (SaleStatusChangedEvent,
                                   SaleCanCancelEvent,
                                   SaleIsExternalEvent,
                                   SaleItemBeforeDecreaseStockEvent,
                                   SaleItemBeforeIncreaseStockEvent,
                                   SaleItemAfterSetBatchesEvent,
                                   DeliveryStatusChangedEvent,
                                   StockOperationConfirmedEvent,
                                   ECFGetPrinterUserNumberEvent)
from stoqlib.domain.fiscal import FiscalBookEntry, Invoice
from stoqlib.domain.interfaces import IContainer, IInvoice, IInvoiceItem
from stoqlib.domain.payment.payment import Payment
from stoqlib.domain.payment.method import PaymentMethod
from stoqlib.domain.person import (Person, Client, Branch, LoginUser,
                                   SalesPerson, Company, Individual,
                                   ClientCategory)
from stoqlib.domain.product import (Product, ProductHistory, Storable,
                                    StockTransactionHistory, StorableBatch)
from stoqlib.domain.returnedsale import ReturnedSale, ReturnedSaleItem
from stoqlib.domain.sellable import Sellable, SellableCategory
from stoqlib.domain.service import Service
from stoqlib.domain.station import BranchStation
from stoqlib.domain.taxes import check_tax_info_presence, InvoiceItemIpi
from stoqlib.exceptions import SellError, StockError, DatabaseInconsistency
from stoqlib.lib.dateutils import localnow
from stoqlib.lib.defaults import quantize, DECIMAL_PRECISION
from stoqlib.lib.formatters import format_quantity
from stoqlib.lib.parameters import sysparam
from stoqlib.lib.translation import stoqlib_gettext


_ = stoqlib_gettext

# pyflakes: Reference requires that CostCenter is imported at least once
CostCenter  # pylint: disable=W0104

#
# Base Domain Classes
#


@implementer(IInvoiceItem)
class SaleItem(Domain):
    """An item of a |sellable| within a |sale|.

    Different from |sellable| which contains information about
    the base price, tax, etc, this contains the price in which
    *self* was sold, it's taxes, the quantity, etc.

    Note that objects of this type should never be created manually, only by
    calling :meth:`Sale.add_sellable`

    See also:
    `schema <http://doc.stoq.com.br/schema/tables/sale_item.html>`__
    """

    __storm_table__ = 'sale_item'

    repr_fields = ['sale_id']

    #: the quantity of the of sold item in this sale
    quantity = QuantityCol()

    #: the quantity already decreased from stock.
    quantity_decreased = QuantityCol(default=0)

    #: original value the |sellable| had when adding the sale item
    base_price = PriceCol()

    #: averiage cost of the items in this item
    average_cost = PriceCol(default=0)

    #: price of this item
    price = PriceCol()

    sale_id = IdCol()

    #: |sale| for this item
    sale = Reference(sale_id, 'Sale.id')

    sellable_id = IdCol()

    #: |sellable| for this item
    sellable = Reference(sellable_id, 'Sellable.id')

    batch_id = IdCol()

    #: If the sellable is a storable, the |batch| that it was removed from
    batch = Reference(batch_id, 'StorableBatch.id')

    delivery_id = IdCol(default=None)

    #: The |delivery| this sale_item *is in* or None
    delivery = Reference(delivery_id, 'Delivery.id')

    cfop_id = IdCol(default=None)

    #: :class:`fiscal entry <stoqlib.domain.fiscal.CfopData>`
    cfop = Reference(cfop_id, 'CfopData.id')

    #: user defined notes, currently only used by services
    notes = UnicodeCol(default=None)

    #: estimated date that *self* will be fixed, currently
    #: only used by services
    estimated_fix_date = DateTimeCol(default_factory=localnow)

    # FIXME: This doesn't appear to be used anywhere. Maybe we
    #        should remove it from the database
    completion_date = DateTimeCol(default=None)

    #: Id of ICMS tax in product tax template
    icms_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemIcms` tax for *self*
    icms_info = Reference(icms_info_id, 'InvoiceItemIcms.id')

    #: Id of IPI tax in product tax template
    ipi_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemIpi` tax for *self*
    ipi_info = Reference(ipi_info_id, 'InvoiceItemIpi.id')

    #: Id of PIS tax in product tax template
    pis_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemPis` tax for *self*
    pis_info = Reference(pis_info_id, 'InvoiceItemPis.id')

    #: Id of COFINS tax in product tax template
    cofins_info_id = IdCol()

    #: the :class:`stoqlib.domain.taxes.InvoiceItemCofins` tax for *self*
    cofins_info = Reference(cofins_info_id, 'InvoiceItemCofins.id')

    #: Id of |sale_item| parent of self
    parent_item_id = IdCol(default=None)

    parent_item = Reference(parent_item_id, 'SaleItem.id')

    # : A list of children of self
    children_items = ReferenceSet('id', 'SaleItem.parent_item_id')

    def __init__(self, store, sale: 'Sale', sellable: 'sellable', **kw):
        if not 'kw' in kw:
            base_price = sellable.price
            kw['base_price'] = base_price
            if not kw.get('cfop'):
                kw['cfop'] = sellable.default_sale_cfop
            if not kw.get('cfop'):
                kw['cfop'] = sysparam.get_object(store, 'DEFAULT_SALES_CFOP')

            store = kw.get('store', store)
            check_tax_info_presence(kw, store)
        Domain.__init__(self, store=store, sale=sale, sellable=sellable, **kw)

        product = self.sellable.product
        if product:
            # Set ipi details before icms, since icms may depend on the ipi
            self.ipi_info.set_item_tax(self)
            self.icms_info.set_item_tax(self)
        self.pis_info.set_item_tax(self)
        self.cofins_info.set_item_tax(self)

    #
    #  Properties
    #

    @property
    def returned_quantity(self):
        tables = [ReturnedSale,
                  Join(ReturnedSaleItem, ReturnedSale.id == ReturnedSaleItem.returned_sale_id)]
        query = And(ReturnedSaleItem.sale_item == self,
                    Or(ReturnedSale.status == ReturnedSale.STATUS_CONFIRMED,
                       ReturnedSale.status == ReturnedSale.STATUS_PENDING))
        return self.store.using(*tables).find(
            ReturnedSaleItem, query).sum(ReturnedSaleItem.quantity) or Decimal('0')

    @property
    def sale_discount(self):
        """The discount percentage (relative to the original price
           when the item was sold)

        :returns: the discount amount
        """
        if self.price > 0 and self.price < self.base_price:
            return (1 - (self.price / self.base_price)) * 100
        return 0

    @property
    def price_with_discount(self):
        """Applies the sale discount to this item.

        This will apply the discount given in the sale proportionally to this
        item.

        This value should be used when returning or trading this item, since the
        user should not receive more than what he paid for.

        Please note that this may result in rounding problems, since precision
        may be lost when appling the discount in the items.

        :returns: price with discount/surcharge
        """
        diff = self.sale.discount_value - self.sale.surcharge_value
        if diff == 0:
            return currency(self.price)

        # Dont use self.sale.(surcharge/discount)_percentage here since they are
        # already quantized, and we may lose even more precision.
        percentage = diff / self.sale.get_sale_subtotal()
        return currency(self.price * (1 - percentage))

    #
    # Invoice implementation
    #

    @property
    def item_discount(self):
        product = self.sellable.product
        if product and product.is_package:
            price = sum([quantize(child.price * child.quantity)
                         for child in self.children_items])
            discount = max(0, self.base_price * self.quantity - price)
        else:
            discount = self.base_price - self.price

        return Decimal(discount)

    @property
    def parent(self):
        return self.sale

    @property
    def cfop_code(self):
        """Returns the cfop code to be used on the NF-e

        If the sale was also printed on a ECF, then the cfop should be:
          * 5.929: if sold to a |Client| in the same state or

        :returns: the cfop code
        """
        if self.sale.coupon_id:
            return u'5929'

        if self.cfop:
            return self.cfop.code.replace(u'.', u'')

        # FIXME: remove sale cfop?
        return self.sale.cfop.code.replace(u'.', u'')

    @property
    def delivery_adaptor(self):
        """Get the delivery whose service item is self, if exists"""
        delivery_item = self.sale.get_delivery_item()
        if delivery_item:
            return Delivery.get_by_service_item(self.store, self)

        return None

    #
    #  Public API
    #

    def sell(self, user: LoginUser):
        if not self.sellable.is_available(branch=self.sale.branch):
            raise SellError(_(u"%s is not available for sale. Try making it "
                              u"available first and then try again.") % (
                self.sellable.get_description()))

        # This is emitted here instead of inside the if bellow because one can
        # connect on it and change this item in a way that, if it wasn't going
        # to decrease stock before, it will after
        SaleItemBeforeDecreaseStockEvent.emit(self)

        quantity_to_decrease = self.quantity - self.quantity_decreased
        storable = self.sellable.product_storable
        if storable and quantity_to_decrease:
            try:
                item = storable.decrease_stock(
                    quantity_to_decrease, self.sale.branch,
                    StockTransactionHistory.TYPE_SELL, self.id, user,
                    cost_center=self.sale.cost_center, batch=self.batch)
            except StockError as err:
                raise SellError(str(err))

            self.average_cost = item.stock_cost
        self.quantity_decreased += quantity_to_decrease
        self.update_tax_values()

    def cancel(self, user: LoginUser):
        # This is emitted here instead of inside the if bellow because one can
        # connect on it and change this item in a way that, if it wasn't going
        # to increase stock before, it will after
        SaleItemBeforeIncreaseStockEvent.emit(self)

        storable = self.sellable.product_storable
        if storable and self.quantity_decreased:
            storable.increase_stock(self.quantity_decreased,
                                    self.sale.branch,
                                    StockTransactionHistory.TYPE_CANCELED_SALE,
                                    self.id, user,
                                    batch=self.batch)
        self.quantity_decreased = Decimal(0)

    def reserve(self, user: LoginUser, quantity):
        """Reserve some quantity of this this item from stock

        This will remove the informed quantity from the stock.
        """
        assert 0 < quantity <= (self.quantity - self.quantity_decreased)
        storable = self.sellable.product_storable
        if storable:
            storable.decrease_stock(quantity, self.sale.branch,
                                    StockTransactionHistory.TYPE_SALE_RESERVED,
                                    self.id, user, batch=self.batch)
        self.quantity_decreased += quantity

    def return_to_stock(self, quantity, user: LoginUser):
        """Return some reserved quantity to stock

        This will return a previously reserved quantity to stock, so that it can
        be sold in any other sale.
        """
        assert 0 < quantity <= self.quantity_decreased
        storable = self.sellable.product_storable
        if storable:
            storable.increase_stock(quantity, self.sale.branch,
                                    StockTransactionHistory.TYPE_SALE_RETURN_TO_STOCK,
                                    self.id, user, batch=self.batch)
        self.quantity_decreased -= quantity

    def set_batches(self, batches):
        """Set batches for this sale item

        Set how much quantity of each |batch| this sale item represents.
        Note that this will replicate this item and create others, since
        the batch reference is one per sale item.

        At the end, this sale item will contain the quantity not used
        by any batch yet or, if the sum of quantities on batches are
        equal to :obj:`.quantity`, it will be used for one of the batches

        :param batches: a dict mapping the batch to it's quantity
        :returns: a list of the new created items
        :raises: :exc:`ValueError` if this item already has a batch
        :raises: :exc:`ValueError` if the sum of the batches quantities
            is greater than this item's original quantity
        """
        # Make a copy since we are going to modify this dict
        batches = batches.copy()

        if self.batch is not None:
            raise ValueError("This item already has a batch")

        quantities_sum = sum(quantity for quantity in batches.values())
        if quantities_sum > self.quantity:
            raise ValueError("The sum of batch quantities needs to be equal "
                             "or less than the item's original quantity")

        missing = self.quantity - quantities_sum
        # If there's some quantity missing batch information, leave self
        # with that missing quantity so it can be set again in the future
        if missing:
            self.quantity = missing
        else:
            self.batch, self.quantity = batches.popitem()
            self.update_tax_values()

        new_sale_items = []
        for batch, quantity in batches.items():
            new_item = self.__class__(
                store=self.store,
                sellable=self.sellable,
                sale=self.sale,
                quantity=quantity,
                batch=batch,
                cfop=self.cfop,
                base_price=self.base_price,
                price=self.price,
                notes=self.notes)
            new_item.update_tax_values()
            new_sale_items.append(new_item)

        SaleItemAfterSetBatchesEvent.emit(self, new_sale_items)
        return new_sale_items

    def set_discount(self, discount):
        """Apply *discount* on this item

        Note that the discount will be applied based on :obj:`.base_price`
        and then substitute :obj:`.price`, making any previous
        discount/surcharge being lost

        :param decimal.Decimal discount: the discount to be applied
            as a percentage, e.g. 10.0, 22.5
        """
        if self.parent_item:
            component = self.get_component(self.parent_item)
            discount_value = quantize(component.price * discount / 100)
            base_price = component.price
        else:
            discount_value = quantize(self.base_price * discount / 100)
            base_price = self.base_price

        self.price = max(base_price - discount_value, Decimal('0.01'))

    def get_total(self):
        # Sale items are suposed to have only 2 digits, but the value price
        # * quantity may have more than 2, so we need to round it.
        if self.ipi_info:
            return currency(quantize(self.price * self.quantity +
                                     self.ipi_info.v_ipi))
        return currency(quantize(self.price * self.quantity))

    def get_quantity_unit_string(self):
        return u"%s %s" % (format_quantity(self.quantity),
                           self.sellable.unit_description)

    def get_description(self):
        return self.sellable.get_description()

    def is_totally_returned(self):
        """If this sale item was totally returned

        :returns: ``True`` if it was totally returned,
            ``False`` otherwise.
        """
        return self.quantity == self.returned_quantity

    def is_service(self):
        """If this sale item contains a |service|.

        :returns: ``True`` if it's a service
        """
        service = self.store.find(Service, sellable=self.sellable).one()
        return service is not None

    def get_sale_surcharge(self):
        """The surcharge percentage (relative to the original price
           when the item was sold)

        :returns: the surcharge amount
        """
        if self.price > self.base_price:
            return ((self.price / self.base_price) - 1) * 100
        return 0

    def update_tax_values(self):
        if self.icms_info:
            self.icms_info.update_values(self)
        if self.ipi_info:
            self.ipi_info.update_values(self)
        if self.pis_info:
            self.pis_info.update_values(self)
        if self.cofins_info:
            self.cofins_info.update_values(self)

    def has_children(self):
        return self.children_items.count() > 0

    def get_component(self, parent):
        """Get the quantity of a component.

        :param parent: the |sale_item| parent_item of self
        :returns: the |product_component|
        """
        for component in parent.sellable.product.get_components():
            if self.sellable.product == component.component:
                return component
        return None


@implementer(IContainer)
class Delivery(Domain):
    """Delivery, transporting a set of sale items for sale.

    Involves a |transporter| transporting a set of |saleitems| to a
    receival |address|.

    Optionally a :obj:`.tracking_code` can be set to track the items.

    See also:
    `schema <http://doc.stoq.com.br/schema/tables/delivery.html>`__
    """

    __storm_table__ = 'delivery'

    #: The delivery was created and is waiting to be picked
    STATUS_INITIAL = u'initial'

    #: The delivery was cancelled
    STATUS_CANCELLED = u'cancelled'

    #: The delivery was picked and is waiting to be packed
    STATUS_PICKED = u'picked'

    #: The delivery was packed and is waiting to be packed
    STATUS_PACKED = u'packed'

    #: sent to deliver
    STATUS_SENT = u'sent'

    #: received by the |client|
    STATUS_RECEIVED = u'received'

    #: CIF (Cost, Insurance and Freight): The freight is responsibility of
    #: the receiver (i.e. the client)
    FREIGHT_TYPE_CIF = u'cif'

    #: CIF (Free on Board): The freight is responsibility of the sender
    #: (i.e. the branch)
    FREIGHT_TYPE_FOB = u'fob'

    #: 3rd party: The freight is responsibility of a third party
    FREIGHT_TYPE_3RDPARTY = u'3rdparty'

    #: No freight: There's no freight
    FREIGHT_TYPE_NONE = None

    statuses = collections.OrderedDict([
        (STATUS_INITIAL, _(u"Waiting")),
        (STATUS_CANCELLED, _(u"Cancelled")),
        (STATUS_PICKED, _(u"Picked")),
        (STATUS_PACKED, _(u"Packed")),
        (STATUS_SENT, _(u"Sent")),
        (STATUS_RECEIVED, _(u"Received")),
    ])

    freights = collections.OrderedDict([
        (FREIGHT_TYPE_NONE, _(u"No freight")),
        (FREIGHT_TYPE_CIF, _(u"CIF")),
        (FREIGHT_TYPE_FOB, _(u"FOB")),
        (FREIGHT_TYPE_3RDPARTY, _(u"Third party")),
    ])

    #: the delivery status
    status = EnumCol(allow_none=False, default=STATUS_INITIAL)

    #: the date which the delivery was created
    open_date = DateTimeCol(default_factory=TransactionTimestamp)

    #: The date that the delivery was cancelled
    cancel_date = DateTimeCol(default=None)

    #: The date that the delivery was picked
    pick_date = DateTimeCol(default=None)

    #: The date that the delivery was packed
    pack_date = DateTimeCol(default=None)

    #: the date which the delivery sent to deliver
    send_date = DateTimeCol(default=None)

    #: the date which the delivery received by the |client|
    receive_date = DateTimeCol(default=None)

    #: the delivery tracking code, a transporter specific identifier that
    #: can be used to look up the status of the delivery
    tracking_code = UnicodeCol(default=u'')

    #: The type of the freight
    freight_type = EnumCol(default=FREIGHT_TYPE_CIF)

    #: The kind of the volumes
    volumes_kind = UnicodeCol(default=u'')

    #: The quantity of volumes in this freight
    volumes_quantity = IntCol()

    #: The gross weight of the volumes in this freight
    volumes_gross_weight = QuantityCol()

    #: The net weight of the volumes in this freight
    volumes_net_weight = QuantityCol()

    #: The transporter vehicle license plate
    vehicle_license_plate = UnicodeCol()

    #: The transporter vehicle registration state
    vehicle_state = UnicodeCol()

    #: The transporter vehicle RNTC (Registro Nacional de Transportador de Carga)
    vehicle_registration = UnicodeCol()

    address_id = IdCol(default=None)

    #: the |address| to deliver to
    address = Reference(address_id, 'Address.id')

    transporter_id = IdCol(default=None)

    #: the |transporter| for this delivery
    transporter = Reference(transporter_id, 'Transporter.id')

    cancel_responsible_id = IdCol(default=None)
    #: The responsible for cancelling the products for delivery
    cancel_responsible = Reference(cancel_responsible_id, 'LoginUser.id')

    pick_responsible_id = IdCol(default=None)
    #: The responsible for picking the products for delivery
    pick_responsible = Reference(pick_responsible_id, 'LoginUser.id')

    pack_responsible_id = IdCol(default=None)
    #: The responsible for packing the products for delivery
    pack_responsible = Reference(pack_responsible_id, 'LoginUser.id')

    send_responsible_id = IdCol(default=None)
    #: The responsible for delivering the products to the |transporter|
    send_responsible = Reference(send_responsible_id, 'LoginUser.id')

    invoice_id = IdCol(default=None)
    #: The operation's invoice this delivery is for
    invoice = Reference(invoice_id, 'Invoice.id')

    #
    #  Properties
    #

    @property
    def status_str(self):
        return self.statuses[self.status]

    @property
    def address_str(self):
        if self.address:
            return self.address.get_address_string()
        return u''

    @property
    def recipient_str(self):
        return self.address.person.get_description()

    @property
    def service_item(self):
        delivery = sysparam.get_object(self.store, 'DELIVERY_SERVICE').sellable
        operation = self.invoice.operation
        for item in operation.get_items():
            if item.sellable == delivery:
                return item

    @property
    def delivery_items(self):
        return self.invoice.operation.get_items().find(delivery_id=self.id)

    #
    # Classmethods
    #

    @classmethod
    def get_by_service_item(cls, store, item):
        return store.find(cls, invoice_id=item.parent.invoice_id).one()

    #
    #  Public API
    #

    def can_cancel(self):
        """Check if we can cancel the delivery.

        Only initial, picked or packed deliveries can be cancelled.
        """
        return self.status in [self.STATUS_INITIAL,
                               self.STATUS_PICKED,
                               self.STATUS_PACKED]

    def can_pick(self):
        """Check if we can pick the delivery.

        Only initial deliveries can be picked.
        """
        return self.status == self.STATUS_INITIAL

    def can_pack(self):
        """Check if we can pack the delivery.

        Only picked deliveries can be packed.
        """
        return self.status == self.STATUS_PICKED

    def can_send(self):
        """Check if we can send the delivery.

        Only packed deliveries can be sent.
        """
        # FIXME: In the future once pick & pack is implemented, should we only
        # allow packed deliveries to be sent?
        return self.status in [self.STATUS_INITIAL,
                               self.STATUS_PICKED,
                               self.STATUS_PACKED]

    def can_receive(self):
        """Check if we can receive the delivery.

        Only sent deliveries can be received.
        """
        return self.status == self.STATUS_SENT

    def set_initial(self):
        """Set the delivery in its initial state."""
        # FIXME: This should be removed in the future once we implement
        # the pick & pack structure
        self._set_delivery_status(self.STATUS_INITIAL)

    def cancel(self, responsible):
        """Set the delivery as cancelled."""
        assert self.can_cancel()
        self.cancel_date = TransactionTimestamp()
        self._set_delivery_status(self.STATUS_CANCELLED)
        self.cancel_responsible = responsible

    def pick(self, responsible):
        """Set the delivery as picked."""
        assert self.can_pick()
        self._set_delivery_status(self.STATUS_PICKED)
        self.pick_date = TransactionTimestamp()
        self.pick_responsible = responsible

    def pack(self, responsible):
        """Set the delivery as packed."""
        assert self.can_pack()
        self._set_delivery_status(self.STATUS_PACKED)
        self.pack_date = TransactionTimestamp()
        self.pack_responsible = responsible

    def send(self, responsible):
        """Set the delivery as sent."""
        assert self.can_send()
        self._set_delivery_status(self.STATUS_SENT)
        self.send_date = TransactionTimestamp()
        self.send_responsible = responsible

    def receive(self):
        """Set the delivery as received."""
        assert self.can_receive()
        self._set_delivery_status(self.STATUS_RECEIVED)
        self.receive_date = TransactionTimestamp()

    #
    #  IContainer implementation
    #

    def add_item(self, item):
        item.delivery = self

    def get_items(self):
        return list(self.delivery_items)

    def remove_item(self, item):
        item.delivery = None

    def remove_all_items(self):
        for item in self.get_items():
            self.remove_item(item)

    #
    #  Private
    #

    def _set_delivery_status(self, status):
        old_status = self.status
        DeliveryStatusChangedEvent.emit(self, old_status)
        self.status = status


# remove_item takes an extra argument so we cant implement IContainer
# @implementer(IContainer)
@implementer(IInvoice)
class Sale(IdentifiableDomain):
    """Sale logic, the process of selling a |sellable| to a |client|.

    * calculates the sale price including discount/interest/markup
    * creates payments
    * decreases the stock for products
    * creates a delivery (optional)
    * verifies that the client is suitable
    * creates commissions to the sales person
    * add money to the till (if paid with money)
    * calculate taxes and fiscal book entries

    +----------------------------+----------------------------+
    | **Status**                 | **Can be set to**          |
    +----------------------------+----------------------------+
    | :obj:`STATUS_QUOTE`        | :obj:`STATUS_INITIAL`      |
    +----------------------------+----------------------------+
    | :obj:`STATUS_INITIAL`      | :obj:`STATUS_ORDERED`,     |
    +----------------------------+----------------------------+
    | :obj:`STATUS_ORDERED`      | :obj:`STATUS_CONFIRMED`    |
    |                            | :obj:`STATUS_CANCELLED`    |
    +----------------------------+----------------------------+
    | :obj:`STATUS_CONFIRMED`    | :obj:`STATUS_RENEGOTIATED` |
    +----------------------------+----------------------------+
    | :obj:`STATUS_CANCELLED`    | None                       |
    +----------------------------+----------------------------+
    | :obj:`STATUS_RENEGOTIATED` | None                       |
    +----------------------------+----------------------------+
    | :obj:`STATUS_RETURNED`     | None                       |
    +----------------------------+----------------------------+

    .. graphviz::

       digraph sale_status {
         STATUS_QUOTE -> STATUS_INITIAL;
         STATUS_INITIAL -> STATUS_ORDERED;
         STATUS_ORDERED -> STATUS_CONFIRMED;
         STATUS_ORDERED -> STATUS_CANCELLED;
         STATUS_CONFIRMED -> STATUS_CANCELLED;
         STATUS_CONFIRMED -> STATUS_RENEGOTIATED;
       }

    See also:
    `schema <http://doc.stoq.com.br/schema/tables/sale.html>`__
    """

    __storm_table__ = 'sale'

    repr_fields = ['identifier', 'status']

    #: The sale is opened, products or other |sellable| items might have
    #: been added.
    STATUS_INITIAL = u'initial'

    #: When asking for sale quote this is the initial state that is set before
    #: reaching the initial state
    STATUS_QUOTE = u'quote'

    #: This state means the order was left the quoting state, but cant just yet
    #: go to the confirmed state. This may happen for various reasons,
    #: like when there is not enough stock to confirm the sale; when the sale
    #: has pending work orders; or when the confirmation should happen on
    #: the till app (because of the CONFIRM_SALES_AT_TILL parameter)
    STATUS_ORDERED = u'ordered'

    #: The sale has been confirmed and all payments have been registered,
    #: but not necessarily paid.
    STATUS_CONFIRMED = u'confirmed'

    #: The sale has been canceled, this can only happen
    #: to an sale which has not yet reached the SALE_CONFIRMED status.
    STATUS_CANCELLED = u'cancelled'

    #: The sale has been returned, all the payments made have been canceled
    #: and the |client| has been compensated for everything already paid.
    STATUS_RETURNED = u'returned'

    #: A sale that is closed as renegotiated, all payments for this sale
    #: should be canceled at list point. Another new sale is created with
    #: the new, renegotiated payments.
    STATUS_RENEGOTIATED = u'renegotiated'

    statuses = collections.OrderedDict([
        (STATUS_INITIAL, _(u'Opened')),
        (STATUS_QUOTE, _(u'Quoting')),
        (STATUS_ORDERED, _(u'Ordered')),
        (STATUS_CONFIRMED, _(u'Confirmed')),
        (STATUS_CANCELLED, _(u'Cancelled')),
        (STATUS_RETURNED, _(u'Returned')),
        (STATUS_RENEGOTIATED, _(u'Renegotiated')),
    ])

    #: A numeric identifier for this object. This value should be used instead of
    #: :obj:`Domain.id` when displaying a numerical representation of this object to
    #: the user, in dialogs, lists, reports and such.
    identifier = IdentifierCol()

    #: status of the sale
    status = EnumCol(allow_none=False, default=STATUS_INITIAL)

    # FIXME: this doesn't really belong to the sale
    # FIXME: it should also be renamed and avoid *_id
    #: identifier for the coupon of this sale, used by a ECF printer
    coupon_id = IntCol()

    # FIXME: This doesn't appear to be used anywhere.
    #        Maybe we should remove it from the database.
    service_invoice_number = IntCol(default=None)

    #: the date sale was created, this is always set
    open_date = DateTimeCol(default_factory=localnow)

    #: the date sale was confirmed, or None if it hasn't been confirmed
    confirm_date = DateTimeCol(default=None)

    #: the date sale was paid, or None if it hasn't be paid
    close_date = DateTimeCol(default=None)

    #: the date sale was confirmed, or None if it hasn't been cancelled
    cancel_date = DateTimeCol(default=None)

    #: the date sale was confirmed, or None if it hasn't been returned
    return_date = DateTimeCol(default=None)

    #: date when this sale expires, used by quotes
    expire_date = DateTimeCol(default=None)

    #: This flag indicates if the sale its completely paid and received
    paid = BoolCol(default=False)

    #: discount of the sale, in absolute value, for instance::
    #:
    #:    sale.total_sale_amount = 150
    #:    sale.discount_value = 18
    #:    # the price of the sale will now be 132
    #:
    discount_value = PriceCol(default=0)

    #: surcharge of the sale, in absolute value, for instance::
    #:
    #:    sale.total_sale_amount = 150
    #:    sale.surcharge_value = 18
    #:    # the price of the sale will now be 168
    #:
    surcharge_value = PriceCol(default=0)

    #: the total value of all the items in the same, this is set when
    #: a sale is confirmed, this is the same as calling
    #: :obj:`Sale.get_total_sale_amount()` at the time of confirming the sale,
    total_amount = PriceCol(default=0)

    #: The reason the sale was cancelled
    cancel_reason = UnicodeCol()

    cfop_id = IdCol()

    #: the :class:`fiscal entry <stoqlib.domain.fiscal.CfopData>`
    cfop = Reference(cfop_id, 'CfopData.id')

    client_id = IdCol(default=None)

    #: the |client| who this sale was sold to
    client = Reference(client_id, 'Client.id')

    salesperson_id = IdCol()

    #: the |salesperson| who sold the sale
    salesperson = Reference(salesperson_id, 'SalesPerson.id')

    branch_id = IdCol()

    #: the |branch| this sale belongs to
    branch = Reference(branch_id, 'Branch.id')

    station_id = IdCol(allow_none=False)
    #: The station this object was created at
    station = Reference(station_id, 'BranchStation.id')

    transporter_id = IdCol(default=None)

    # FIXME: transporter should only be used on Delivery.
    #: If we have a delivery, this is the |transporter| for this sale
    transporter = Reference(transporter_id, 'Transporter.id')

    group_id = IdCol()

    #: the |paymentgroup| of this sale
    group = Reference(group_id, 'PaymentGroup.id')

    client_category_id = IdCol(default=None)

    #: the |clientcategory| used for price determination.
    client_category = Reference(client_category_id, 'ClientCategory.id')

    cost_center_id = IdCol(default=None)

    #: the |costcenter| that the cost of the products sold in this sale should
    #: be accounted for. When confirming a sale with a |costcenter| set, a
    #: |costcenterentry| will be created for each product
    cost_center = Reference(cost_center_id, 'CostCenter.id')

    #: list of :class:`comments <stoqlib.domain.sale.SaleComment>` for
    #: this sale
    comments = ReferenceSet('id', 'SaleComment.sale_id', order_by='SaleComment.date')

    #: All returned sales of this sale
    returned_sales = ReferenceSet('id', 'ReturnedSale.sale_id',
                                  order_by='ReturnedSale.return_date')

    deliveries = ReferenceSet('invoice_id', 'Delivery.invoice_id')

    invoice_id = IdCol()

    #: The |sale_token| id
    sale_token_id = IdCol()

    #: Reference to |SaleToken|
    sale_token = Reference(sale_token_id, 'SaleToken.id')

    #: The |invoice| generated by the sale
    invoice = Reference(invoice_id, 'Invoice.id')

    cancel_responsible_id = IdCol()
    #: The responsible for cancelling the sale. At the moment, the
    #: |loginuser| that cancelled the sale
    cancel_responsible = Reference(cancel_responsible_id, 'LoginUser.id')

    def __init__(self, store, branch: Branch, **kw):
        kw['invoice'] = Invoice(store=store, invoice_type=Invoice.TYPE_OUT, branch=branch)
        super(Sale, self).__init__(store=store, branch=branch, **kw)
        # Branch needs to be set before cfop, which triggers an
        # implicit flush.
        self.branch = branch
        if not 'cfop' in kw:
            self.cfop = sysparam.get_object(store, 'DEFAULT_SALES_CFOP')

    #
    # Classmethods
    #

    @classmethod
    def get_status_name(cls, status):
        """The :obj:`Sale.status` as a translated string"""
        if not status in cls.statuses:
            raise DatabaseInconsistency(_(u"Invalid status %d") % status)
        return cls.statuses[status]

    #
    # IContainer implementation
    #

    def add_item(self, sale_item):
        assert not sale_item.sale
        sale_item.sale = self

    def get_items(self, with_children=True):
        store = self.store
        query = SaleItem.sale == self
        if not with_children:
            query = And(query,
                        Eq(SaleItem.parent_item_id, None))
        return store.find(SaleItem, query).order_by(SaleItem.te_id)

    def remove_item(self, sale_item, user: LoginUser):
        if sale_item.quantity_decreased > 0:
            sale_item.return_to_stock(sale_item.quantity_decreased, user)

        # If the item removed is the item corresponding to the delivery, we need to
        # remove all items from the delivery, including the delivery itself
        delivery = sale_item.delivery_adaptor
        if delivery:
            delivery.remove_all_items()
            self.store.maybe_remove(delivery)
        sale_item.sale = None
        self.store.maybe_remove(sale_item)

    #
    # IInvoice implementation
    #

    @property
    def recipient(self):
        if self.client:
            return self.client.person
        return None

    @property
    def invoice_subtotal(self):
        return self.get_sale_subtotal()

    @property
    def invoice_total(self):
        return self.get_total_sale_amount()

    @property
    def nfe_coupon_info(self):
        """Returns
        """
        if not self.coupon_id:
            return None

        # According to the "Cartilha do ECF Emissor de Cupom Fiscal - Perguntas e
        # respostas, versão 3.2 - Abril 2016 da Sefaz de MG", the ECF serial number
        # is the number attributed by the establishment/user
        number = ECFGetPrinterUserNumberEvent.emit() or u''
        return Settable(number=number,
                        coo=self.coupon_id)

    # Status

    def can_order(self):
        """Only newly created sales can be ordered

        :returns: ``True`` if the sale can be ordered
        """
        return (self.status == Sale.STATUS_INITIAL or
                self.status == Sale.STATUS_QUOTE)

    def can_confirm(self):
        """Only ordered sales can be confirmed

        :returns: ``True`` if the sale can be confirmed
        """
        if self.client:
            method_values = {}
            for p in self.payments:
                # We should ignore already paid payments
                if p.is_paid():
                    continue
                method_values.setdefault(p.method, 0)
                method_values[p.method] += p.value
            for method, value in method_values.items():
                assert self.client.can_purchase(method, value)

        return (self.status == Sale.STATUS_ORDERED or
                self.status == Sale.STATUS_QUOTE)

    def can_set_paid(self):
        """Only confirmed sales can raise the flag paid. Also, the sale must have at least
        one payment and all the payments must be already paid.

        :returns: ``True`` if the sale can be set as paid
        """
        if self.paid:
            return False

        payments = list(self.payments)
        if not payments:
            return False

        return all(p.is_paid() for p in payments)

    def can_set_not_paid(self):
        """Only confirmed sales can be paid

        :returns: ``True`` if the sale can be set as paid
        """
        return self.paid

    def can_set_renegotiated(self):
        """Only sales with status confirmed can be renegotiated.

        :returns: ``True`` if the sale can be renegotiated
        """
        # This should be as simple as:
        # return self.status == Sale.STATUS_CONFIRMED
        # But due to bug 3890 we have to check every payment.
        return self.payments.find(
            Payment.status == Payment.STATUS_PENDING).count() > 0

    def can_cancel(self, user: LoginUser):
        """Only ordered, confirmed, paid and quoting sales can be cancelled.

        :returns: ``True`` if the sale can be cancelled
        """
        # None is acceptable as it means no one catch the event
        if SaleCanCancelEvent.emit(self) is False:
            return False

        if self.status in (Sale.STATUS_INITIAL, Sale.STATUS_CANCELLED,
                           Sale.STATUS_RETURNED, Sale.STATUS_RENEGOTIATED):
            return False

        # Can aways cancel a quote
        if self.status == Sale.STATUS_QUOTE:
            return True

        # When ALLOW_CANCEL_CONFIRMED_SALES is True, any sale can be cancelled
        # Admin user can always cancel as well
        if (sysparam.get_bool("ALLOW_CANCEL_CONFIRMED_SALES")
                or user.profile.check_app_permission(u'admin')):
            return True

        # If a sale is external, let the user cancel if its ordered (it might
        # have been cancelled in the external store).
        if (sysparam.get_bool("ALLOW_CANCEL_ORDERED_SALES") or
                self.is_external()):
            return self.status == Sale.STATUS_ORDERED

        # If we reached here, the sale is either ORDERED or CONFIRMED
        return False

    def can_return(self):
        """Only confirmed (with or without payment) sales can be returned

        :returns: ``True`` if the sale can be returned
        """
        return self.status == Sale.STATUS_CONFIRMED

    def can_edit(self):
        """Check if the sale can be edited.

        Only quoting and ordered sales can be edited, as long
        as they are not external.

        :returns: ``True`` if the sale can be edited
        """
        if self.is_external():
            return False

        return (self.status == Sale.STATUS_QUOTE or
                self.status == Sale.STATUS_ORDERED)

    def is_external(self):
        """Check if this is an external sale.

        :rtype: bool
        """
        return bool(SaleIsExternalEvent.emit(self))

    def is_returned(self):
        return self.status == Sale.STATUS_RETURNED

    def order(self, user: LoginUser):
        """Orders the sale

        Ordering a sale is the first step done after creating it.
        The state of the sale will change to Sale.STATUS_ORDERED.
        To order a sale you need to add sale items to it.
        A |client| might also be set for the sale, but it is not necessary.
        """
        assert self.can_order()
        if self.get_items().is_empty():
            raise SellError(_('The sale must have sellable items'))
        if self.client and not self.client.is_active:
            raise SellError(_('Unable to make sales for clients with status '
                              '%s') % self.client.get_status_string())

        self._set_sale_status(Sale.STATUS_ORDERED, user)

    def confirm(self, user: LoginUser, till=None):
        """Confirms the sale

        Confirming a sale means that the customer has confirmed the sale.
        Sale items containing products are physically received and
        the payments are agreed upon but not necessarily received.

        All money payments will be set as paid.

        :param till: the |till| where this sale was confirmed. Can
            be `None` in case the process was automated (e.g. a virtual store)
        """
        assert self.can_confirm()
        assert self.branch

        for item in self.get_items():
            self.validate_batch(item.batch, sellable=item.sellable)
            if item.sellable.product:
                ProductHistory.add_sold_item(self.store, self.branch, item)
            item.sell(user)

        self.total_amount = self.get_total_sale_amount()

        self.group.confirm()
        self._add_inpayments(till=till)
        self._create_fiscal_entries(user)

        # Save operation_nature and branch in Invoice table.
        self.invoice.branch = self.branch

        if self._create_commission_at_confirm():
            for payment in self.payments:
                self.create_commission(payment)

        if self.client:
            self.group.payer = self.client.person

        self.confirm_date = TransactionTimestamp()

        # When confirming a sale, all credit and money payments are
        # automatically paid.
        # Since some plugins may listen to the sale status change event, we should
        # set payments as paid before the status change.
        source_account = sysparam.get_object(self.store, 'SALES_ACCOUNT')
        destination_account = sysparam.get_object(self.store, 'TILLS_ACCOUNT')
        for method in self.store.find(PaymentMethod):
            if method.operation.pay_on_sale_confirm():
                self.group.pay_method_payments(method.method_name,
                                               source_account=source_account,
                                               destination_account=destination_account)

        old_status = self.status
        self._set_sale_status(Sale.STATUS_CONFIRMED, user)

        if self.current_sale_token:
            self.current_sale_token.close_token()

        # do not log money payments twice
        if not self.only_paid_with_money():
            if self.client:
                msg = _(u"Sale {sale_number} to client {client_name} was "
                        u"confirmed with value {total_value:.2f}.").format(
                    sale_number=self.identifier,
                    client_name=self.client.person.name,
                    total_value=self.get_total_sale_amount())
            else:
                msg = _(u"Sale {sale_number} without a client was "
                        u"confirmed with value {total_value:.2f}.").format(
                    sale_number=self.identifier,
                    total_value=self.get_total_sale_amount())
            Event.log(self.store, Event.TYPE_SALE, msg)

        StockOperationConfirmedEvent.emit(self, old_status)

    def set_paid(self):
        """Mark the sale as paid
        Marking a sale as paid means that all the payments have been received.
        """
        assert self.can_set_paid()

        # Right now commissions are created when the payment is confirmed
        # (if the parameter is set) or when the payment is confirmed.
        # This code is still here for the users that some payments created
        # (and paid) but no commission created yet.
        # This can be removed sometime in the future.
        for payment in self.payments:
            self.create_commission(payment)

        self.close_date = TransactionTimestamp()

        self.paid = True

        if self.only_paid_with_money():
            # Money payments are confirmed and paid, so lof them that way
            if self.client:
                msg = _(u"Sale {sale_number} to client {client_name} was paid "
                        u"and confirmed with value {total_value:.2f}.").format(
                    sale_number=self.identifier,
                    client_name=self.client.person.name,
                    total_value=self.get_total_sale_amount())
            else:
                msg = _(u"Sale {sale_number} without a client was paid "
                        u"and confirmed with value {total_value:.2f}.").format(
                    sale_number=self.identifier,
                    total_value=self.get_total_sale_amount())
        else:
            if self.client:
                msg = _(u"Sale {sale_number} to client {client_name} was paid "
                        u"with value {total_value:.2f}.").format(
                    sale_number=self.identifier,
                    client_name=self.client.person.name,
                    total_value=self.get_total_sale_amount())
            else:
                msg = _(u"Sale {sale_number} without a client was paid "
                        u"with value {total_value:.2f}.").format(
                    sale_number=self.identifier,
                    total_value=self.get_total_sale_amount())
        Event.log(self.store, Event.TYPE_SALE, msg)

    def set_not_paid(self):
        """Mark a sale as not paid. This happens when the user sets a
        previously paid payment as not paid.
        """
        assert self.can_set_not_paid()

        self.close_date = None
        self.paid = False

    def set_renegotiated(self, user: LoginUser):
        """Set the sale as renegotiated. The sale payments have been
        renegotiated and the operations will be done in
        another |paymentgroup|."""
        assert self.can_set_renegotiated()

        self.close_date = TransactionTimestamp()
        self._set_sale_status(Sale.STATUS_RENEGOTIATED, user)

    def set_not_returned(self, user: LoginUser):
        """Sets a sale as not returnd

        This will reset the sale status to confirmed (once you can only returna
        confirmed sale). Also, the return_date will be reset.
        """
        self._set_sale_status(Sale.STATUS_CONFIRMED, user)
        self.return_date = None

    def cancel(self, user: LoginUser, reason: str, force=False):
        """Cancel the sale

        You can only cancel an ordered sale. This will also cancel
        all the payments related to it.

        :param reason: A short text describing the cancellation reason.
        :param force: if ``True``, :meth:`.can_cancel` will not be asserted.
            Only use this if you really need to (for example, when canceling
            the last sale on the ecf)
        """
        if not force:
            assert self.can_cancel(user)

        for item in self.get_items():
            item.cancel(user)

        self.cancel_date = TransactionTimestamp()
        self.cancel_reason = reason
        self.cancel_responsible = user
        self.paid = False

        # Cancel payments
        for payment in self.payments:
            if payment.can_cancel():
                payment.cancel()

        if self.current_sale_token:
            self.current_sale_token.close_token()

        self._set_sale_status(Sale.STATUS_CANCELLED, user)

    def return_(self, returned_sale: ReturnedSale):
        """Returns a sale
        Returning a sale means that all the items are returned to the stock.
        A renegotiation object needs to be supplied which
        contains the invoice number and the eventual penalty

        :param returned_sale: a :class:`stoqlib.domain.returnedsale.ReturnedSale`
            object. It can be created by :meth:`create_sale_return_adapter`
        """
        assert self.can_return()
        assert isinstance(returned_sale, ReturnedSale)

        totally_returned = all([sale_item.is_totally_returned() for
                                sale_item in self.get_items()])
        if totally_returned:
            self.return_date = TransactionTimestamp()
            self._set_sale_status(Sale.STATUS_RETURNED, returned_sale.responsible)
            self.paid = False

        if self.client:
            if totally_returned:
                msg = _(u"Sale {sale_number} to client {client_name} was "
                        u"totally returned with value {total_value:.2f}. "
                        u"Reason: {reason}")
            else:
                msg = _(u"Sale {sale_number} to client {client_name} was "
                        u"partially returned with value {total_value:.2f}. "
                        u"Reason: {reason}")
            msg = msg.format(sale_number=self.identifier,
                             client_name=self.client.person.name,
                             total_value=returned_sale.returned_total,
                             reason=returned_sale.reason)
        else:
            if totally_returned:
                msg = _(u"Sale {sale_number} without a client was "
                        u"totally returned with value {total_value:.2f}. "
                        u"Reason: {reason}")
            else:
                msg = _(u"Sale {sale_number} without a client was "
                        u"partially returned with value {total_value:.2f}. "
                        u"Reason: {reason}")
            msg = msg.format(sale_number=self.identifier,
                             total_value=returned_sale.returned_total,
                             reason=returned_sale.reason)

        Event.log(self.store, Event.TYPE_SALE, msg)

    def set_items_discount(self, discount):
        """Apply discount on this sale's items

        :param decimal.Decimal discount: the discount to be applied
            as a percentage, e.g. 10.0, 22.5
        """
        new_total = currency(0)
        items = []
        for item in self.get_items():
            sellable = item.sellable
            if sellable.product and sellable.product.is_package:
                # We should not set discount for package_products
                continue
            items.append(item)
            item.set_discount(discount)
            new_total += quantize(item.price * item.quantity)

        # Since we apply the discount percentage above, items can generate a
        # 3rd decimal place, that will be rounded to the 2nd, making the value
        # differ. Find that difference and apply it to a sale item. The sale
        # item that will be used for this rounding is the first one that the
        # quantity can divide the diff.
        sale_base_subtotal = self.get_sale_base_subtotal()
        discount_value = quantize((sale_base_subtotal * discount) / 100)
        diff = new_total - sale_base_subtotal + discount_value

        if diff:
            # The value cannot be <= 0
            # Note that we should use price instead of base_price, since the
            # for above may have changed the price already
            for item in items:
                if (diff * 100) % item.quantity == 0:
                    item.price = max(item.price - diff / item.quantity, Decimal('0.01'))
                    break

    #
    # Accessors
    #

    def get_total_sale_amount(self, subtotal=None):
        """
        Fetches the total value  paid by the |client|.
        It can be calculated as::

            Sale total = Sum(product and service prices) + surcharge +
                             interest - discount

        :param subtotal: pre calculated subtotal, pass in this to avoid
           a querying the database
        :returns: the total value
        """

        if subtotal is None:
            subtotal = self.get_sale_subtotal()

        surcharge_value = self.surcharge_value or Decimal(0)
        discount_value = self.discount_value or Decimal(0)
        total_amount = subtotal + surcharge_value - discount_value
        return currency(total_amount)

    def get_sale_subtotal(self):
        """Fetch the subtotal for the sale, eg the sum of the
        prices for of all items.

        :returns: subtotal
        """
        total = 0
        for sale_item in self.get_items():
            total += sale_item.get_total()

        return currency(total)

    def get_sale_base_subtotal(self):
        """Get the base subtotal of items

        Just a helper that, unlike :meth:`.get_sale_subtotal`, will
        return the total based on item's base price.

        :returns: the base subtotal
        """
        items = self.get_items()
        subtotal = 0
        for item in items:
            sellable = item.sellable
            if sellable.product and sellable.product.is_package:
                # We should not sum package_product
                continue
            if item.parent_item:
                component = item.get_component(item.parent_item)
                subtotal += quantize(item.quantity * component.price)
            else:
                subtotal += quantize(item.quantity * item.base_price)
        return currency(subtotal)

    def get_items_total_quantity(self):
        """Fetches the total number of items in the sale

        :returns: number of items
        """
        return self.get_items().sum(SaleItem.quantity) or Decimal(0)

    def get_total_paid(self):
        """Return the total amount already paid for this sale

        :returns: the total amount paid
        """
        total_paid = 0
        for payment in self.group.get_valid_payments():
            if payment.is_inpayment() and payment.is_paid():
                # Already paid by client. Value instead of paid_value as the
                # second might have penalties and discounts not applicable here
                total_paid += payment.value
            elif payment.is_outpayment():
                # Already returned to client
                total_paid -= payment.value

        return currency(total_paid)

    def get_total_to_pay(self):
        """Missing payment value for this sale.

        Returns the value the client still needs to pay for this sale.
        This is the same as
        :meth:`.get_total_sale_amount` - :meth:`.get_total_paid`
        """
        return currency(self.get_total_sale_amount() - self.get_total_paid())

    def get_returned_value(self):
        """The total value returned from this sale.

        This will return the sum of all returned sales of this sale.
        """
        return currency(sum(i.returned_total for i in self.returned_sales))

    def get_available_discount_for_items(self, user=None, exclude_item=None):
        """Get available discount for items in this sale

        The available items discount is the total discount not used
        by items in this sale. For instance, if we have 2 products
        with a price of 100 and they can have 10% of discount, we have
        20 of discount available. If one of those products price
        is set to 98, that is, using 2 of it's discount, the available
        discount is now 18.

        :param user: passed to
            :meth:`stoqlib.domain.sellable.Sellable.get_maximum_discount`
            together with :obj:`.client_category` to check for the max
            discount for sellables on this sale
        :param exclude_item: a |saleitem| to exclude from the calculations.
            Useful if you are trying to get some extra discount for that
            item and you don't want it's discount to be considered here
        :returns: the available discount
        """
        available_discount = currency(0)
        used_discount = currency(0)

        for item in self.get_items():
            if item == exclude_item:
                continue
            # Don't put surcharges on the discount, or it can end up negative
            if item.price > item.base_price:
                continue

            used_discount += item.base_price - item.price
            max_discount = item.sellable.get_maximum_discount(
                category=self.client_category, user=user) / 100
            available_discount += item.base_price * max_discount

        return available_discount - used_discount

    def get_kitchen_items(self):
        """Returns sale items that require kitchen production

        This method checks firstly for the sellable_branch_override table,
        and if the sellable is not found there, it moves to sellable. It
        then returns a list of items whose sellable needs kitchen production.

        :returns: list of sale items that need kitchen production
        """
        return [item for item in self.get_items()
                if item.sellable.get_requires_kitchen_production(self.branch)]

    def get_details_str(self):
        """Returns the sale details

        The details are composed by the items notes, the delivery
        address and the estimated fix date

        Note that there might be some extra comments on :obj:`.comments`

        :returns: the sale details string.
        """
        details = []
        delivery_added = False
        for sale_item in self.get_items():
            if delivery_added is False:
                # FIXME: Add the delivery info just once can lead to an error.
                #        It's possible that some item went to delivery X while
                #        some went to delivery Y.
                delivery = sale_item.delivery
            if delivery is not None:
                details.append(_(u'Delivery Address: %s') %
                               delivery.address.get_address_string())
                # At the moment, we just support only one delivery per sale.
                delivery_added = True
                delivery = None
            else:
                if sale_item.notes:
                    details.append(_(u'"%s" Notes: %s') % (
                        sale_item.get_description(), sale_item.notes))
            if sale_item.is_service() and sale_item.estimated_fix_date:
                details.append(_(u'"%s" Estimated Fix Date: %s') % (
                    sale_item.get_description(),
                    sale_item.estimated_fix_date.strftime('%x')))
        return u'\n'.join(sorted(details))

    def get_salesperson_name(self):
        """
        :returns: the sales person name
        """
        return self.salesperson.get_description()

    def get_client_name(self):
        """Returns the client name, if a |client| has been provided for
        this sale

        :returns: the client name of a place holder string for sales without
           clients set.
        """
        if not self.client:
            return _(u'Not Specified')
        return self.client.get_name()

    def get_client_document(self):
        """Returns the client document for this sale

        This could be either its cnpj or cpf.
        """
        if not self.client_id:
            return None

        return self.client.person.get_cnpj_or_cpf()

    # FIXME: move over to client or person
    def get_client_role(self):
        """Fetches the client role

        :returns: the client role (an |individual| or a |company|) instance or
          None if the sale haven't |client| set.
        """
        if not self.client:
            return None
        client_role = self.client.person.has_individual_or_company_facets()
        if client_role is None:
            raise DatabaseInconsistency(
                _(u"The sale %r have a client but no "
                  u"client_role defined.") % self)

        return client_role

    def get_items_missing_batch(self):
        """Get all |saleitems| missing |batch|

        This usually happens when we create a quote. Since we are
        not removing the items from the stock, they probably were
        not set on the |saleitem|.

        :returns: a result set of |saleitems| that needs to set
            set the batch information
        """
        return self.store.find(
            SaleItem,
            And(SaleItem.sale_id == self.id,
                SaleItem.sellable_id == Sellable.id,
                Sellable.id == Storable.id,
                Eq(Storable.is_batch, True),
                Eq(SaleItem.batch_id, None)))

    def need_adjust_batches(self):
        """Checks if we need to set |batches| for this sale's |saleitems|

        This usually happens when we create a quote. Since we are
        not removing the items from the stock, they probably were
        not set on the |saleitem|.

        :returns: ``True`` if any |saleitem| needs a |batch|,
            ``False`` otherwise.
        """
        return not self.get_items_missing_batch().is_empty()

    def check_and_adjust_batches(self):
        """ Check batches and perform a first adjustment when a sale item has
        only one batch.

        :returns: ``True`` if all items that need a batch were adjusted, or
            ``False`` if there are items that were not possible to be adjusted.
        """
        # No batchs or batches already adjusted
        if not self.need_adjust_batches():
            return True

        all_adjusted = True
        sale_items = self.get_items_missing_batch()
        # Set unique batch.
        for item in sale_items:
            storable = item.sellable.product_storable
            available_batches = list(storable.get_available_batches(self.branch))
            if len(available_batches) == 1:
                item.batch = available_batches[0]
            else:
                all_adjusted = False

        return all_adjusted

    def only_paid_with_money(self):
        """Find out if the sale is paid using money

        :returns: ``True`` if the sale was paid with money
        """
        if self.payments.is_empty():
            return False
        return all(payment.is_of_method(u'money') for payment in self.payments)

    def add_sellable(self, sellable, quantity=1, price=None,
                     quantity_decreased=0, batch=None, parent=None):
        """Adds a new item to a sale.

        :param sellable: the |sellable|
        :param quantity: quantity to add, defaults to 1
        :param price: optional, the price, it not set the price
          from the sellable will be used
        :param quantity_decreased: the quantity already decreased from
          stock. e.g. The param quantity 10 and that quantity were already
          decreased, so this param should be 10 too.
        :param batch: the |batch| this sellable comes from, if the sellable is a
          storable. Should be ``None`` if it is not a storable or if the storable
          does not have batches.
        :param parent: a |sale_item| parent_item of another |sale_item|
        :returns: a |saleitem| for representing the
          sellable within this sale.
        """
        # Quote can add items without batches, but they will be validated
        # after on self.confirm
        if self.status not in (self.STATUS_QUOTE, self.STATUS_ORDERED):
            self.validate_batch(batch, sellable=sellable)
        if price is None:
            price = sellable.price
        return SaleItem(store=self.store,
                        quantity=quantity,
                        quantity_decreased=quantity_decreased,
                        sale=self,
                        sellable=sellable,
                        batch=batch,
                        price=price,
                        parent_item=parent)

    def create_sale_return_adapter(self, branch: Branch, user: LoginUser, station: BranchStation):
        store = self.store
        returned_sale = ReturnedSale(
            store=store,
            sale=self,
            branch=branch,
            responsible=user,
            station=station,
        )
        for sale_item in self.get_items(with_children=False):
            if sale_item.is_totally_returned():
                # Exclude quantities already returned from this one
                continue

            r_item = ReturnedSaleItem(
                store=store,
                sale_item=sale_item,
                returned_sale=returned_sale,
                quantity=sale_item.quantity_decreased,
                batch=sale_item.batch,
                # XXX Please note that when applying the sale discount in the
                # items, ther may be some rounding issues, leaving the total
                # value either greater or lower than the expected value.
                price=sale_item.price_with_discount
            )
            for child in sale_item.children_items:
                ReturnedSaleItem(store=store,
                                 sale_item=child,
                                 returned_sale=returned_sale,
                                 quantity=child.quantity_decreased,
                                 batch=child.batch,
                                 price=child.price_with_discount,
                                 parent_item=r_item)
        return returned_sale

    def create_commission(self, payment):
        """Creates a commission for the *payment*

        This will create a |commission| for the given |payment|,
        :obj:`.sale` and :obj:`.sale.salesperson`. Note that, if the
        payment already has a commission, nothing will be done.
        """
        from stoqlib.domain.commission import Commission
        if payment.has_commission():
            return

        commission = Commission(
            commission_type=self._get_commission_type(),
            sale=self,
            payment=payment,
            store=self.store)
        if payment.is_outpayment():
            commission.value = -commission.value

        return commission

    def get_first_sale_comment(self):
        first_comment = self.comments.first()
        if first_comment:
            return first_comment.comment
        return u''

    def get_delivery_item(self):
        delivery_service_id = sysparam.get_object_id('DELIVERY_SERVICE')
        for item in self.get_items():
            if item.sellable.id == delivery_service_id:
                return item
        return None

    #
    # Properties
    #

    @property
    def status_str(self):
        return self.get_status_name(self.status)

    @property
    def current_sale_token(self):
        """The current token attached to this sale."""
        return self.store.find(SaleToken, sale=self).one()

    @property
    def products(self):
        """All |saleitems| of this sale containing a |product|.

        :returns: the result set containing the |saleitems|, ordered
            by :attr:`stoqlib.domain.sellable.Sellable.code`
        """
        return self.store.find(
            SaleItem,
            And(SaleItem.sale_id == self.id,
                SaleItem.sellable_id == Sellable.id,
                Sellable.id == Product.id)).order_by(
            Sellable.code)

    @property
    def services(self):
        """All |saleitems| of this sale containing a |service|.

        :returns: the result set containing the |saleitems|, ordered
            by :attr:`stoqlib.domain.sellable.Sellable.code`
        """
        return self.store.find(
            SaleItem,
            And(SaleItem.sale_id == self.id,
                SaleItem.sellable_id == Sellable.id,
                Sellable.id == Service.id)).order_by(
            Sellable.code)

    @property
    def payments(self):
        """Returns all valid payments for this sale ordered by open date

        This will return a list of valid payments for this sale, that
        is, all payments on the |paymentgroups| that were not cancelled.
        If you need to get the cancelled too, use :obj:`.group.payments`.

        :returns: an ordered iterable of |payment|.
        """
        return self.group.get_valid_payments().order_by(Payment.open_date)

    @property
    def discount_percentage(self):
        """Sets a discount by percentage.

        Note that percentage must be added as an absolute value, in other
        words::

            sale.total_sale_amount = 200
            sale.discount_percentage = 5
            # the price of the sale will now be be `190`
        """
        discount_value = self.discount_value
        if not discount_value:
            return Decimal(0)
        subtotal = self.get_sale_subtotal()
        assert subtotal > 0, ('the sale subtotal should not be zero '
                              'at this point')
        total = subtotal - discount_value
        percentage = (1 - total / subtotal) * 100
        return quantize(percentage)

    @discount_percentage.setter
    def discount_percentage(self, value):
        self.discount_value = self._get_percentage_value(value)

    @property
    def surcharge_percentage(self):
        """Sets a discount by percentage.

        Note that percentage must be added as an absolute value, in other
        words::

            sale.total_sale_amount = 200
            sale.surcharge_percentage = 5
            # the price of the sale will now be `210`

        """
        surcharge_value = self.surcharge_value
        if not surcharge_value:
            return Decimal(0)
        subtotal = self.get_sale_subtotal()
        assert subtotal > 0, ('the sale subtotal should not be zero '
                              'at this point')
        total = subtotal + surcharge_value
        percentage = ((total / subtotal) - 1) * 100
        return quantize(percentage)

    @surcharge_percentage.setter
    def surcharge_percentage(self, value):
        self.surcharge_value = self._get_percentage_value(value)

    #
    # Private API
    #

    def _set_sale_status(self, status, user: LoginUser):
        old_status = self.status
        self.status = status

        SaleStatusChangedEvent.emit(self, old_status, user)

    def _get_percentage_value(self, percentage):
        if not percentage:
            return currency(0)
        subtotal = self.get_sale_subtotal()
        percentage = Decimal(percentage)
        perc_value = subtotal * (percentage / Decimal(100))
        # discount/surchage cannot have more than 2 decimal points
        return quantize(currency(perc_value))

    def _add_inpayments(self, till=None):
        payments = self.payments
        if not payments.count():
            raise ValueError(
                _('You must have at least one payment for each payment group'))

        if till is None:
            return

        for payment in payments:
            if not payment.is_inpayment():
                # There may be a change payment if the client has overpaid the
                # sale.
                continue
            till.add_entry(payment)

    def _create_commission_at_confirm(self):
        return sysparam.get_bool('SALE_PAY_COMMISSION_WHEN_CONFIRMED')

    def _get_commission_type(self):
        from stoqlib.domain.commission import Commission

        nitems = 0
        for item in self.payments:
            if not item.is_outpayment():
                nitems += 1

        if nitems <= 1:
            return Commission.DIRECT
        return Commission.INSTALLMENTS

    def _get_pm_commission_total(self):
        """Return the payment method commission total. Usually credit
        card payment method is the most common method which uses
        commission
        """
        return currency(0)

    def _get_icms_total(self, av_difference):
        """A Brazil-specific method
        Calculates the icms total value

        :param av_difference: the average difference for the sale items.
                              it means the average discount or surcharge
                              applied over all sale items
        """
        icms_total = Decimal(0)
        for item in self.products:
            price = item.price + av_difference
            sellable = item.sellable
            tax_constant = sellable.get_tax_constant()
            if tax_constant is None or tax_constant.tax_type != TaxType.CUSTOM:
                continue
            icms_tax = tax_constant.tax_value / Decimal(100)
            icms_total += icms_tax * quantize(price * item.quantity)

        return icms_total

    def _get_iss_total(self, av_difference):
        """A Brazil-specific method
        Calculates the iss total value

        :param av_difference: the average difference for the sale items.
                              it means the average discount or surcharge
                              applied over all sale items
        """
        iss_total = Decimal(0)
        iss_tax = sysparam.get_decimal('ISS_TAX') / Decimal(100)
        for item in self.services:
            price = item.price + av_difference
            iss_total += iss_tax * quantize(price * item.quantity)
        return iss_total

    def _get_average_difference(self):
        if self.get_items().is_empty():
            raise DatabaseInconsistency(
                _(u"Sale orders must have items, which means products or "
                  u"services"))
        total_quantity = self.get_items_total_quantity()
        if not total_quantity:
            raise DatabaseInconsistency(
                _(u"Sale total quantity should never be zero"))
        # If there is a discount or a surcharge applied in the whole total
        # sale amount, we must share it between all the item values
        # otherwise the icms and iss won't be calculated properly
        total = (self.get_total_sale_amount() -
                 self._get_pm_commission_total())
        subtotal = self.get_sale_subtotal()
        return (total - subtotal) / total_quantity

    def _get_iss_entry(self):
        return FiscalBookEntry.get_entry_by_payment_group(
            self.store, self.group,
            FiscalBookEntry.TYPE_SERVICE)

    def _create_fiscal_entries(self, user: LoginUser):
        """A Brazil-specific method
        Create new ICMS and ISS entries in the fiscal book
        for a given sale.

        Important: freight and interest are not part of the base value for
        ICMS. Only product values and surcharge which applies increasing the
        product totals are considered here.
        """
        av_difference = self._get_average_difference()

        if not self.products.is_empty():
            FiscalBookEntry.create_product_entry(
                self.store, self.branch, user,
                self.group, self.cfop, self.coupon_id,
                self._get_icms_total(av_difference))

        if not self.services.is_empty() and self.service_invoice_number:
            FiscalBookEntry.create_service_entry(
                self.store, self.branch, user,
                self.group, self.cfop, self.service_invoice_number,
                self._get_iss_total(av_difference))


class SaleToken(Domain):
    """A Token to help on sale for restaurants

    This will be attached to a |sale| to help the sale for restaurants, hotels.
    eg: table 1, table 2, room 12, room 334
    """

    __storm_table__ = 'sale_token'

    STATUS_AVAILABLE = u'available'
    STATUS_OCCUPIED = u'occupied'

    statuses = collections.OrderedDict([
        (STATUS_AVAILABLE, _(u'Available')),
        (STATUS_OCCUPIED, _(u'Occupied')),
    ])

    #: the status of the sale_token
    status = EnumCol(allow_none=False, default=STATUS_AVAILABLE)

    #: the code that used to identify the token
    code = UnicodeCol()

    #: The name of the token
    name = UnicodeCol()

    sale_id = IdCol()
    #: The |sale| that this token is attached to
    sale = Reference(sale_id, 'Sale.id')

    branch_id = IdCol()
    #: The |branch| that this token belongs
    branch = Reference(branch_id, 'Branch.id')

    @property
    def status_str(self):
        return self.statuses[self.status]

    @property
    def description(self):
        return "[{}] {}".format(self.code, self.name)

    #
    # Public API
    #

    @classmethod
    def find_by_client(cls, store, client):
        tables = [cls, Join(Sale, cls.sale_id == Sale.id)]
        return store.using(*tables).find(cls, Sale.client == client)

    def open_token(self, sale):
        assert self.can_open()
        self.sale = sale
        sale.sale_token = self
        self.status = SaleToken.STATUS_OCCUPIED

    def close_token(self):
        assert self.can_close()
        self.sale = None
        self.status = SaleToken.STATUS_AVAILABLE

    def can_open(self):
        return self.status == SaleToken.STATUS_AVAILABLE

    def can_close(self):
        return self.status == SaleToken.STATUS_OCCUPIED


class SaleTokenView(Viewable):
    """Sale token view."""

    ClientPerson = ClassAlias(Person, 'client_person')
    ClientCompany = ClassAlias(Company, 'client_company')
    BranchPerson = ClassAlias(Person, 'branch_person')
    BranchCompany = ClassAlias(Company, 'branch_company')

    sale_token = SaleToken
    sale = Sale
    client = Client
    branch = Branch

    id = SaleToken.id
    name = SaleToken.name
    code = SaleToken.code
    status = SaleToken.status

    client_id = Client.id
    client_name = Coalesce(NullIf(ClientCompany.fancy_name, u''), ClientPerson.name)
    branch_id = Branch.id
    branch_name = Coalesce(NullIf(BranchCompany.fancy_name, u''), BranchPerson.name)
    sale_identifier = Sale.identifier
    sale_identifier_str = Cast(Sale.identifier, 'text')

    tables = [
        SaleToken,

        # Sale
        LeftJoin(Sale, SaleToken.sale_id == Sale.id),

        # Client
        LeftJoin(Client, Sale.client_id == Client.id),
        LeftJoin(ClientPerson, Client.person_id == ClientPerson.id),
        LeftJoin(ClientCompany, ClientCompany.person_id == ClientPerson.id),

        # Branch
        LeftJoin(Branch, SaleToken.branch_id == Branch.id),
        LeftJoin(BranchPerson, Branch.person_id == BranchPerson.id),
        LeftJoin(BranchCompany, BranchCompany.person_id == BranchPerson.id),
    ]

    @property
    def status_str(self):
        return SaleToken.statuses[self.status]


class SaleComment(Domain):
    """A simple holder for |sale| comments

    See also:
    `schema <http://doc.stoq.com.br/schema/tables/sale_comment.html>`__
    """

    __storm_table__ = 'sale_comment'

    #: When this comment was created
    date = DateTimeCol(default_factory=localnow)

    #: The comment itself.
    comment = UnicodeCol()

    author_id = IdCol()
    #: The author of the comment
    author = Reference(author_id, 'LoginUser.id')

    sale_id = IdCol()
    #: The |sale| that was commented
    sale = Reference(sale_id, 'Sale.id')


#
# Views
#

class ReturnedSaleItemsView(Viewable):
    branch = Branch
    returned_sale = ReturnedSale
    sellable = Sellable

    # returned and original sale item
    id = ReturnedSaleItem.id
    quantity = ReturnedSaleItem.quantity
    price = ReturnedSaleItem.price
    parent_item_id = ReturnedSaleItem.parent_item_id

    # returned and original sale
    _sale_id = Sale.id
    _new_sale_id = ReturnedSale.new_sale_id
    returned_identifier = ReturnedSale.identifier
    invoice_number = Invoice.invoice_number
    return_date = ReturnedSale.return_date
    reason = ReturnedSale.reason

    # sellable
    sellable_id = ReturnedSaleItem.sellable_id
    code = Sellable.code
    description = Sellable.description

    batch_number = Coalesce(StorableBatch.batch_number, u'')
    batch_date = StorableBatch.create_date

    # summaries
    total = Round(ReturnedSaleItem.price * ReturnedSaleItem.quantity, DECIMAL_PRECISION)

    tables = [
        ReturnedSaleItem,
        LeftJoin(StorableBatch, StorableBatch.id == ReturnedSaleItem.batch_id),
        Join(SaleItem, SaleItem.id == ReturnedSaleItem.sale_item_id),
        Join(Sellable, Sellable.id == ReturnedSaleItem.sellable_id),
        Join(ReturnedSale, ReturnedSale.id == ReturnedSaleItem.returned_sale_id),
        LeftJoin(Invoice, Invoice.id == ReturnedSale.invoice_id),
        Join(Sale, Sale.id == ReturnedSale.sale_id),
        # Note that the sale branch may be different than the returned sale
        # branch
        Join(Branch, Branch.id == ReturnedSale.branch_id),
    ]

    @property
    def new_sale(self):
        if not self._new_sale_id:
            return None
        return self.store.get(Sale, self._new_sale_id)

    #
    # Class methods
    #

    @classmethod
    def find_by_sale(cls, store, sale):
        return store.find(cls, _sale_id=sale.id).order_by(ReturnedSale.return_date)

    @classmethod
    def find_parent_items(cls, store, sale):
        query = And(cls.returned_sale.sale_id == sale.id,
                    Eq(cls.parent_item_id, None))
        return store.find(cls, query)

    #
    # Public API
    #

    def get_children(self):
        return self.store.find(ReturnedSaleItemsView,
                               ReturnedSaleItemsView.parent_item_id == self.id)

    def is_package(self):
        if self.sellable.product is None:
            # Services
            return False
        product = self.store.get(Product, self.sellable.product.id)
        return product.is_package


_SaleItemSummary = Select(columns=[SaleItem.sale_id,
                                   Alias(Sum(InvoiceItemIpi.v_ipi), 'v_ipi'),
                                   Alias(Sum(SaleItem.quantity), 'total_quantity'),
                                   Alias(Sum(Round(SaleItem.quantity * SaleItem.price,
                                                   DECIMAL_PRECISION)), 'subtotal')],
                          tables=[SaleItem,
                                  LeftJoin(InvoiceItemIpi,
                                           InvoiceItemIpi.id == SaleItem.ipi_info_id)],
                          group_by=[SaleItem.sale_id])
SaleItemSummary = Alias(_SaleItemSummary, '_sale_item')

_TradeAndCreditTotal = Select(columns=[Payment.group_id,
                                       Alias(Sum(Payment.value), 'total')],
                              tables=[Payment,
                                      LeftJoin(PaymentMethod,
                                               PaymentMethod.id == Payment.method_id)],
                              where=And(In(PaymentMethod.method_name, ['credit', 'trade']),
                                        Payment.payment_type == Payment.TYPE_IN),
                              group_by=[Payment.group_id])
TradeAndCreditTotal = Alias(_TradeAndCreditTotal, '_trade_credit_total')

_PaymentTotal = Select(columns=[Payment.group_id,
                                Alias(Sum(Payment.value), 'total')],
                       tables=[Payment],
                       where=(Payment.status != Payment.STATUS_CANCELLED),
                       group_by=[Payment.group_id])
PaymentTotal = Alias(_PaymentTotal, '_payment_total')


class SaleView(Viewable):
    """Stores general information about sales
    """

    Person_Branch = ClassAlias(Person, 'person_branch')
    Person_Client = ClassAlias(Person, 'person_client')
    Person_SalesPerson = ClassAlias(Person, 'person_sales_person')
    Company_Branch = ClassAlias(Company, 'company_branch')
    Company_Client = ClassAlias(Company, 'company_client')

    #: the |sale| of the view
    sale = Sale  # type: Sale

    #: the |client| of the view
    client = Client

    #: The branch this sale was sold
    branch = Branch

    #: The |invoice| of the view
    invoice = Invoice

    #: The token referencing this sale
    token = SaleToken

    #: the id of the sale table
    id = Sale.id

    #: unique numeric identifier for the sale
    identifier = Sale.identifier

    #: unique numeric identifier for the sale, text representation
    identifier_str = Cast(Sale.identifier, 'text')

    #: The code of the current token holding the sale
    token_code = SaleToken.code

    #: The name of the current token holding the sale
    token_name = SaleToken.name

    token_str = Concat('[', token_code, '] ', token_name)

    #: the sale invoice number
    invoice_number = Invoice.invoice_number

    #: the id generated by the fiscal printer
    coupon_id = Sale.coupon_id

    #: the date when the sale was started
    open_date = Sale.open_date

    #: the date when the sale was closed
    close_date = Sale.close_date

    #: the date when the sale was confirmed
    confirm_date = Sale.confirm_date

    #: the date when the sale was cancelled
    cancel_date = Sale.cancel_date

    #: the date when the sale was returned
    return_date = Sale.return_date

    #: the date when the sale will expire
    expire_date = Sale.expire_date

    #: the sale status
    status = Sale.status

    #: the flag that indicates if the sale is completely paid
    paid = Sale.paid

    #: the sale surcharge value
    surcharge_value = Sale.surcharge_value

    #: the sale discount value
    discount_value = Sale.discount_value

    #: the |branch| where this |sale| was sold
    branch_id = Sale.branch_id

    #: the if of the |client| table
    client_id = Client.id

    #: the salesperson name
    salesperson_name = Coalesce(Person_SalesPerson.name, u'')

    #: the |sale| salesperson id
    salesperson_id = SalesPerson.id

    #: the |sale| client name
    client_name = Coalesce(Person_Client.name, u'')

    #: the |sale| client fancy name
    client_fancy_name = Company_Client.fancy_name

    #: name of the |branch| this |sale| was sold
    branch_name = Coalesce(NullIf(Company_Branch.fancy_name, u''), Person_Branch.name)

    # Summaries
    v_ipi = Coalesce(Field('_sale_item', 'v_ipi'), 0)

    #: the sum of all items in the sale
    _subtotal = Coalesce(Field('_sale_item', 'subtotal'), 0) + v_ipi

    #: the items total quantity for the sale
    total_quantity = Coalesce(Field('_sale_item', 'total_quantity'), 0)

    #: the subtotal - discount + charge
    _total = Coalesce(Field('_sale_item', 'subtotal'), 0) - \
        Sale.discount_value + Sale.surcharge_value + v_ipi

    #: the total of the sale without trades and credit values
    _net_total = _total - Coalesce(Field('_trade_credit_total', 'total'), 0)

    #: the total of the sale without trades and credit values
    missing_payment = _total - Coalesce(Field('_payment_total', 'total'), 0)

    tables = [
        Sale,
        LeftJoin(SaleItemSummary, Field('_sale_item', 'sale_id') == Sale.id),
        LeftJoin(TradeAndCreditTotal, Field('_trade_credit_total', 'group_id') == Sale.group_id),
        LeftJoin(PaymentTotal, Field('_payment_total', 'group_id') == Sale.group_id),
        LeftJoin(Branch, Sale.branch_id == Branch.id),
        LeftJoin(Client, Sale.client_id == Client.id),
        LeftJoin(SalesPerson, Sale.salesperson_id == SalesPerson.id),
        LeftJoin(Invoice, Sale.invoice_id == Invoice.id),

        LeftJoin(Person_Branch, Branch.person_id == Person_Branch.id),
        LeftJoin(Company_Branch, Company_Branch.person_id == Person_Branch.id),
        LeftJoin(Person_Client, Client.person_id == Person_Client.id),
        LeftJoin(Company_Client, Company_Client.person_id == Person_Client.id),
        LeftJoin(Person_SalesPerson, SalesPerson.person_id == Person_SalesPerson.id),

        LeftJoin(SaleToken, SaleToken.id == Sale.sale_token_id),
    ]

    @classmethod
    def post_search_callback(cls, sresults):
        select = sresults.get_select_expr(Count(1), Sum(cls._total),
                                          Sum(cls._net_total))
        return ('count', 'sum', 'net_sum'), select

    #
    # Class methods
    #

    @classmethod
    def find_by_branch(cls, store, branch):
        if branch:
            return store.find(cls, Sale.branch == branch)

        return store.find(cls)

    #
    # Properties
    #

    @property
    def returned_sales(self):
        return self.store.find(ReturnedSale, sale_id=self.id)

    @property
    def return_total(self):
        store = self.store
        returned_items = store.find(ReturnedSaleItemsView, Sale.id == self.id)
        return currency(returned_items.sum(ReturnedSaleItemsView.total) or 0)

    #
    # Public API
    #

    def can_return(self):
        return self.sale.can_return()

    def can_confirm(self):
        return self.sale.can_confirm()

    def can_cancel(self, user: LoginUser):
        return self.sale.can_cancel(user)

    def can_edit(self):
        return self.sale.can_edit()

    @property
    def subtotal(self):
        # The editor requires the model to be a currency, but _subtotal is a
        # decimal. So we need to convert it
        return currency(self._subtotal)

    @property
    def total(self):
        return currency(self._total)

    @property
    def net_total(self):
        return currency(self._net_total)

    @property
    def open_date_as_string(self):
        return self.open_date.strftime("%x")

    @property
    def status_name(self):
        return Sale.get_status_name(self.status)


class SaleCommentsView(Viewable):
    """A view for |salecomments|

    This is used to get the most information of a |salecomment|
    without doing lots of database queries
    """

    #: the |salecomment| object
    comment = SaleComment

    # SaleComment
    id = SaleComment.id
    comment = SaleComment.comment
    date = SaleComment.date

    # Sale
    sale_id = Sale.id
    sale_identifier = Sale.identifier

    # Person
    author_name = Person.name

    tables = [
        SaleComment,
        Join(Sale, SaleComment.sale_id == Sale.id),
        Join(LoginUser, SaleComment.author_id == LoginUser.id),
        Join(Person, LoginUser.person_id == Person.id),
    ]

    @classmethod
    def find_by_sale(cls, store, sale):
        """Find results for this view for *sale*

        :param store: a store
        :param sale: the |sale| used to filter the results
        :returns: the matching views
        :rtype: a sequence of :class:`SaleCommentsView`
        """
        return store.find(cls, sale_id=sale.id)


class ReturnedSaleView(Viewable):
    """Stores general informatios about returned sales."""

    Person_Branch = ClassAlias(Person, 'person_branch')
    Person_Client = ClassAlias(Person, 'person_client')
    Person_SalesPerson = ClassAlias(Person, 'person_sales_person')
    Person_LoginUser = ClassAlias(Person, 'person_login_user')

    sale = Sale
    client = Client
    branch = Branch
    returned_sale = ReturnedSale
    returned_item = ReturnedSaleItem

    # Sale
    sale_id = Sale.id

    # Returned Sale
    id = ReturnedSaleItem.id
    identifier = ReturnedSale.identifier
    identifier_str = Cast(ReturnedSale.identifier, 'text')
    invoice_number = Invoice.invoice_number
    return_date = ReturnedSale.return_date
    reason = ReturnedSale.reason
    responsible_id = ReturnedSale.responsible_id
    branch_id = ReturnedSale.branch_id
    new_sale_id = ReturnedSale.new_sale_id

    # Returned Sale Item
    price = ReturnedSaleItem.price
    quantity = ReturnedSaleItem.quantity
    total = Round(ReturnedSaleItem.price * ReturnedSaleItem.quantity, DECIMAL_PRECISION)

    # Sellable
    product_name = Sellable.description

    # Person
    salesperson_name = Person_SalesPerson.name
    client_name = Person_Client.name
    responsible_name = Person_LoginUser.name

    # Branch
    branch_name = Coalesce(NullIf(Company.fancy_name, u''), Person_Branch.name)

    # Client
    client_id = Client.id

    tables = [
        ReturnedSale,
        Join(Sale, Sale.id == ReturnedSale.sale_id),
        Join(ReturnedSaleItem,
             ReturnedSaleItem.returned_sale_id == ReturnedSale.id),
        Join(Sellable, Sellable.id == ReturnedSaleItem.sellable_id),

        Join(Branch, ReturnedSale.branch_id == Branch.id),
        Join(Person_Branch, Branch.person_id == Person_Branch.id),
        Join(Company, Company.person_id == Person_Branch.id),
        Join(SalesPerson, Sale.salesperson_id == SalesPerson.id),
        Join(Person_SalesPerson,
             SalesPerson.person_id == Person_SalesPerson.id),
        Join(LoginUser, LoginUser.id == ReturnedSale.responsible_id),
        Join(Person_LoginUser, Person_LoginUser.id == LoginUser.person_id),
        LeftJoin(Invoice, Sale.invoice_id == Invoice.id),
        LeftJoin(Client, Sale.client_id == Client.id),
        LeftJoin(Person_Client, Client.person_id == Person_Client.id),
    ]

    def get_children_items(self):
        query = And(ReturnedSaleView.client_id == self.client_id,
                    ReturnedSaleItem.id.is_in([child.id
                                               for child in self.returned_item.children_items]))
        return self.store.find(ReturnedSaleView, query)


class SalePaymentMethodView(SaleView):

    # If a sale has more than one payment, it will appear as much times in the
    # search. Must always be used with select(distinct=True).
    tables = SaleView.tables[:]
    tables.append(LeftJoin(Payment, Sale.group_id == Payment.group_id))

    #
    # Class Methods
    #

    @classmethod
    def find_by_payment_method(cls, store, method):
        if method:
            results = store.find(cls, And(Payment.method == method,
                                          Payment.status != Payment.STATUS_CANCELLED))
        else:
            results = store.find(cls)

        results.config(distinct=True)
        return results


class SoldSellableView(Viewable):
    Person_Client = ClassAlias(Person, 'person_client')
    Person_SalesPerson = ClassAlias(Person, 'person_sales_person')
    sale_item = SaleItem

    # Sellable
    id = Sellable.id
    code = Sellable.code
    description = Sellable.description

    # SaleItem
    sale_item_id = SaleItem.id

    # Client
    client_id = Sale.client_id
    client_name = Person_Client.name

    # Aggregates
    total_quantity = Sum(SaleItem.quantity)
    subtotal = Sum(Round(SaleItem.quantity * SaleItem.price, DECIMAL_PRECISION))

    group_by = [id, code, description, client_id, client_name, sale_item]

    tables = [
        Sellable,
        LeftJoin(SaleItem, SaleItem.sellable_id == Sellable.id),
        LeftJoin(Sale, Sale.id == SaleItem.sale_id),
        LeftJoin(Client, Sale.client_id == Client.id),
        LeftJoin(SalesPerson, Sale.salesperson_id == SalesPerson.id),
        LeftJoin(Person_Client, Client.person_id == Person_Client.id),
        LeftJoin(Person_SalesPerson, SalesPerson.person_id == Person_SalesPerson.id),
        LeftJoin(InvoiceItemIpi, InvoiceItemIpi.id == SaleItem.ipi_info_id),
    ]


class SoldServicesView(SoldSellableView):
    estimated_fix_date = SaleItem.estimated_fix_date

    group_by = SoldSellableView.group_by[:]
    group_by.append(estimated_fix_date)

    tables = SoldSellableView.tables[:]
    tables.append(Join(Service, Sellable.id == Service.id))


class SoldProductsView(SoldSellableView):

    value = SaleItem.price
    quantity = SaleItem.quantity
    total_value = Round(SaleItem.quantity * SaleItem.price, DECIMAL_PRECISION)
    sale_date = Sale.open_date

    tables = SoldSellableView.tables[:]
    tables.append(Join(Product, Sellable.id == Product.id))

    group_by = SoldSellableView.group_by[:]
    group_by.append(sale_date)

    def get_children_items(self):
        query = And(SoldProductsView.client_id == self.client_id,
                    SaleItem.id.is_in([child.id for child in self.sale_item.children_items]))
        return self.store.find(SoldProductsView, query)


# FIXME: This needs some more work, as currently, this viewable is:
#        * Not filtering the paiments correctly given a date.
#        * Not ignoring payments from returned sales
# Get the total amount already paid in a sale and group it by sales person
_PaidSale = Select(columns=[Sale.salesperson_id,
                            Alias(Sum(Payment.paid_value), 'paid_value')],
                   tables=[Sale, LeftJoin(Payment,
                                          Payment.group_id == Sale.group_id)],
                   group_by=[Sale.salesperson_id])

PaidSale = Alias(_PaidSale, '_paid_sale')


class SalesPersonSalesView(Viewable):

    id = SalesPerson.id
    name = Person.name

    # aggregates
    total_amount = Sum(Sale.total_amount)
    total_quantity = Sum(Field('_sale_item', 'total_quantity'))
    total_sales = Count(Sale.id)
    # paid_value = Field('_paid_sale', 'paid_value')

    group_by = [id, name]

    tables = [
        SalesPerson,
        LeftJoin(Sale, Sale.salesperson_id == SalesPerson.id),
        LeftJoin(SaleItemSummary, Field('_sale_item', 'sale_id') == Sale.id),
        LeftJoin(Person, Person.id == SalesPerson.person_id),
        # LeftJoin(PaidSale, Field('_paid_sale', 'salesperson_id') == SalesPerson.id),
    ]

    clause = Sale.status == Sale.STATUS_CONFIRMED

    @classmethod
    def find_by_date(cls, store, date):
        if date:
            if isinstance(date, tuple):
                date_query = And(Date(Sale.confirm_date) >= date[0],
                                 Date(Sale.confirm_date) <= date[1])
            else:
                date_query = Date(Sale.confirm_date) == date

            results = store.find(cls, date_query)
        else:
            results = store.find(cls)

        results.config(distinct=True)
        return results


class ClientsWithSaleView(Viewable):
    main_address = Address
    city_location = CityLocation

    id = Person.id
    person_name = Person.name
    phone = Person.phone_number
    email = Person.email

    cpf = Individual.cpf
    birth_date = Individual.birth_date

    cnpj = Company.cnpj

    category = ClientCategory.name

    sales = Count(Distinct(Sale.id))
    sale_items = Sum(SaleItem.quantity)
    total_amount = Sum(Round(SaleItem.price * SaleItem.quantity, DECIMAL_PRECISION))
    last_purchase = Max(Sale.confirm_date)

    tables = [
        Person,
        Join(Client, Person.id == Client.person_id),
        LeftJoin(ClientCategory, ClientCategory.id == Client.category_id),
        LeftJoin(Individual, Individual.person_id == Person.id),
        LeftJoin(Company, Company.person_id == Person.id),
        Join(Sale, Client.id == Sale.client_id),
        Join(SaleItem, SaleItem.sale_id == Sale.id),
        Join(Sellable, Sellable.id == SaleItem.sellable_id),
        LeftJoin(SellableCategory, SellableCategory.id == Sellable.category_id),
        LeftJoin(Address,
                 And(Address.person_id == Person.id,
                     Eq(Address.is_main_address, True))),
        LeftJoin(CityLocation, Address.city_location_id == CityLocation.id),
    ]

    group_by = [id, Individual.id, Company.id, ClientCategory.id,
                Address.id, CityLocation.id]

    clause = Sale.status == Sale.STATUS_CONFIRMED

    #
    # Public API
    #

    @property
    def address_string(self):
        return self.main_address.get_address_string()

    @property
    def details_string(self):
        return self.main_address.get_details_string()

    @property
    def cnpj_or_cpf(self):
        return self.cnpj or self.cpf


class SoldItemsByClient(Viewable):
    product = Product
    sellable = Sellable

    id = Concat(Sellable.id, Person.name)

    # Sellable
    code = Sellable.code
    description = Sellable.description
    sellable_category = SellableCategory.description

    # Client
    client_name = Person.name
    email = Person.email
    phone_number = Person.phone_number

    # Aggregates
    base_price = Avg(SaleItem.base_price)
    quantity = Sum(SaleItem.quantity)
    price = Avg(SaleItem.price)
    total = Sum(Round(SaleItem.quantity * SaleItem.price, DECIMAL_PRECISION))

    tables = [
        Sellable,
        Join(SellableCategory, SellableCategory.id == Sellable.category_id),
        Join(Product, Product.id == Sellable.id),
        Join(SaleItem, SaleItem.sellable_id == Sellable.id),
        Join(Sale, SaleItem.sale_id == Sale.id),
        LeftJoin(Client, Client.id == Sale.client_id),
        LeftJoin(Person, Person.id == Client.person_id),
    ]

    clause = Or(Sale.status == Sale.STATUS_CONFIRMED,
                Sale.status == Sale.STATUS_ORDERED)

    group_by = [id, Person.id, Product, sellable_category, Sellable.id]


_Payments = Select(
    columns=[Payment.group_id,
             Alias(Sum(Payment.value), 'value')],
    tables=[Payment, Join(PaymentMethod, PaymentMethod.id == Payment.method_id)],
    where=And(Payment.status != Payment.STATUS_CANCELLED,
              Payment.payment_type == Payment.TYPE_IN,
              PaymentMethod.method_name == u'credit'),
    group_by=[Payment.group_id])


class SoldItemsBySalesperson(Viewable):
    id = Sellable.id
    code = Sellable.code
    description = Sellable.description

    category = SellableCategory.description
    batch_number = Coalesce(StorableBatch.batch_number, u'')

    brand = Product.brand

    branch_name = Company.fancy_name
    salesperson_name = Person.name

    quantity = Sum(SaleItem.quantity)
    total = Sum(SaleItem.quantity * SaleItem.price)

    tables = [
        Sellable,
        LeftJoin(Product, Product.id == Sellable.id),
        LeftJoin(SellableCategory, Sellable.category_id == SellableCategory.id),
        Join(SaleItem, SaleItem.sellable_id == Sellable.id),
        Join(Sale, SaleItem.sale_id == Sale.id),
        LeftJoin(StorableBatch, StorableBatch.id == SaleItem.batch_id),
        Join(Branch, Sale.branch_id == Branch.id),
        Join(Company, Branch.person_id == Company.person_id),
        Join(SalesPerson, SalesPerson.id == Sale.salesperson_id),
        Join(Person, Person.id == SalesPerson.person_id),
    ]

    clause = And(Ne(Sale.confirm_date, None),
                 Sale.status != Sale.STATUS_CANCELLED)
    group_by = [id, branch_name, code, description, category, batch_number,
                salesperson_name, brand]


class Context(Domain):
    __storm_table__ = 'context'

    name = UnicodeCol(allow_none=False)

    start_time = TimeCol()

    end_time = TimeCol()

    branch_id = IdCol(allow_none=False)

    branch = Reference(branch_id, 'Branch.id')


class SaleContext(Domain):
    __storm_table__ = 'sale_context'

    sale_id = IdCol(allow_none=False)

    sale = Reference(sale_id, 'Sale.id')

    context_id = IdCol(allow_none=False)

    context = Reference(context_id, 'Context.id')
