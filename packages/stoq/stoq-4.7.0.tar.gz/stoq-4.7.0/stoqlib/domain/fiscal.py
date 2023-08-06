# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

#
# Copyright (C) 2006-2007 Async Open Source <http://www.async.com.br>
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
#
#  Author(s): Stoq Team <stoq-devel@async.com.br>
#
""" Domain classes to manage fiscal informations.

Note that this whole module is Brazil-specific.
"""

# pylint: enable=E1101

import collections

from storm.expr import LeftJoin, Join, Or
from storm.references import Reference
from zope.interface import implementer

from stoqlib.database.expr import Date, TransactionTimestamp
from stoqlib.database.properties import (UnicodeCol, DateTimeCol, IntCol, BoolCol,
                                         IdCol, EnumCol)
from stoqlib.database.properties import PriceCol
from stoqlib.database.viewable import Viewable
from stoqlib.domain.base import Domain
from stoqlib.domain.interfaces import IDescribable, IReversal
from stoqlib.domain.person import Person, Branch, LoginUser
from stoqlib.lib.dateutils import localnow
from stoqlib.lib.parameters import sysparam
from stoqlib.lib.pluginmanager import get_plugin_manager
from stoqlib.lib.translation import stoqlib_gettext


_ = stoqlib_gettext


@implementer(IDescribable)
class CfopData(Domain):
    """A Brazil-specific class wich defines a fiscal code of operations.
    In Brazil it means 'Codigo Fiscal de Operacoes e Prestacoes'

    Canonical list of C.F.O.Ps can be found `here <http://tinyurl.com/mncsnlf>`__

    See also:
    `schema <http://doc.stoq.com.br/schema/tables/cfop_data.html>`__
    """

    __storm_table__ = 'cfop_data'

    #: fiscal code, for example. 1.102
    code = UnicodeCol()

    #: description, for example "Compra para comercialização"
    description = UnicodeCol()

    @classmethod
    def get_for_sale(cls, store):
        return store.find(cls, Or(CfopData.code.startswith(u'5'),
                                  CfopData.code.startswith(u'6'),
                                  CfopData.code.startswith(u'7')))

    @classmethod
    def get_for_receival(cls, store):
        return store.find(cls, Or(CfopData.code.startswith(u'1'),
                                  CfopData.code.startswith(u'2'),
                                  CfopData.code.startswith(u'3')))

    def get_description(self):
        # FIXME: kgetattr tries to get this instead of self.description,
        # making it return u" " on a new model. How to fix that properly?
        if not self.code and not self.description:
            return u""
        return u"%s %s" % (self.code, self.description)


