# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2005-2007 Async Open Source <http://www.async.com.br>
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
""" Editors definitions for products"""

import collections
from decimal import Decimal

from gi.repository import Gtk
from kiwi.currency import currency
from kiwi.datatypes import ValidationError
from kiwi.python import Settable
from kiwi.ui.forms import MultiLineField, NumericField, PriceField, TextField

from stoqdrivers.enum import TaxType

from stoqlib.api import api
from stoqlib.domain.inventory import Inventory
from stoqlib.domain.person import Branch
from stoqlib.domain.product import (ProductSupplierInfo, Product,
                                    ProductComponent,
                                    ProductQualityTest, Storable,
                                    ProductManufacturer, ProductAttribute)
from stoqlib.domain.sellable import (Sellable,
                                     SellableTaxConstant)
from stoqlib.gui.base.dialogs import run_dialog
from stoqlib.gui.base.messagebar import MessageBar
from stoqlib.gui.editors.baseeditor import BaseEditor
from stoqlib.gui.editors.sellableeditor import SellableEditor
from stoqlib.gui.slaves.imageslave import ImageGallerySlave
from stoqlib.lib.decorators import cached_property
from stoqlib.lib.defaults import quantize, MAX_INT
from stoqlib.lib.message import info
from stoqlib.lib.parameters import sysparam
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext


#
# Slaves
#

class TemporaryProductComponent(object):
    def __init__(self, store, product=None, component=None, quantity=Decimal(1),
                 design_reference=u'', price=Decimal(0)):
        self.product = product
        self.component = component
        self.quantity = quantity
        self.design_reference = design_reference

        if self.component is not None:
            # keep this values in memory in order to speed up the
            # data access
            sellable = self.component.sellable
            self.id = sellable.id
            self.code = sellable.code
            self.description = sellable.get_description()
            self.category = sellable.get_category_description()
            self.unit = sellable.unit_description
            self.production_cost = self.component.get_production_cost()
            product_component = self._get_product_component(store)
            self.price = product_component.price if product_component else price
        else:
            self.price = price

    def _get_product_component(self, store):
        return store.find(ProductComponent,
                          product=self.product, component=self.component).one()

    #
    # Public API
    #

    def get_total_production_cost(self):
        cost = self.price or self.production_cost
        return quantize(cost * self.quantity)

    def delete_product_component(self, store):
        component = self._get_product_component(store)
        if component is not None:
            # FIXME: bug 5581 Check if we can really remove this object when
            # working with synced databases
            store.remove(component)

    def add_or_update_product_component(self, store):
        component = self._get_product_component(store)
        if component is not None:
            # updating
            component.quantity = self.quantity
            component.design_reference = self.design_reference
            component.price = self.price
        else:
            # adding
            ProductComponent(product=self.product,
                             component=self.component,
                             quantity=self.quantity,
                             design_reference=self.design_reference,
                             store=store,
                             price=self.price)

#
#   Quality Test Editor & Slave
#


class QualityTestEditor(BaseEditor):
    model_name = _('Quality Test')
    model_type = ProductQualityTest
    gladefile = 'QualityTestEditor'

    proxy_widgets = ['description', 'test_type']
    confirm_widgets = ['description']

    def __init__(self, store, model=None, product=None):
        self._product = product
        BaseEditor.__init__(self, store=store, model=model)

    def _setup_widgets(self):
        self.sizegroup1.add_widget(self.decimal_value)
        self.sizegroup1.add_widget(self.boolean_value)
        self.test_type.prefill([(value, key)
                                for key, value in ProductQualityTest.types.items()])
        self.boolean_value.prefill([(_('True'), True), (_(('False')), False)])

        # Editing values
        if self.model.test_type == ProductQualityTest.TYPE_BOOLEAN:
            self.boolean_value.select(self.model.get_boolean_value())
        else:
            min_value, max_value = self.model.get_range_value()
            self.min_value.set_value(min_value)
            self.max_value.set_value(max_value)

    def create_model(self, store):
        return ProductQualityTest(product=self._product, store=store)

    def setup_proxies(self):
        self._setup_widgets()
        self.proxy = self.add_proxy(self.model, self.proxy_widgets)

    def on_confirm(self):
        if self.model.test_type == ProductQualityTest.TYPE_BOOLEAN:
            self.model.set_boolean_value(self.boolean_value.read())
        else:
            self.model.set_range_value(self.min_value.read(),
                                       self.max_value.read())

    #
    #   Callbacks
    #

    def on_test_type__changed(self, widget):
        if self.model.test_type == ProductQualityTest.TYPE_BOOLEAN:
            self.boolean_value.show()
            self.decimal_value.hide()
        else:
            self.boolean_value.hide()
            self.decimal_value.show()


