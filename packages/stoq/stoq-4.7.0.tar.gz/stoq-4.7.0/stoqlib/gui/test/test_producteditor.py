# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2012-2015 Async Open Source <http://www.async.com.br>
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

import base64
from decimal import Decimal

import mock
from storm.expr import Update

from stoqlib.domain.commission import CommissionSource
from stoqlib.domain.inventory import Inventory
from stoqlib.domain.product import Product, ProductStockItem
from stoqlib.domain.sellable import SellableCategory, Sellable
from stoqlib.database.runtime import get_current_branch
from stoqlib.gui.editors.producteditor import (ProductEditor,
                                               ProductionProductEditor,
                                               ProductStockQuantityEditor)
from stoqlib.gui.test.uitestutils import GUITest
from stoqlib.gui.slaves.productslave import ProductComponentSlave
from stoqlib.lib.parameters import sysparam

# A (1px, 1px) image
_image = base64.b64decode("""
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI
WXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3wEPEDYaIuf2wwAAABl0RVh0Q29tbWVudABDcmVhdGVk
IHdpdGggR0lNUFeBDhcAAAANSURBVAjXY2BgYGAAAAAFAAFe8yo6AAAAAElFTkSuQmCC
""")


# TODO: Test product editor for products without storable
class TestProductEditor(GUITest):
    def tearDown(self):
        sysparam.set_int(self.store, 'COST_PRECISION_DIGITS', 2)
        GUITest.tearDown(self)

    def test_create(self):
        editor = ProductEditor(self.store)
        editor.code.update("12345")
        self.check_editor(editor, 'editor-product-create')

    def test_create_without_category(self):
        # Removing data from SellableCategory, so we can test the validation of
        # category_combo update when there is no category.
        self.store.execute(Update({Sellable.category_id: None}, table=Sellable))
        self.clean_domain([CommissionSource, SellableCategory])

        editor = ProductEditor(self.store)
        editor.code.update("12345")
        self.assertNotSensitive(editor, ['category_combo'])
        self.check_editor(editor, 'editor-product-create-no-category')

    def test_create_grid_product(self):
        grid_product = self.create_product(is_grid=True)
        editor = ProductEditor(self.store, grid_product)
        self.assertEqual(grid_product.product_type, Product.TYPE_GRID)
        self.check_editor(editor, 'editor-product-create-grid-product')

    def test_create_with_template(self):
        attribute_group = self.create_attribute_group()
        grid_attribute = self.create_grid_attribute(attribute_group=attribute_group,
                                                    description=u'attr 1')
        grid_attribute2 = self.create_grid_attribute(attribute_group=attribute_group,
                                                     description=u'attr 2')
        grid_product = self.create_product(storable=True, is_grid=True)
        self.create_product_attribute(product=grid_product, attribute=grid_attribute)
        self.create_product_attribute(product=grid_product, attribute=grid_attribute2)
        editor = ProductEditor(self.store, product_type=Product.TYPE_GRID,
                               template=grid_product)
        # Be sure that its not the same product
        self.assertNotEqual(grid_product, editor.model)
        # But they have the same list of |grid_attribute|
        grid_product_attributes = set(attr.attribute for attr in grid_product.attributes)
        model_attributes = set(attr.attribute for attr in editor.model.attributes)
        self.assertEqual(grid_product_attributes, model_attributes)
        # and they are not empty
        self.assertNotEqual(len(model_attributes), 0)

    def test_show(self):
        product = self.create_product(storable=True)
        image = self.create_image()
        image.image = _image
        image.sellable = product.sellable

        editor = ProductEditor(self.store, product)
        editor.code.update("12345")
        self.check_editor(editor, 'editor-product-show')

    def test_visual_mode(self):
        product = self.create_product(storable=True)
        editor = ProductEditor(self.store, product, visual_mode=True)
        editor.code.update("12412")
        self.assertNotSensitive(editor, ['add_category', 'sale_price_button'])
        self.check_editor(editor, 'editor-product-visual-mode')

    def test_cost_precision_digits(self):
        # Set a number of digts greated than 2
        sysparam.set_int(self.store, 'COST_PRECISION_DIGITS', 5)

        product = self.create_product(storable=True)
        product.sellable.cost = Decimal('1.23456')
        editor = ProductEditor(self.store, product)
        editor.code.update("12345")
        # We expect the editor to show the correct value
        self.check_editor(editor, 'editor-product-cost-precision-digits')