@implementer(IReversal)
class FiscalBookEntry(Domain):

    __storm_table__ = 'fiscal_book_entry'

    (TYPE_PRODUCT,
     TYPE_SERVICE,
     TYPE_INVENTORY) = range(3)

    date = DateTimeCol(default_factory=localnow)
    is_reversal = BoolCol(default=False)
    invoice_number = IntCol()
    cfop_id = IdCol()
    cfop = Reference(cfop_id, 'CfopData.id')
    branch_id = IdCol()
    branch = Reference(branch_id, 'Branch.id')
    drawee_id = IdCol(default=None)
    drawee = Reference(drawee_id, 'Person.id')
    payment_group_id = IdCol(default=None)
    payment_group = Reference(payment_group_id, 'PaymentGroup.id')
    iss_value = PriceCol(default=None)
    icms_value = PriceCol(default=None)
    ipi_value = PriceCol(default=None)
    entry_type = IntCol(default=None)

    @classmethod
    def has_entry_by_payment_group(cls, store, payment_group, entry_type):
        return bool(cls.get_entry_by_payment_group(
            store, payment_group, entry_type))

    @classmethod
    def get_entry_by_payment_group(cls, store, payment_group, entry_type):
        return store.find(cls, payment_group=payment_group,
                          is_reversal=False,
                          entry_type=entry_type).one()

    @classmethod
    def _create_fiscal_entry(cls, store, branch: Branch, user: LoginUser, entry_type, group, cfop,
                             invoice_number, iss_value=0, icms_value=0, ipi_value=0):
        return FiscalBookEntry(
            entry_type=entry_type,
            iss_value=iss_value,
            ipi_value=ipi_value,
            icms_value=icms_value,
            invoice_number=invoice_number,
            cfop=cfop,
            drawee=group.recipient,
            branch=branch,
            date=TransactionTimestamp(),
            payment_group=group,
            store=store)

    @classmethod
    def create_product_entry(cls, store, branch: Branch, user: LoginUser, group, cfop,
                             invoice_number, value, ipi_value=0):
        """Creates a new product entry in the fiscal book

        :param store: a store
        :param group: payment group
        :type  group: :class:`PaymentGroup`
        :param cfop: cfop for the entry
        :type  cfop: :class:`CfopData`
        :param invoice_number: payment invoice number
        :param value: value of the payment
        :param ipi_value: ipi value of the payment
        :returns: a fiscal book entry
        :rtype: :class:`FiscalBookEntry`
        """
        return cls._create_fiscal_entry(store, branch, user, FiscalBookEntry.TYPE_PRODUCT, group,
                                        cfop, invoice_number, icms_value=value,
                                        ipi_value=ipi_value,)

    @classmethod
    def create_service_entry(cls, store, branch: Branch, user: LoginUser, group, cfop,
                             invoice_number, value):
        """Creates a new service entry in the fiscal book

        :param store: a store
        :param group: payment group
        :type  group: :class:`PaymentGroup`
        :param cfop: cfop for the entry
        :type  cfop: :class:`CfopData`
        :param invoice_number: payment invoice number
        :param value: value of the payment
        :returns: a fiscal book entry
        :rtype: :class:`FiscalBookEntry`
        """
        return cls._create_fiscal_entry(store, branch, user, FiscalBookEntry.TYPE_SERVICE, group,
                                        cfop, invoice_number, iss_value=value,)

    def reverse_entry(self, invoice_number,
                      iss_value=None, icms_value=None, ipi_value=None):
        store = self.store
        icms_value = icms_value if icms_value is not None else self.icms_value
        iss_value = iss_value if iss_value is not None else self.iss_value
        ipi_value = ipi_value if ipi_value is not None else self.ipi_value

        return FiscalBookEntry(
            entry_type=self.entry_type,
            iss_value=iss_value,
            icms_value=icms_value,
            ipi_value=ipi_value,
            cfop_id=sysparam.get_object_id('DEFAULT_SALES_CFOP'),
            branch=self.branch,
            invoice_number=invoice_number,
            drawee=self.drawee,
            is_reversal=True,
            payment_group=self.payment_group,
            store=store)


class _FiscalBookEntryView(Viewable):

    book_entry = FiscalBookEntry

    id = FiscalBookEntry.id
    date = Date(FiscalBookEntry.date)
    invoice_number = FiscalBookEntry.invoice_number
    cfop_id = FiscalBookEntry.cfop_id
    branch_id = FiscalBookEntry.branch_id
    drawee_id = FiscalBookEntry.drawee_id
    payment_group_id = FiscalBookEntry.payment_group_id
    cfop_code = CfopData.code
    drawee_name = Person.name

    tables = [
        FiscalBookEntry,
        LeftJoin(Person, Person.id == FiscalBookEntry.drawee_id),
        Join(CfopData, CfopData.id == FiscalBookEntry.cfop_id)
    ]