#
#   Product Supplier Editor & Slave
#

class ProductSupplierEditor(BaseEditor):
    model_name = _('Product Supplier')
    model_type = ProductSupplierInfo
    gladefile = 'ProductSupplierEditor'

    proxy_widgets = ('base_cost', 'icms', 'notes', 'lead_time',
                     'minimum_purchase', 'supplier_code', 'branch_combo')
    confirm_widgets = ['base_cost', 'icms', 'lead_time', 'minimum_purchase',
                       'supplier_code']

    def _setup_widgets(self):
        unit = self.model.product.sellable.unit
        if unit is None:
            description = _(u'Unit(s)')
        else:
            description = unit.description
        self.unit_label.set_text(description)
        self.base_cost.set_digits(sysparam.get_int('COST_PRECISION_DIGITS'))
        self.base_cost.set_adjustment(
            Gtk.Adjustment(lower=0, upper=MAX_INT, step_increment=1))
        self.minimum_purchase.set_adjustment(
            Gtk.Adjustment(lower=0, upper=MAX_INT, step_increment=1))
        self._setup_branch_combo()

    def _setup_branch_combo(self):
        current_branch = api.get_current_branch(self.store)
        branches = [current_branch]
        user = api.get_current_user(self.store)
        if user.profile.check_app_permission(u'admin'):
            branches.extend(list(Branch.get_active_remote_branches(self.store, current_branch)))
        options = [(branch.get_description(), branch) for branch in branches]
        self.branch_combo.prefill(options)
        self.branch_combo.set_sensitive(False)

        has_generic_active = self.model.product.is_supplied_by(
            self.model.supplier, exclude=self.model, branch=None)
        if self.model.branch is not None or has_generic_active:
            self.branch_checkbutton.set_active(True)
            self.branch_combo.set_sensitive(True)
            if has_generic_active:
                # There is already a generical supplier info, so this must have a
                # specific branch
                self.branch_checkbutton.set_sensitive(False)

    #
    # BaseEditor hooks
    #

    def setup_proxies(self):
        self._setup_widgets()
        self.proxy = self.add_proxy(self.model, self.proxy_widgets)

    def validate_confirm(self):
        return self.base_cost.read() > 0

    #
    # Kiwi handlers
    #

    def on_minimum_purchase__validate(self, entry, value):
        if not value or value <= Decimal(0):
            return ValidationError(_("Minimum purchase must be greater than "
                                     "zero."))

    def on_base_cost__validate(self, entry, value):
        if not value or value <= currency(0):
            return ValidationError(_("Value must be greater than zero."))

    def on_lead_time__validate(self, entry, value):
        if value < 1:
            return ValidationError(_("Lead time must be greater or equal one "
                                     "day"))

    def on_supplier_code__validate(self, entry, value):
        if not value:
            return
        d = {self.model_type.supplier_id: self.model.supplier.id,
             self.model_type.supplier_code: value}

        supplier_info = self.model.check_unique_tuple_exists(d)
        if supplier_info is not None:
            desc = supplier_info.product.sellable.description
            return ValidationError(
                _("This code already exists for this supplier "
                  "on product '%s'") % (desc, ))

    def on_branch_combo__validate(self, entry, value):
        if self.model.product.is_supplied_by(self.model.supplier, branch=value,
                                             exclude=self.model):
            return ValidationError(
                _("The product is already supplied in this branch"))

    def on_branch_checkbutton__toggled(self, check):
        active = check.get_active()
        self.branch_combo.set_sensitive(active)
        if active is False:
            self.model.branch = None
            self.proxy.update('branch')

#
# Editors
#


