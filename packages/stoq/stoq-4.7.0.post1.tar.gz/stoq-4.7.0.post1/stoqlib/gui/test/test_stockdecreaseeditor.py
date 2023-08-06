# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2015 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

import mock

from stoqlib.domain.taxes import (ProductIcmsTemplate,
                                  ProductIpiTemplate,
                                  ProductTaxTemplate)
from stoqlib.gui.editors.stockdecreaseeditor import StockDecreaseItemEditor
from stoqlib.gui.test.uitestutils import GUITest


class TestStockDecreaseItemEditor(GUITest):
    def test_show_item_editor(self):
        decrease_item = self.create_stock_decrease_item()
        editor = StockDecreaseItemEditor(self.store, decrease_item)
        self.check_editor(editor, 'editor-stock-decrease-item-edit')

        with mock.patch('stoqlib.lib.pluginmanager.PluginManager.is_active') as patch:
            patch.return_value = True
            editor = StockDecreaseItemEditor(self.store, decrease_item)
            self.check_editor(editor, 'editor-stock-decrease-item-with-nfe')


class TestStockDecreaseItemSlave(GUITest):
    def test_show(self):
        sellable = self.create_sellable()
        sellable.cost = 100
        decrease_item = self.create_stock_decrease_item(sellable=sellable,
                                                        quantity=2,
                                                        cost=150)
        editor = StockDecreaseItemEditor(self.store, decrease_item)
        slave = editor.item_slave
        self.assertEqual(slave.original_cost.read(), 100)
        self.assertEqual(slave.cost.read(), 150)
        self.assertEqual(slave.quantity.get_value(), 2)
        self.check_slave(slave, 'slave-stock-decrease-item-show')

    def test_on_quantity__validate(self):
        decrease_item = self.create_stock_decrease_item(quantity=10)
        editor = StockDecreaseItemEditor(self.store, decrease_item)
        slave = editor.item_slave
        self.assertEqual(slave.quantity.get_value(), 10)
        slave.quantity.update(0)
        self.assertInvalid(slave, ['quantity'])
        slave.quantity.update(1)
        self.assertValid(slave, ['quantity'])

    def test_on_cost__validate(self):
        decrease_item = self.create_stock_decrease_item(cost=150)
        editor = StockDecreaseItemEditor(self.store, decrease_item)
        slave = editor.item_slave
        self.assertEqual(slave.cost.get_value(), 150)
        slave.cost.update(0)
        self.assertInvalid(slave, ['cost'])
        slave.cost.update(100)
        self.assertValid(slave, ['cost'])

    def test_update_taxes(self):
        tax_template = ProductTaxTemplate(store=self.store,
                                          tax_type=ProductTaxTemplate.TYPE_ICMS)
        icms_template = ProductIcmsTemplate(store=self.store,
                                            product_tax_template=tax_template)
        icms_template.csosn = 201

        tax_template = ProductTaxTemplate(store=self.store,
                                          tax_type=ProductTaxTemplate.TYPE_IPI)
        ipi_template = ProductIpiTemplate(store=self.store,
                                          product_tax_template=tax_template)
        ipi_template.cst = 00

        pis_template = self.create_product_pis_template(cst=49)
        self.assertEqual(pis_template.cst, 49)

        cofins_template = self.create_product_cofins_template(cst=49)
        self.assertEqual(cofins_template.cst, 49)

        product = self.create_product()
        product.set_icms_template(icms_template)
        product.set_ipi_template(ipi_template)
        product.set_pis_template(pis_template)
        product.set_cofins_template(cofins_template)
        decrease_item = self.create_stock_decrease_item(sellable=product.sellable,
                                                        cost=100,
                                                        quantity=1)
        with mock.patch('stoqlib.lib.pluginmanager.PluginManager.is_active') as patch:
            patch.return_value = True
            editor = StockDecreaseItemEditor(self.store, decrease_item)
            slave = editor.item_slave
            icms_slave = editor.icms_slave
            ipi_slave = editor.ipi_slave
            self.assertEqual(icms_slave.v_bc_st.read(), 100)
            self.assertEqual(ipi_slave.v_bc.read(), 100)
            slave.cost.update(150)
            self.assertEqual(icms_slave.v_bc_st.read(), 150)
            self.assertEqual(ipi_slave.v_bc.read(), 150)
            slave.quantity.update(2)
            self.assertEqual(icms_slave.v_bc_st.read(), 300)
            self.assertEqual(ipi_slave.v_bc.read(), 300)
