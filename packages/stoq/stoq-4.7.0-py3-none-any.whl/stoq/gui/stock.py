# -*- Mode: Python; coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2005-2015 Async Open Source <http://www.async.com.br>
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
""" Main gui definition for stock application.  """

import logging

from gi.repository import Gtk, GdkPixbuf, Pango, GLib
from kiwi.datatypes import converter

from stoqlib.api import api
from stoqlib.enums import SearchFilterPosition
from stoqlib.domain.image import Image
from stoqlib.domain.person import Branch
from stoqlib.domain.views import ProductFullStockView
from stoqlib.domain.transfer import TransferOrder
from stoqlib.domain.returnedsale import ReturnedSale
from stoqlib.lib.defaults import sort_sellable_code
from stoqlib.lib.imageutils import get_thumbnail
from stoqlib.lib.message import warning
from stoqlib.lib.translation import stoqlib_ngettext, stoqlib_gettext as _
from stoqlib.gui.dialogs.initialstockdialog import InitialStockDialog
from stoqlib.gui.dialogs.labeldialog import PrintLabelEditor
from stoqlib.gui.dialogs.productstockdetails import ProductStockHistoryDialog
from stoqlib.gui.dialogs.sellableimage import SellableImageViewer
from stoqlib.gui.editors.producteditor import (ProductStockEditor,
                                               ProductStockQuantityEditor)
from stoqlib.gui.search.loansearch import LoanItemSearch, LoanSearch
from stoqlib.gui.search.receivingsearch import PurchaseReceivingSearch
from stoqlib.gui.search.returnedsalesearch import (PendingReturnedSaleSearch,
                                                   ReturnedItemSearch)
from stoqlib.gui.search.productsearch import (ProductSearchQuantity,
                                              ProductStockSearch,
                                              ProductBrandSearch,
                                              ProductBrandByBranchSearch,
                                              ProductBatchSearch,
                                              ProductClosedStockSearch)
from stoqlib.gui.search.purchasesearch import PurchasedItemsSearch
from stoqlib.gui.search.transfersearch import (TransferOrderSearch,
                                               TransferItemSearch)
from stoqlib.gui.search.searchcolumns import SearchColumn, QuantityColumn
from stoqlib.gui.search.searchfilters import ComboSearchFilter
from stoqlib.gui.search.stockdecreasesearch import StockDecreaseSearch
from stoqlib.gui.utils.keybindings import get_accels
from stoqlib.gui.utils.printing import print_labels
from stoqlib.gui.wizards.loanwizard import NewLoanWizard, CloseLoanWizard
from stoqlib.gui.wizards.receivingwizard import ReceivingOrderWizard
from stoqlib.gui.wizards.stockdecreasewizard import StockDecreaseWizard
from stoqlib.gui.wizards.stocktransferwizard import StockTransferWizard
from stoqlib.reporting.product import SimpleProductReport

from stoq.gui.shell.shellapp import ShellApp

log = logging.getLogger(__name__)