class ProductComponentEditor(BaseEditor):
    gladefile = 'ProductComponentEditor'
    proxy_widgets = ['quantity', 'design_reference', 'price']
    title = _(u'Product Component')
    model_type = TemporaryProductComponent

    def _setup_widgets(self):
        self.price.hide()
        self.price_lbl.hide()
        self.component_description.set_text(self.model.description)
        self.quantity.set_adjustment(
            Gtk.Adjustment(lower=0, upper=MAX_INT, step_increment=1,
                           page_increment=10))
        self.price.set_adjustment(
            Gtk.Adjustment(lower=0, upper=MAX_INT, step_increment=1,
                           page_increment=10))
        # set a default quantity value for new components
        if not self.model.quantity:
            self.quantity.set_value(1)

    #
    # BaseEditor
    #

    def setup_proxies(self):
        self._setup_widgets()
        self.proxy = self.add_proxy(
            self.model, ProductComponentEditor.proxy_widgets)

    def validate_confirm(self):
        return self.quantity.read() > 0

    #
    # Kiwi Callbacks
    #

    def on_quantity__validate(self, widget, value):
        if not value > 0:
            # FIXME: value < upper bound
            return ValidationError(_(u'The component quantity must be '
                                     'greater than zero.'))


class ProductPackageComponentEditor(ProductComponentEditor):
    confirm_widgets = ['price']

    def setup_proxies(self):
        super(ProductPackageComponentEditor, self).setup_proxies()
        self.design_reference.hide()
        self.design_reference_lbl.hide()
        self.price.show()
        self.price_lbl.show()

    #
    # Kiwi Callbacks
    #

    def on_price__validate(self, widget, value):
        if value <= 0:
            return ValidationError(_("The price must be greater than zero."))