class Invoice(Domain):
    """Stores information about invoices"""

    __storm_table__ = 'invoice'

    TYPE_IN = u'in'
    TYPE_OUT = u'out'

    LEGACY_MODE = u'legacy'
    NFE_MODE = u'nfe'
    NFCE_MODE = u'nfce'

    MODES = collections.OrderedDict([
        (55, NFE_MODE),
        (65, NFCE_MODE),
    ])

    MODE_NAMES = {
        NFE_MODE: _('NF-e'),
        NFCE_MODE: _('NFC-e')
    }

    #: the invoice number
    invoice_number = IntCol()

    #: the operation nature
    operation_nature = UnicodeCol()

    #: the invoice type, representing an IN/OUT operation
    invoice_type = EnumCol(allow_none=False)

    #: the invoice series
    series = IntCol(default=None)

    #: the invoice mode
    mode = EnumCol(default=None)

    #: the key generated by NF-e plugin
    key = UnicodeCol()

    #: numeric code randomly generated for each NF-e
    cnf = UnicodeCol()

    branch_id = IdCol()

    #: the |branch| where this invoice was generated
    branch = Reference(branch_id, 'Branch.id')

    def __init__(self, branch: Branch, **kw):
        super(Invoice, self).__init__(branch=branch, **kw)

    @classmethod
    def get_next_invoice_number(cls, store, branch: Branch, mode=None, series=None):
        return Invoice.get_last_invoice_number(store, branch, series, mode) + 1

    @classmethod
    def get_last_invoice_number(cls, store, branch: Branch, series=None, mode=None):
        """Returns the last invoice number. If there is not an invoice
        number used, the returned value will be zero.

        :param store: a store
        :returns: an integer representing the last sale invoice number
        """
        last = store.find(cls, branch=branch, series=series,
                          mode=mode).max(cls.invoice_number)
        return last or 0

    @property
    def operation(self):
        from stoqlib.domain.loan import Loan
        from stoqlib.domain.returnedsale import ReturnedSale
        from stoqlib.domain.sale import Sale
        from stoqlib.domain.stockdecrease import StockDecrease
        from stoqlib.domain.transfer import TransferOrder
        for op_class in [Sale, StockDecrease, Loan, ReturnedSale, TransferOrder]:
            operation = self.store.find(op_class, invoice_id=self.id).one()
            if operation:
                return operation

        raise AssertionError("No operation corresponding to this invoice")

    def check_unique_invoice_number_by_branch(self, invoice_number, branch,
                                              mode, series=None):
        """Check if the invoice_number is used in determined branch

        :param invoice_number: the invoice number we want to check
        :param branch: the |branch| of the invoice
        :param mode: one of the Invoice.mode
        :param series: the series of the invoice
        """
        queries = {Invoice.invoice_number: invoice_number,
                   Invoice.branch_id: branch.id,
                   Invoice.mode: mode,
                   Invoice.series: series}
        return self.check_unique_tuple_exists(queries)

    def check_invoice_info_consistency(self):
        """If the invoice number is set, series and mode should also be.

        We should have a database constraint for this, but since these three data
        isn't saved at once, the constraint would brake every time.
        """
        # FIXME: The nfce plugin is responsible for generating those
        # information now, but that broke our nfe plugin since it
        # needs an invoice number, but not the mode an the series.
        # We should find a better way of handling this since we don't
        # want to polute the nfe/nfce invoice number namespace.
        pg = get_plugin_manager()
        if pg.is_active('nfe'):  # pragma nocoverage
            return

        # FIXME: We should not use assert in this kind of code since
        # there's an optimization flag on python that removes all the asserts
        assert ((self.invoice_number and self.series and self.mode) or
                (not self.invoice_number and not self.series and not self.mode))

    def on_create(self):
        self.check_invoice_info_consistency()

    def on_update(self):
        self.check_invoice_info_consistency()


class IcmsIpiView(_FiscalBookEntryView):
    """
    Stores information about the taxes (ICMS and IPI) related to a
    certain product.
    This view is used to query the product tax information.

    :param id: the id of the fiscal_book_entry
    :param icms_value: the total value of icms
    :param ipi_value: the total value of ipi
    :param date: the date when the entry was created
    :param invoice_number: the invoice number
    :param cfop_data_id: the cfop
    :param cfop_code: the code of the cfop
    :param drawee_name: the drawee name
    :param drawee_id: the person
    :param branch_id: the branch
    :param payment_group_id: the payment group
    """

    icms_value = FiscalBookEntry.icms_value
    ipi_value = FiscalBookEntry.ipi_value

    clause = FiscalBookEntry.entry_type == FiscalBookEntry.TYPE_PRODUCT


class IssView(_FiscalBookEntryView):
    """
    Stores information related to a service tax (ISS).
    This view is used to query the service tax information.

    :param id: the id of the fiscal_book_entry
    :param iss_value: the total value of ipi
    :param date: the date when the entry was created
    :param invoice_number: the invoice number
    :param cfop_data_id: the if of the cfop_data table
    :param cfop_code: the code of the cfop
    :param drawee_name: the drawee name
    :param drawee_id: the person
    :param branch_id: the branch
    :param payment_group_id: the payment group
    """

    iss_value = FiscalBookEntry.iss_value

    clause = FiscalBookEntry.entry_type == FiscalBookEntry.TYPE_SERVICE