class StockApp(ShellApp):
    app_title = _('Stock')
    gladefile = "stock"
    search_spec = ProductFullStockView
    search_labels = _('Matching:')
    report_table = SimpleProductReport
    pixbuf_converter = converter.get_converter(GdkPixbuf.Pixbuf)

    #
    # Application
    #

    def create_actions(self):
        group = get_accels('app.stock')
        actions = [
            ("NewReceiving", None, _("Order _receival..."),
             group.get('new_receiving')),
            ('NewTransfer', Gtk.STOCK_CONVERT, _('Transfer...'),
             group.get('transfer_product')),
            ('NewStockDecrease', None, _('Stock decrease...'),
             group.get('stock_decrease')),
            ('StockInitial', Gtk.STOCK_GO_UP, _('Register initial stock...')),
            ("LoanNew", None, _("Loan...")),
            ("LoanClose", None, _("Close loan...")),
            ("SearchPurchaseReceiving", None, _("Received purchases..."),
             group.get('search_receiving'),
             _("Search for received purchase orders")),
            ("SearchProductHistory", None, _("Product history..."),
             group.get('search_product_history'),
             _("Search for product history")),
            ("SearchStockDecrease", None, _("Stock decreases..."), '',
             _("Search for manual stock decreases")),
            ("SearchPurchasedStockItems", None, _("Purchased items..."),
             group.get('search_purchased_stock_items'),
             _("Search for purchased items")),
            ("SearchBrandItems", None, _("Brand items..."),
             group.get('search_brand_items'),
             _("Search for brand items on stock")),
            ("SearchBrandItemsByBranch", None, _("Brand item by branch..."),
             group.get('search_brand_by_branch'),
             _("Search for brand items by branch on stock")),
            ("SearchBatchItems", None, _("Batch items..."),
             group.get('search_batch_items'),
             _("Search for batch items on stock")),
            ("SearchStockItems", None, _("Stock items..."),
             group.get('search_stock_items'),
             _("Search for items on stock")),
            ("SearchTransfer", None, _("Transfers..."),
             group.get('search_transfers'),
             _("Search for stock transfers")),
            ("SearchClosedStockItems", None, _("Closed stock Items..."),
             group.get('search_closed_stock_items'),
             _("Search for closed stock items")),
            ("LoanSearch", None, _("Loans...")),
            ("LoanSearchItems", None, _("Loan items...")),
            ("SearchTransferItems", None, _("Transfer items...")),
            ("SearchReturnedItems", None, _("Returned items...")),
            ("SearchPendingReturnedSales", None, _("Pending returned sales...")),
            ("ProductMenu", None, _("Product")),
            ("PrintLabels", None, _("Print labels...")),
            ("ManageStock", None, _("Manage stock...")),

            ("ProductStockHistory", Gtk.STOCK_INFO, _("History..."),
             group.get('history'),
             _('Show the stock history of the selected product')),
            ("EditProduct", Gtk.STOCK_EDIT, _("Edit..."),
             group.get('edit_product'),
             _("Edit the selected product, allowing you to change it's "
               "details")),
        ]
        self.stock_ui = self.add_ui_actions(actions)

        toggle_actions = [
            ('StockPictureViewer', None, _('Picture viewer'),
             group.get('toggle_picture_viewer')),
        ]
        self.add_ui_actions(toggle_actions, 'ToggleActions')
        self.set_help_section(_("Stock help"), 'app-stock')

    def create_ui(self):
        if api.sysparam.get_bool('SMART_LIST_LOADING'):
            self.search.enable_lazy_search()

        self.window.add_print_items([self.PrintLabels])
        self.window.add_export_items()
        self.window.add_extra_items([self.StockInitial, self.LoanClose,
                                     self.StockPictureViewer])
        self.window.add_new_items([self.NewReceiving, self.NewTransfer,
                                   self.NewStockDecrease, self.LoanNew])
        self.window.add_search_items([
            self.SearchPurchaseReceiving,
            self.SearchProductHistory,
            self.SearchTransfer,
            self.SearchTransferItems,
            self.SearchStockDecrease,
            self.SearchReturnedItems,
            self.SearchPurchasedStockItems,
            self.SearchStockItems,
            self.SearchBrandItems,
            self.SearchBrandItemsByBranch,
            self.SearchBatchItems,
            self.SearchClosedStockItems,
            self.SearchPendingReturnedSales,
            # Separator
            self.LoanSearch,
            self.LoanSearchItems,

        ])
        self._inventory_widgets = [self.NewTransfer, self.NewReceiving,
                                   self.StockInitial, self.NewStockDecrease,
                                   self.LoanNew, self.LoanClose]
        self.register_sensitive_group(self._inventory_widgets,
                                      lambda: not self.has_open_inventory())

        self.image_viewer = None

        self.image = Gtk.Image()
        # FIXME: How are we goint to display an image preview?
        #self.edit_button = self.uimanager.get_widget('/toolbar/AppToolbarPH/EditProduct')
        #self.edit_button.set_icon_widget(self.image)
        self.image.show()

        self.search.set_summary_label(column='stock',
                                      label=_('<b>Stock Total:</b>'),
                                      format='<b>%s</b>',
                                      parent=self.get_statusbar_message_area())

    def get_domain_options(self):
        options = [
            ('fa-info-circle-symbolic', _('History'), 'stock.ProductStockHistory', True),
            ('fa-edit-symbolic', _('Edit'), 'stock.EditProduct', True),
            ('', _('Print labels'), 'stock.PrintLabels', False),
            ('', _('Manage stock'), 'stock.ManageStock', False),
        ]

        return options

    def activate(self, refresh=True):
        if refresh:
            self.refresh()

        open_inventory = self.check_open_inventory()

        if not open_inventory:
            self.transfers_bar = self._create_pending_info_message()
            self.returned_bar = self._create_pending_returned_sale_message()
        else:
            self.transfers_bar = None
            self.returned_bar = None

        self._update_widgets()

        self.search.focus_search_entry()

    def deactivate(self):
        if self.transfers_bar:
            self.transfers_bar.hide()
        if self.returned_bar:
            self.returned_bar.hide()

        self._close_image_viewer()

    def set_open_inventory(self):
        self.set_sensitive(self._inventory_widgets, False)

    def create_filters(self):
        self.search.set_query(self._query)
        self.set_text_field_columns(['description', 'code', 'barcode',
                                     'category_description', 'manufacturer'])
        branches = Branch.get_active_branches(self.store)
        self.branch_filter = ComboSearchFilter(
            _('Show by:'), api.for_combo(branches, empty=_("All branches")))
        self.branch_filter.select(api.get_current_branch(self.store))
        self.add_filter(self.branch_filter, position=SearchFilterPosition.TOP)

    def get_columns(self):
        return [SearchColumn('code', title=_('Code'), sorted=True,
                             sort_func=sort_sellable_code,
                             data_type=str, width=130),
                SearchColumn('barcode', title=_("Barcode"), data_type=str,
                             width=130),
                SearchColumn('category_description', title=_("Category"),
                             data_type=str, width=100, visible=False),
                SearchColumn('description', title=_("Description"),
                             data_type=str, expand=True,
                             ellipsize=Pango.EllipsizeMode.END),
                SearchColumn('manufacturer', title=_("Manufacturer"),
                             data_type=str, visible=False),
                SearchColumn('brand', title=_("Brand"),
                             data_type=str, visible=False),
                SearchColumn('model', title=_("Model"),
                             data_type=str, visible=False),
                SearchColumn('location', title=_("Location"), data_type=str,
                             width=100, visible=False),
                QuantityColumn('stock', title=_('Quantity'), width=100,
                               use_having=True),
                SearchColumn('has_image', title=_('Picture'),
                             data_type=bool, width=80),
                ]

    #
    # Private API
    #

    def _open_image_viewer(self):
        assert self.image_viewer is None

        self.image_viewer = SellableImageViewer(size=(325, 325))
        self.image_viewer.toplevel.connect(
            'delete-event', self.on_image_viewer_closed)
        self.image_viewer.show_all()

        self._update_widgets()

    def _close_image_viewer(self):
        if self.image_viewer is None:
            return

        self.image_viewer.destroy()
        self.image_viewer = None

    def _query(self, store):
        branch = self.branch_filter.get_state().value
        return self.search_spec.find_by_branch(store, branch)

    def _update_widgets(self):
        branch = api.get_current_branch(self.store)

        is_main_branch = self.branch_filter.get_state().value is branch
        item = self.results.get_selected()

        sellable = item and item.product.sellable
        if sellable:
            if item.has_image:
                # XXX:Workaround for a bug caused by the image domain refactoring
                # which left some existent thumbnail as None
                thumbnail = sellable.image.thumbnail
                if thumbnail is None:
                    # Create new store to create the thumbnail
                    with api.new_store() as new_store:
                        image = sellable.image
                        image = new_store.fetch(image)
                        size = (Image.THUMBNAIL_SIZE_WIDTH, Image.THUMBNAIL_SIZE_HEIGHT)
                        image.thumbnail = get_thumbnail(image.image, size)
                        thumbnail = image.thumbnail
                pixbuf = self.pixbuf_converter.from_string(thumbnail)
            else:
                pixbuf = None

            self._update_edit_image(pixbuf)
            if self.image_viewer:
                self.image_viewer.set_sellable(sellable)
        else:
            self._update_edit_image()

        # Always let the user choose the manage stock option and do a proper
        # check there (showing a warning if he can't)
        self.set_sensitive([self.ManageStock], bool(item))
        self.set_sensitive([self.EditProduct, self.PrintLabels], bool(item))
        self.set_sensitive([self.ProductStockHistory],
                           bool(item) and is_main_branch)
        # We need more than one branch to be able to do transfers
        # Note that 'all branches' is not a real branch
        has_branches = len(self.branch_filter.combo) > 2

        transfer_active = self.NewTransfer.get_enabled()
        self.set_sensitive([self.NewTransfer],
                           transfer_active and has_branches)
        # Building a list of searches that we must disable if there is no
        # branches other than the main company
        searches = [self.SearchTransfer, self.SearchTransferItems,
                    self.SearchPendingReturnedSales]
        self.set_sensitive(searches, has_branches)

    def _update_edit_image(self, pixbuf=None):
        if not pixbuf:
            self.image.set_from_stock(Gtk.STOCK_EDIT,
                                      Gtk.IconSize.LARGE_TOOLBAR)
            return

        # FIXME: get this icon size from settings
        icon_size = 24
        pixbuf = pixbuf.scale_simple(icon_size, icon_size,
                                     GdkPixbuf.InterpType.BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def _update_filter_slave(self, slave):
        self.refresh()

    def _transfer_stock(self):
        if self.check_open_inventory():
            return
        store = api.new_store()
        model = self.run_dialog(StockTransferWizard, store)
        store.confirm(model)
        store.close()
        self.refresh()

    def _receive_purchase(self):
        if self.check_open_inventory():
            return
        store = api.new_store()
        model = self.run_dialog(ReceivingOrderWizard, store)
        store.confirm(model)
        store.close()
        self.refresh()

    def _create_pending_info_message(self):
        branch = api.get_current_branch(self.store)
        n_transfers = TransferOrder.get_pending_transfers(self.store, branch).count()

        if not n_transfers:
            return None

        msg = stoqlib_ngettext(_(u"You have %s incoming transfer"),
                               _(u"You have %s incoming transfers"),
                               n_transfers) % n_transfers
        info_bar = self.window.add_info_bar(Gtk.MessageType.QUESTION, msg)
        button = info_bar.add_button(_(u"Receive"), Gtk.ResponseType.OK)
        button.connect('clicked', self._on_info_transfers__clicked)

        return info_bar

    def _create_pending_returned_sale_message(self):
        branch = api.get_current_branch(self.store)
        n_returned = ReturnedSale.get_pending_returned_sales(self.store, branch).count()

        if not n_returned:
            return None

        msg = stoqlib_ngettext(_(u"You have %s returned sale to receive"),
                               _(u"You have %s returned sales to receive"),
                               n_returned) % n_returned
        info_returned_bar = self.window.add_info_bar(Gtk.MessageType.QUESTION, msg)
        button = info_returned_bar.add_button(_(u"Returned sale"), Gtk.ResponseType.OK)
        button.connect('clicked', self._on_info_returned_sales__clicked)

        return info_returned_bar

    def _search_transfers(self):
        branch = api.get_current_branch(self.store)
        self.run_dialog(TransferOrderSearch, self.store)

        # After the search is closed we may want to update , or even hide the
        # message, if there is no pending transfer to receive
        if self.transfers_bar:
            n_transfers = TransferOrder.get_pending_transfers(self.store, branch).count()

            if n_transfers > 0:
                msg = stoqlib_ngettext(_(u"You have %s incoming transfer"),
                                       _(u"You have %s incoming transfers"),
                                       n_transfers) % n_transfers
                self.transfers_bar.set_message(msg)
            else:
                self.transfers_bar.hide()
        self.refresh()

    def _search_pending_returned_sales(self):
        with api.new_store() as store:
            self.run_dialog(PendingReturnedSaleSearch, store)

        branch = api.get_current_branch(self.store)
        # After the search is closed we may want to update , or even hide the
        # message, if there is no pending returned sale to receive
        if self.returned_bar:
            n_returned = ReturnedSale.get_pending_returned_sales(self.store, branch).count()

            if n_returned > 0:
                msg = stoqlib_ngettext(_(u"You have %s returned sale to receive"),
                                       _(u"You have %s returned sales to receive"),
                                       n_returned) % n_returned
                self.returned_bar.set_message(msg)
            else:
                self.returned_bar.hide()
        self.refresh()

    #
    # Callbacks
    #

    def on_image_viewer_closed(self, window, event):
        self.image_viewer = None
        self.StockPictureViewer.set_state(GLib.Variant.new_boolean(False))

    def on_results__has_rows(self, results, product):
        self._update_widgets()

    def on_results__selection_changed(self, results, product):
        self._update_widgets()

    def on_ProductStockHistory__activate(self, button):
        selected = self.results.get_selected()
        sellable = selected.sellable
        self.run_dialog(ProductStockHistoryDialog, self.store, sellable,
                        branch=self.branch_filter.combo.get_selected())

    def on_ManageStock__activate(self, action):
        user = api.get_current_user(self.store)
        if not user.profile.check_app_permission(u'inventory'):
            return warning(_('Only users with access to the inventory app can'
                             ' change the stock quantity'))

        product = self.results.get_selected().product
        if product.is_grid:
            return warning(_("Can't change stock quantity of a grid parent"))

        if product.storable and product.storable.is_batch:
            return warning(_("It's not possible to change the stock quantity of"
                             " a batch product"))

        branch = self.branch_filter.combo.get_selected()
        if not branch:
            return warning(_('You must select a branch first'))

        with api.new_store() as store:
            self.run_dialog(ProductStockQuantityEditor, store,
                            store.fetch(product), branch=branch)

        if store.committed:
            self.refresh()

    def on_PrintLabels__activate(self, button):
        selected = self.results.get_selected()
        sellable = selected.sellable
        label_data = self.run_dialog(PrintLabelEditor, None, self.store,
                                     sellable)
        if label_data:
            print_labels(label_data, self.store)

    def on_EditProduct__activate(self, button):
        selected = self.results.get_selected()
        assert selected

        store = api.new_store()
        product = store.fetch(selected.product)

        model = self.run_dialog(ProductStockEditor, store, product)
        store.confirm(model)
        store.close()
        if model:
            self.refresh()

    def _on_info_transfers__clicked(self, button):
        self._search_transfers()

    def _on_info_returned_sales__clicked(self, button):
        self._search_pending_returned_sales()

    # Stock

    def on_NewReceiving__activate(self, button):
        self._receive_purchase()

    def on_NewTransfer__activate(self, button):
        self._transfer_stock()

    def on_NewStockDecrease__activate(self, action):
        if self.check_open_inventory():
            return
        store = api.new_store()
        model = self.run_dialog(StockDecreaseWizard, store)
        store.confirm(model)
        store.close()
        self.refresh()

    def on_StockInitial__activate(self, action):
        if self.check_open_inventory():
            return

        with api.new_store() as store:
            self.run_dialog(InitialStockDialog, store)

        if store.committed:
            self.refresh()

    def on_StockPictureViewer__change_state(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self._open_image_viewer()
        else:
            self._close_image_viewer()

    # Loan

    def on_LoanNew__activate(self, action):
        if self.check_open_inventory():
            return
        store = api.new_store()
        model = self.run_dialog(NewLoanWizard, store)
        store.confirm(model)
        store.close()
        self.refresh()

    def on_LoanClose__activate(self, action):
        if self.check_open_inventory():
            return
        store = api.new_store()
        model = self.run_dialog(CloseLoanWizard, store)
        store.confirm(model)
        store.close()
        self.refresh()

    def on_LoanSearch__activate(self, action):
        self.run_dialog(LoanSearch, self.store)

    def on_LoanSearchItems__activate(self, action):
        self.run_dialog(LoanItemSearch, self.store)

    # Search

    def on_SearchPurchaseReceiving__activate(self, button):
        self.run_dialog(PurchaseReceivingSearch, self.store)

    def on_SearchTransfer__activate(self, action):
        self._search_transfers()

    def on_SearchTransferItems__activate(self, action):
        self.run_dialog(TransferItemSearch, self.store)

    def on_SearchPendingReturnedSales__activate(self, action):
        self._search_pending_returned_sales()

    def on_SearchReturnedItems__activate(self, action):
        self.run_dialog(ReturnedItemSearch, self.store)

    def on_SearchPurchasedStockItems__activate(self, action):
        self.run_dialog(PurchasedItemsSearch, self.store)

    def on_SearchStockItems__activate(self, action):
        self.run_dialog(ProductStockSearch, self.store)

    def on_SearchBrandItems__activate(self, action):
        self.run_dialog(ProductBrandSearch, self.store)

    def on_SearchBrandItemsByBranch__activate(self, action):
        self.run_dialog(ProductBrandByBranchSearch, self.store)

    def on_SearchBatchItems__activate(self, action):
        self.run_dialog(ProductBatchSearch, self.store)

    def on_SearchClosedStockItems__activate(self, action):
        self.run_dialog(ProductClosedStockSearch, self.store)

    def on_SearchProductHistory__activate(self, action):
        self.run_dialog(ProductSearchQuantity, self.store)

    def on_SearchStockDecrease__activate(self, action):
        self.run_dialog(StockDecreaseSearch, self.store)