class ProductEditor(SellableEditor):
    model_name = _('Product')
    model_type = Product
    help_section = 'product'
    ui_form_name = u'product'
    product_widgets = ['product_type_str']
    proxy_widgets = SellableEditor.proxy_widgets + product_widgets

    def __init__(self, store, model=None, visual_mode=False,
                 product_type=Product.TYPE_COMMON, template=None, wizard=None):
        """
        :param product_type: one of the available
            :attr:`stoqlib.domain.product.Product.product_types` that
            will be used when creating a new one
        :param template: a product to use as a template when creating
            a new one. Some properties will be copied from it.
        """
        self._template = template
        self._product_type = product_type
        self._wizard = wizard
        SellableEditor.__init__(self, store, model, visual_mode=visual_mode)
        # This can't be done in setup_slaves() as we need to access
        # self.main_dialog when setting up the quality test slave
        self._add_extra_tabs()

    #
    # Private
    #

    def _add_infobar(self, message, message_type):
        infobar = MessageBar(message, message_type)
        infobar.show()

        self.main_box.pack_start(infobar, False, False, 0)
        self.main_box.reorder_child(infobar, 0)

        return infobar

    def _add_extra_tabs(self):
        for tabname, tabslave in self.get_extra_tabs():
            self.add_extra_tab(tabname, tabslave)

    def _disable_child_widgets(self):
        """This method disables edition of attributes gotten from parent.
        """
        widgets = [self.description, self.category_combo, self.cost, self.price,
                   self.default_sale_cfop, self.unit_combo, self.tax_constant,
                   self.add_category]
        for widget in widgets:
            widget.set_property('sensitive', False)

    #
    #  SellableEditor
    #

    def get_taxes(self):
        query = (SellableTaxConstant.tax_type != int(TaxType.SERVICE))
        constants = self.store.find(
            SellableTaxConstant, query).order_by(SellableTaxConstant.description)
        return [(c.description, c) for c in constants]

    def setup_slaves(self):
        super(ProductEditor, self).setup_slaves()

        from stoqlib.gui.slaves.productslave import ProductInformationSlave
        info_slave = ProductInformationSlave(self.store, self.model, self.db_form,
                                             visual_mode=self.visual_mode)

        self.add_extra_tab(_(u'Details'), info_slave)

    def setup_proxies(self):
        super(ProductEditor, self).setup_proxies()

        self.add_proxy(self.model, self.product_widgets)

        if self.model.parent is not None:
            self._disable_child_widgets()
            msg = (_("Some properties of this product have been disabled for "
                     "editing as that should be done on the parent product."))
            self._add_infobar(msg, Gtk.MessageType.INFO)
        elif self.model.product_type == Product.TYPE_GRID:
            msg = (_("This is just a skeleton product responsible for "
                     "creating grid products. Create those on the 'Grid' tab"))
            self._add_infobar(msg, Gtk.MessageType.INFO)
        if self.model.product_type == Product.TYPE_PACKAGE:
            # We are building its sale price on Pack content tab, so disable
            # this the widget and set a simbolic value
            self.price.set_property('sensitive', False)
            # FIXME Disable promotional price for now
            self.sale_price_button.set_property('sensitive', False)
            msg = (_("The price of this product consists of the sum of "
                     "its components price on 'Pack content' tab"))
            self._add_infobar(msg, Gtk.MessageType.INFO)

    def get_extra_tabs(self):
        from stoqlib.gui.slaves.productslave import (ProductTaxSlave,
                                                     ProductSupplierSlave,
                                                     ProductGridSlave,
                                                     ProductPackageSlave)
        extra_tabs = []

        suppliers_slave = ProductSupplierSlave(self.store, self.model,
                                               self.visual_mode)
        extra_tabs.append((_(u'Suppliers'), suppliers_slave))

        tax_slave = ProductTaxSlave(self.store, self.model, self.visual_mode)
        extra_tabs.append((_(u'Taxes'), tax_slave))

        if self.model.product_type == Product.TYPE_GRID:
            # If there is a wizard, it means we are creating a new product.
            # Store the selected attributes in the database
            if self._wizard:
                for attribute in self._wizard.attr_list:
                    ProductAttribute(store=self.store,
                                     product_id=self.model.id,
                                     attribute_id=attribute.id)

            attribute_option_slave = ProductGridSlave(self.store, self.model,
                                                      self.visual_mode)
            extra_tabs.append((_(u'Grid'), attribute_option_slave))
            attribute_option_slave.grid_tab_alignment.connect('focus',
                                                              self._on_grid_tab_alignment__focus)
        elif self.model.product_type == Product.TYPE_PACKAGE:
            self.package_slave = ProductPackageSlave(self.store, self.model,
                                                     visual_mode=self.visual_mode)
            extra_tabs.append((_(u'Pack content'), self.package_slave))

        return extra_tabs

    def setup_widgets(self):
        self.cost.set_digits(sysparam.get_int('COST_PRECISION_DIGITS'))
        self.description.grab_focus()

    def create_model(self, store):
        self._model_created = True
        sellable = Sellable(store=store)
        model = Product(store=store, sellable=sellable)
        no_storable = [Product.TYPE_WITHOUT_STOCK, Product.TYPE_PACKAGE]
        if not self._product_type in no_storable:
            storable = Storable(product=model, store=store)

        if self._product_type == Product.TYPE_BATCH:
            storable.is_batch = True
        elif self._product_type == Product.TYPE_WITHOUT_STOCK:
            model.manage_stock = False
        elif self._product_type == Product.TYPE_CONSIGNED:
            model.consignment = True
        elif self._product_type == Product.TYPE_GRID:
            model.is_grid = True
            # Configurable products should not manage stock
            model.manage_stock = False
        elif self._product_type == Product.TYPE_PACKAGE:
            model.is_package = True
            # Package products should not manage stock
            model.manage_stock = False

        if self._template is not None:
            sellable.tax_constant = self._template.sellable.tax_constant
            sellable.unit = self._template.sellable.unit
            sellable.category = self._template.sellable.category
            sellable.base_price = self._template.sellable.base_price
            sellable.cost = self._template.sellable.cost
            sellable.default_sale_cfop = self._template.sellable.default_sale_cfop

            model.manufacturer = self._template.manufacturer
            model.brand = self._template.brand
            model.model = self._template.model
            model.family = self._template.family
            model.ncm = self._template.ncm
            model.set_icms_template(self._template._icms_template)
            model.set_ipi_template(self._template._ipi_template)
            model.set_pis_template(self._template._pis_template)
            model.set_cofins_template(self._template._cofins_template)

            for product_attr in self._template.attributes:
                ProductAttribute(store=self.store,
                                 product_id=model.id,
                                 attribute_id=product_attr.attribute.id)
            for supplier_info in self._template.suppliers:
                ProductSupplierInfo(
                    store=self.store,
                    product=model,
                    supplier=supplier_info.supplier)
        else:
            sellable.tax_constant = sysparam.get_object(self.store,
                                                        'DEFAULT_PRODUCT_TAX_CONSTANT')
            sellable.unit_id = sysparam.get_object_id('SUGGESTED_UNIT')

        return model

    def on_confirm(self):
        # The user choose not to manage stock for this product, so we must
        # remove the storable.
        if not self.model.manage_stock and self.model.storable:
            self.store.remove(self.model.storable)

        # When creating a purchase, we use the supplier cost instead of the one
        # in the sellable. If there is only one supplier for this product, also
        # update its cost. TODO: What should we do when there is more than one
        # supplier?
        infos = list(self.model.get_suppliers_info())
        if len(infos) == 1:
            infos[0].base_cost = self.model.sellable.cost

        if self.model.is_grid and self.has_changes():
            self.model.update_children_info()

    #
    #   Callbacks
    #

    def _on_grid_tab_alignment__focus(self, widget, value):
        self.model.update_children_description()


