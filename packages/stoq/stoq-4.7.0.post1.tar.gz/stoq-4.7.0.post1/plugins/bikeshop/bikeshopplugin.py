# -*- Mode: Python; coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
##
## Copyright (C) 2014 Async Open Source <http://www.async.com.br>
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

from zope.interface import implementer

from stoqlib.lib.interfaces import IPlugin
from stoqlib.lib.pluginmanager import register_plugin

from .bikeshopui import BikeShopUI


@implementer(IPlugin)
class BikeShopPlugin(object):
    name = u'bikeshop'
    has_product_slave = True

    def __init__(self):
        self.ui = None

    #
    #  IPlugin
    #

    def get_migration(self):
        pass

    def get_tables(self):
        return []

    def activate(self):
        self.ui = BikeShopUI()

    def get_server_tasks(self):
        return []

    def get_dbadmin_commands(self):
        return []

    def handle_dbadmin_command(self, command, options, args):
        assert False


register_plugin(BikeShopPlugin)
