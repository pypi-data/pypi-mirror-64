# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2012 Async Open Source <http://www.async.com.br>
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
from kiwi.python import Settable

from stoqlib.domain.devices import DeviceSettings
from stoqlib.gui.editors.deviceseditor import DeviceSettingsEditor
from stoqlib.gui.test.uitestutils import GUITest


class _Device(object):
    def __init__(self, name):
        self.device_name = name


class _UsbDevice(object):
    def __init__(self, idVendor, idProduct):
        self.idVendor = idVendor
        self.idProduct = idProduct


class TestDeviceSettingsEditor(GUITest):

    def test_init_wrong_station(self):
        station = object()
        with self.assertRaises(TypeError):
            DeviceSettingsEditor(self.store, station=station)

    @mock.patch('stoqlib.gui.editors.deviceseditor.DeviceManager.get_serial_devices')
    @mock.patch('stoqlib.domain.station.BranchStation.get_active_stations')
    def test_init_without_station(self, get_active_stations, get_serial_devices):
        get_serial_devices.return_value = [_Device('/dev/ttyS0'),
                                           _Device('/dev/ttyS1')]
        get_active_stations.return_value = []
        editor = DeviceSettingsEditor(self.store)
        self.check_editor(editor, 'editor-devicesetting-without-station')

    @mock.patch('stoqlib.gui.editors.deviceseditor.DeviceManager.get_serial_devices')
    def test_create(self, get_serial_devices):
        get_serial_devices.return_value = [_Device('/dev/ttyS0'),
                                           _Device('/dev/ttyS1')]
        station = self.create_station()
        editor = DeviceSettingsEditor(self.store, station=station)
        editor.type_combo.select_item_by_data(DeviceSettings.SCALE_DEVICE)
        editor.brand_combo.select_item_by_data('toledo')
        self.check_editor(editor, 'editor-devicesetting-create')

    @mock.patch('stoqlib.gui.editors.deviceseditor.get_usb_printer_devices')
    @mock.patch('stoqlib.gui.editors.deviceseditor.DeviceManager.get_serial_devices')
    def test_show(self, get_serial_devices, get_usb):
        get_serial_devices.return_value = [_Device('/dev/ttyS0'),
                                           _Device('/dev/ttyS1')]
        get_usb.return_value = [
            # Without manufacturer and product
            Settable(idProduct=1234, idVendor=9999),
            # Without manufacturer
            Settable(idProduct=0x1234, idVendor=0x9876, manufacturer=None,
                     product='Printer'),
            # Complete
            Settable(idProduct=0x1234, idVendor=0x9876, manufacturer='USB',
                     product='Printer')
        ]

        station = self.create_station()
        settings = DeviceSettings(store=self.store,
                                  type=DeviceSettings.SCALE_DEVICE)
        editor = DeviceSettingsEditor(self.store, model=settings,
                                      station=station)
        self.check_editor(editor, 'editor-devicesetting-show')

    def test_get_supported_types(self):
        editor = DeviceSettingsEditor(self.store)

        # Scale type
        editor.model.type = DeviceSettings.SCALE_DEVICE
        types = editor._get_supported_types()
        self.assertIn('toledo', types)

        # Non fiscal type
        editor.model.type = DeviceSettings.NON_FISCAL_PRINTER_DEVICE
        types = editor._get_supported_types()
        self.assertIn('epson', types)
        self.assertIn('bematech', types)

        # Unsupported
        editor.model.type = None
        with self.assertRaises(TypeError):
            editor._get_supported_types()