class ProductionProductEditor(ProductEditor):

    _cost_msg = _(u'Cost must be greater than the sum of the components.')

    def _is_valid_cost(self, cost):
        if hasattr(self, '_component_slave'):
            component_cost = self.component_slave.get_component_cost()
            return cost >= component_cost
        return True

    def create_model(self, store):
        model = ProductEditor.create_model(self, store)
        model.is_composed = True
        return model

    def get_extra_tabs(self):
        from stoqlib.gui.slaves.productslave import (ProductTaxSlave,
                                                     ProductComponentSlave,
                                                     ProductQualityTestSlave)
        self.component_slave = ProductComponentSlave(self.store, self.model,
                                                     self.visual_mode)
        tax_slave = ProductTaxSlave(self.store, self.model, self.visual_mode)
        quality_slave = ProductQualityTestSlave(self, self.store, self.model,
                                                self.visual_mode)
        return [(_(u'Components'), self.component_slave),
                (_(u'Taxes'), tax_slave),
                (_(u'Quality'), quality_slave),
                ]

    def setup_widgets(self):
        super(ProductionProductEditor, self).setup_widgets()
        self.cost.set_sensitive(not sysparam.get_bool('UPDATE_PRODUCT_COST_ON_COMPONENT_UPDATE'))

    def validate_confirm(self):
        if not self._is_valid_cost(self.cost.read()):
            info(self._cost_msg)
            return False
        return True

    def on_component_slave__cost_updated(self, slave, cost):
        if sysparam.get_bool('UPDATE_PRODUCT_COST_ON_COMPONENT_UPDATE'):
            # We have to update the sellable directly since kiwi won't do it for
            # us, since the widget is insensitive
            self.model.sellable.cost = cost
            self.sellable_proxy.update('cost')

    def on_cost__validate(self, widget, value):
        if value <= 0:
            return ValidationError(_(u'Cost cannot be zero or negative.'))
        if not self._is_valid_cost(value):
            return ValidationError(self._cost_msg)


class ProductStockEditor(BaseEditor):
    """This is a product editor limitted to editing physical stock information"""
    model_name = _('Product')
    model_type = Product
    gladefile = 'ProductStockEditor'

    def setup_slaves(self):
        from stoqlib.gui.slaves.productslave import ProductInformationSlave
        info_slave = ProductInformationSlave(self.store, self.model,
                                             visual_mode=self.visual_mode)
        info_slave.nfe_frame.hide()
        self.attach_slave('information_holder', info_slave)

        from stoqlib.gui.slaves.sellableslave import SellableDetailsSlave
        details_slave = SellableDetailsSlave(self.store, self.model.sellable,
                                             visual_mode=self.visual_mode)
        self.attach_slave('details_holder', details_slave)

        # Make everything aligned by pytting notes_lbl on the same size group
        info_slave.left_labels_group.add_widget(details_slave.notes_lbl)

        event_box = Gtk.EventBox()
        event_box.show()
        image_gallery_slave = ImageGallerySlave(
            self.store, self.model.sellable, self.visual_mode)
        self.notebook.append_page(event_box, Gtk.Label(label=_("Images")))
        self.attach_slave('images', image_gallery_slave, event_box)