class TestProductProductionEditor(GUITest):
    def test_create(self):
        editor = ProductionProductEditor(self.store)
        editor.code.update("12345")
        self.check_editor(editor, 'editor-product-prod-create')

    def test_show(self):
        component = self.create_product_component(storable=True)
        component.component.sellable.code = u'4567'
        editor = ProductionProductEditor(
            self.store, component.product)
        editor.code.update("12345")
        self.check_editor(editor, 'editor-product-prod-show')

    def test_confirm(self):
        component = self.create_product_component(storable=True)
        component.component.sellable.code = u'4567'
        component.product.sellable.code = u'6789'
        editor = ProductionProductEditor(self.store, component.product)

        self.click(editor.main_dialog.ok_button)
        self.check_editor(editor, 'editor-product-prod-confirm',
                          [editor.retval])

    @mock.patch('stoqlib.gui.slaves.productslave.run_dialog')
    def test_edit_component(self, run_dialog):
        run_dialog.return_value = None
        component = self.create_product_component()
        component.component.sellable.code = u'4567'
        branch = get_current_branch(self.store)
        self.create_storable(component.product, branch=branch, stock=1,
                             unit_cost=10)

        editor = ProductionProductEditor(self.store, component.product)
        editor.code.update("12345")
        compslave = editor.component_slave
        compslave.component_combo.select_item_by_data(component.component)
        self.click(compslave.add_button)

        self.assertEqual(run_dialog.call_count, 1)

        self.check_editor(editor, 'editor-product-prod-edit')

    @mock.patch('stoqlib.gui.slaves.productslave.info')
    def test_edit_component_edit_composed(self, info):
        component = self.create_product_component()
        component.component.sellable.code = u'4567'
        branch = get_current_branch(self.store)
        self.create_storable(component.component, branch=branch, stock=1,
                             unit_cost=10)

        editor = ProductionProductEditor(self.store, component.component)
        editor.code.update("12345")
        compslave = editor.component_slave
        compslave.component_combo.select_item_by_data(component.product)
        self.click(compslave.add_button)

        info.assert_called_once_with(
            'You can not add this product as component, '
            'since Description is composed by Description')


class TestProductComponentSlave(GUITest):
    def test_show(self):
        component = self.create_product_component()
        slave = ProductComponentSlave(self.store, component.product)
        self.check_slave(slave, 'slave-production-component-show')


class TestProductStockQuantityEditor(GUITest):

    def test_initial_stock(self):
        branch = get_current_branch(self.store)
        product = self.create_product(branch=branch, storable=False)
        product.manage_stock = False
        editor = ProductStockQuantityEditor(self.store, product, branch)
        self.check_editor(editor, 'editor-product-stock-quantity-initial-show')

        # Update editor
        editor.quantity.update(15)
        editor.cost.update('3.45')

        stock_items_before = self.store.find(ProductStockItem).count()

        # Confirm
        self.click(editor.main_dialog.ok_button)

        # Check data
        stock_items_after = self.store.find(ProductStockItem).count()
        self.assertEqual(stock_items_after, stock_items_before + 1)

        stock_item = product.storable.get_stock_item(branch, batch=None)
        self.assertEqual(stock_item.quantity, 15)
        self.assertEqual(stock_item.stock_cost, Decimal('3.45'))

    def test_inventory(self):
        branch = get_current_branch(self.store)
        product = self.create_product(branch=branch, stock=10)
        editor = ProductStockQuantityEditor(self.store, product, branch)
        self.check_editor(editor, 'editor-product-stock-quantity-inventory-show')

        # Update editor
        editor.quantity.update(20)
        editor.reason.update('test case')

        inventories_before = self.store.find(Inventory).count()

        # Confirm
        self.click(editor.main_dialog.ok_button)

        # Check data
        inventories_after = self.store.find(Inventory).count()
        self.assertEqual(inventories_after, inventories_before + 1)

        stock_item = product.storable.get_stock_item(branch, batch=None)
        self.assertEqual(stock_item.quantity, 20)

        # Check Inventory
        inventory = self.store.find(Inventory).order_by(Inventory.te_id).last()
        # The inventory should have only one item
        item = inventory.get_items().one()

        self.assertEqual(item.recorded_quantity, 10)
        self.assertEqual(item.counted_quantity, 20)
        self.assertEqual(item.actual_quantity, 20)
        self.assertEqual(item.is_adjusted, True)
        self.assertEqual(inventory.status, Inventory.STATUS_CLOSED)

    def test_same_branch(self):
        branch = get_current_branch(self.store)
        product = self.create_product(branch=branch, stock=10)

        editor = ProductStockQuantityEditor(self.store, product, branch)
        # Using set_text because update() will not show the validation
        editor.quantity.set_text('-4')
        editor.reason.update('test')
        # Do not let the user decrease stock to a negative number
        self.assertInvalid(editor, ['quantity'])

        # Let the user decrease stock
        editor.quantity.update(9)
        self.assertValid(editor, ['quantity'])

        # Let the user increase stock
        editor.quantity.update(11)
        self.assertValid(editor, ['quantity'])
        self.click(editor.main_dialog.ok_button)

    def test_other_branch(self):
        other_branch = self.create_branch()
        product = self.create_product(branch=other_branch, stock=10)

        with self.sysparam(SYNCHRONIZED_MODE=True):
            editor = ProductStockQuantityEditor(self.store, product, other_branch)
            editor.quantity.set_text('9')
            # Do not let the user decrease stock from other branches in
            # synchronized mode
            self.assertInvalid(editor, ['quantity'])

            # The user can increase stock from other branches
            editor.quantity.set_text('11')
            editor.reason.update('test')
            self.assertValid(editor, ['quantity'])
            self.click(editor.main_dialog.ok_button)
