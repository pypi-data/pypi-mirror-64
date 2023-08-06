# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2015 Async Open Source <http://www.async.com.br>
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
##
""" Transfer editors """

from gi.repository import Gtk
from kiwi.datatypes import ValidationError
from kiwi.python import Settable

from stoqlib.domain.transfer import TransferOrderItem
from stoqlib.gui.editors.baseeditor import BaseEditorSlave
from stoqlib.gui.editors.invoiceitemeditor import InvoiceItemEditor
from stoqlib.lib.defaults import MAX_INT
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext


class TransferItemEditor(InvoiceItemEditor):
    model_name = _(u"Transfer Item")
    model_type = TransferOrderItem

    def setup_slaves(self):
        self.item_slave = TransferItemSlave(self.store, self.model, parent=self)
        self.attach_slave('item-holder', self.item_slave)


class TransferItemSlave(BaseEditorSlave):
    gladefile = 'TransferItemSlave'
    model_type = TransferOrderItem
    proxy_widgets = ['stock_cost', 'quantity']

    def __init__(self, store, model, parent):
        self.model = model
        self.icms_slave = parent.icms_slave
        self.ipi_slave = parent.ipi_slave
        self.quantity_model = Settable(quantity=model.quantity)
        BaseEditorSlave.__init__(self, store, self.model)

    def _setup_widgets(self):
        self.original_cost.update(self.model.sellable.cost)
        for widget in [self.quantity, self.stock_cost]:
            widget.set_adjustment(Gtk.Adjustment(lower=0, upper=MAX_INT,
                                                 step_increment=1, page_increment=10))

    def setup_proxies(self):
        self._setup_widgets()
        self.proxy = self.add_proxy(self.model, self.proxy_widgets)
        self.add_proxy(self.quantity_model, ['quantity'])

    def _update_taxes(self):
        if self.ipi_slave:
            self.ipi_slave.update_values()
        if self.icms_slave:
            self.icms_slave.update_values()

    #
    # Kiwi callbacks
    #

    def after_stock_cost__changed(self, widget):
        self._update_taxes()

    def after_quantity__changed(self, widget):
        self._update_taxes()

    def on_quantity__validate(self, widget, value):
        if value <= 0:
            return ValidationError(_(u"The quantity should be greater than zero."))

    def on_stock_cost__validate(self, widget, value):
        if value <= 0:
            return ValidationError(_(u"The cost must be greater than zero."))