class ProductStockQuantityEditor(BaseEditor):
    """Editor for adjusting the stock quantity of a product

    This editor will set the quantity of a product for a given branch. If the
    product does not manage stock yet, a storable will be created first and the
    initial stock be registred.

    If the product is already a storable, an inventory will be created for just
    this product (so that the original quantity is registred and can be
    audited), and the quantity will be adjusted. A reason in this case is
    mandatory
    """
    title = _('Adjust stock quantity')
    model_name = _('Stock')
    model_type = Settable

    @cached_property()
    def fields(self):
        # Check if sellable's unit allow fraction to use decimal places
        unit = self._product.sellable.unit
        if unit and unit.allow_fraction:
            quantity_digits = 3
        else:
            quantity_digits = 0

        fields = collections.OrderedDict(
            quantity=NumericField(_('Quantity'), proxy=True, mandatory=True,
                                  digits=quantity_digits),
        )
        # When creating an inventory, a reason is necessary
        if self._stock_item:
            fields['reason'] = MultiLineField(_('Reason'), proxy=True, mandatory=True)
        else:
            # Inventories dont do anything with the cost yet. Maybe we should
            # fix that
            fields['cost'] = PriceField(_('Cost'), proxy=True, mandatory=True)
        return fields

    def __init__(self, store, model, branch):
        self._branch = branch
        assert self._branch
        self._product = model
        # model here is the product, but we will create a settable later
        if model.storable:
            # We dont support editing batch products yet.
            assert not model.storable.is_batch
            self._stock_item = model.storable.get_stock_item(branch, batch=None)
        else:
            self._stock_item = None

        BaseEditor.__init__(self, store=store)

    def create_model(self, store):
        if self._stock_item:
            return Settable(quantity=self._stock_item.quantity,
                            cost=self._stock_item.stock_cost, reason=u'')
        else:
            return Settable(quantity=Decimal(0), cost=self._product.sellable.cost)

    def _register_inventory(self):
        query = Storable.id == self._product.id
        inventory = Inventory.create_inventory(self.store, branch=self._branch,
                                               station=api.get_current_station(self.store),
                                               responsible=api.get_current_user(self.store),
                                               query=query)
        # At this point, the inventory should have only one item.
        item = inventory.get_items().one()
        item.counted_quantity = item.actual_quantity = self.model.quantity
        # item.product_cost = self.model.cost
        item.reason = self.model.reason
        item.adjust(user=api.get_current_user(self.store), invoice_number=None)
        inventory.close()

    def _register_initial_stock(self):
        if not self._product.storable:
            self._product.set_as_storable_product(self._branch, api.get_current_user(self.store),
                                                  self.model.quantity, self.model.cost)
        elif self.model.quantity:
            self._product.storable.register_initial_stock(self.model.quantity,
                                                          self._branch,
                                                          self.model.cost,
                                                          api.get_current_user(self.store))

    def on_confirm(self):
        if not self._stock_item:
            # If the item does not manage stock, we will make it a managed
            # storable and register the initial stock
            return self._register_initial_stock()
        else:
            # If the product already manages stock, this will be an easy way for
            # the user to fix the actual quantity (like a mini inventory).
            # XXX: Make sure that the user has access to the inventory app
            # before calling this.
            return self._register_inventory()

    #
    # Kiwi Callbacks
    #

    def on_quantity__validate(self, widget, new_quantity):
        # Never let the user set negative values
        if new_quantity < 0:
            return ValidationError(_("This value cannot be negative"))

        # In Synchronized mode dont let the user decrease the stock from other
        # branches
        if (api.sysparam.get_bool('SYNCHRONIZED_MODE')
                and self._branch != api.get_current_branch(self.store)
                and new_quantity < self.model.quantity):
            return ValidationError(_("You cannot decrease stock from other "
                                     "branches"))


class ProductManufacturerEditor(BaseEditor):
    model_name = _('Manufacturer')
    model_type = ProductManufacturer
    confirm_widgets = ['name']

    @cached_property()
    def fields(self):
        return collections.OrderedDict(
            name=TextField(_('Name'), proxy=True, mandatory=True),
            code=TextField(_('Code'), proxy=True),
        )

    def create_model(self, store):
        return ProductManufacturer(name=u'', store=store)

    def setup_proxies(self):
        self.name.grab_focus()

    #
    # Kiwi Callbacks
    #

    def on_name__validate(self, widget, new_name):
        if not new_name:
            return ValidationError(
                _("The manufacturer should have a name."))
        if self.model.check_unique_value_exists(ProductManufacturer.name,
                                                new_name):
            return ValidationError(
                _("The manufacturer '%s' already exists.") % new_name)

    def on_code__validate(self, widget, new_code):
        if self.model.check_unique_value_exists(ProductManufacturer.code,
                                                new_code):
            return ValidationError(_("The code '%s' already exists") % new_code)


def test_product():  # pragma nocover
    ec = api.prepare_test()
    product = ec.create_product()
    run_dialog(ProductEditor,
               parent=None, store=ec.store, model=product)


if __name__ == '__main__':  # pragma nocover
    test_product()
