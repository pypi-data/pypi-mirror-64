
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
##
""" Editors implementation for Stoq devices configuration"""

from stoqdrivers.interfaces import INonFiscalPrinter
from stoqdrivers.printers.base import (get_baudrate_values,
                                       get_usb_printer_devices,
                                       get_supported_printers_by_iface)
from stoqdrivers.scales.base import get_supported_scales

from stoqlib.api import api
from stoqlib.domain.devices import DeviceSettings
from stoqlib.domain.station import BranchStation
from stoqlib.gui.editors.baseeditor import BaseEditor
from stoqlib.lib.devicemanager import DeviceManager
from stoqlib.lib.environment import is_developer_mode
from stoqlib.lib.message import warning
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext


TEST_MESSAGE = """<unset_condensed>
<centralize>Welcome to <set_bold>Stoq<unset_bold>
<set_condensed>Condensed <set_bold>bold<unset_bold> text<unset_condensed>
<set_double_height>Double Height<unset_double_height>
<descentralize>
<cut_paper>
"""


class DeviceSettingsEditor(BaseEditor):
    gladefile = 'DeviceSettingsEditor'
    model_type = DeviceSettings
    proxy_widgets = ('type_combo',
                     'brand_combo',
                     'device_combo',
                     'model_combo',
                     'baudrate',
                     'station',
                     'is_active_button')

    def __init__(self, store, model=None, station=None):
        if station is not None and not isinstance(station, BranchStation):
            raise TypeError("station should be a BranchStation")

        self._branch_station = station
        # This attribute is set to True when setup_proxies is finished
        self._is_initialized = False
        BaseEditor.__init__(self, store, model)
        self._original_brand = self.model.brand
        self._original_model = self.model.model
        self.test_button = self.add_button(_('Test device'))

    def refresh_ok(self, *args):
        if not self._is_initialized:
            return
        if self.test_button:
            self.test_button.set_sensitive(self.model.is_valid())
        BaseEditor.refresh_ok(self, self.model.is_valid())

    def setup_station_combo(self):
        if self._branch_station:
            self.station.prefill([(self._branch_station.name,
                                   self._branch_station)])
            self.model.station = self._branch_station
            return

        self.station.prefill(
            [(station.name, station)
             for station in BranchStation.get_active_stations(self.store)])

    def setup_device_port_combo(self):
        items = [(_("Choose..."), None)]
        items.extend([(str(device.device_name), str(device.device_name))
                      for device in DeviceManager.get_serial_devices()])
        items.extend(self._get_usb_devices())

        if is_developer_mode():
            # Include virtual port for virtual printer
            items.append(('Virtual device', u'/dev/null'))

        devices = [i[1] for i in items]
        if self.model.device_name not in devices:
            items.append(('Unkown device (%s)' % self.model.device_name,
                          self.model.device_name))
        self.device_combo.prefill(items)

    def setup_device_types_combo(self):
        items = [(_("Choose..."), None)]
        device_types = (
            # TODO: Reenable when we have cheque printers working.
            # DeviceSettings.CHEQUE_PRINTER_DEVICE,
            DeviceSettings.NON_FISCAL_PRINTER_DEVICE,
            DeviceSettings.SCALE_DEVICE, )

        items.extend([(self.model.describe_device_type(t), t)
                      for t in device_types])
        self.type_combo.prefill(items)

    def setup_widgets(self):
        self.setup_device_types_combo()
        self.setup_device_port_combo()
        self.setup_station_combo()
        self.baudrate.prefill(get_baudrate_values())
        if not self.edit_mode:
            self.is_active_button.set_sensitive(False)

    def _get_supported_types(self):
        if self.model.type == DeviceSettings.SCALE_DEVICE:
            supported_types = get_supported_scales()
        #elif self.model.type == DeviceSettings.CHEQUE_PRINTER_DEVICE:
        #    supported_types = get_supported_printers_by_iface(IChequePrinter)
        elif self.model.type == DeviceSettings.NON_FISCAL_PRINTER_DEVICE:
            supported_types = get_supported_printers_by_iface(INonFiscalPrinter,
                                                              include_virtual=is_developer_mode())
        else:
            raise TypeError("The selected device type isn't supported")
        return supported_types

    def _get_usb_devices(self):
        try:
            import usb.core
        except ImportError:  # pragma no cover
            return []

        devices = []
        for device in get_usb_printer_devices():
            try:
                dev = 'usb:{}:{}'.format(hex(device.idVendor), hex(device.idProduct))
                try:
                    if device.manufacturer is not None:
                        desc = '{} {}'.format(device.manufacturer, device.product)
                    else:
                        desc = dev
                except Exception:
                    desc = dev

                devices.append((desc, dev))
            except usb.core.USBError:  # pragma no cover
                # The user might not have access to some devices
                continue

        return devices

    def _get_supported_brands(self):
        return sorted(list(self._get_supported_types().keys()))

    def _get_supported_models(self):
        return self._get_supported_types()[self.model.brand]

    def update_brand_combo(self):
        self.brand_combo.clear()
        self.brand_combo.set_sensitive(self.model.type is not None)
        if self.model.type is None:
            return
        items = [(_("Choose..."), None)]
        supported_brands = self._get_supported_brands()
        items.extend([(brand.capitalize(), str(brand))
                      for brand in supported_brands])
        self.brand_combo.prefill(items)

    def update_model_combo(self):
        self.model_combo.clear()
        brand = self.model.brand
        self.model_combo.set_sensitive(brand is not None)
        if self.model.brand is None:
            return
        supported_models = self._get_supported_models()
        items = [(_("Choose..."), None)]
        items.extend([(obj.model_name, str(obj.__name__))
                      for obj in supported_models])
        self.model_combo.prefill(items)

    #
    # BaseEditor hooks
    #

    def setup_proxies(self):
        self.setup_widgets()
        self.proxy = self.add_proxy(self.model,
                                    DeviceSettingsEditor.proxy_widgets)
        self._is_initialized = True

    def create_model(self, store):
        return DeviceSettings(device_name=None,
                              station=api.get_current_station(store),
                              baudrate=9600,
                              brand=None,
                              model=None,
                              type=None,
                              store=store)

    def get_title(self, *args):
        if self.edit_mode:
            return _("Edit Device for %s") % self.model.station.name
        else:
            return _("Add Device")

    def validate_confirm(self):
        settings = DeviceSettings.get_by_station_and_type(
            store=api.get_default_store(),
            station=self.model.station.id,
            type=self.model.type,
            exclude=self.model)
        if settings and self.is_active_button.get_active():
            warning(_(u"An active %s already exists for station \"%s\"") % (
                    self.model.device_type_name,
                    self.model.station_name))
            return False

        return True

    #
    # Kiwi callbacks
    #

    def on_brand_combo__changed(self, *args):
        self.update_model_combo()
        self.refresh_ok()

    def on_type_combo__changed(self, *args):
        self.update_brand_combo()
        self.refresh_ok()

    def on_model_combo__changed(self, *args):
        self.refresh_ok()

    def on_device_combo__changed(self, *args):
        self.refresh_ok()

    def on_test_button__clicked(self, button):
        driver = self.model.get_interface()
        if self.model.type == DeviceSettings.NON_FISCAL_PRINTER_DEVICE:
            driver.open()
            driver.print_line(TEST_MESSAGE)
        elif self.model.type == DeviceSettings.SCALE_DEVICE:
            data = driver.read_data()
            warning(str(data.weight))
