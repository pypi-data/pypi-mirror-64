# -*- Mode: Python; coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2016 Async Open Source <http://www.async.com.br>
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

import collections
import datetime
import os
import threading

import dateutil.parser
from gi.repository import GObject, GLib
from kiwi.python import Settable
from kiwi.utils import gsignal

from stoqlib.api import api, safe_str
from stoqlib.gui.base.dialogs import run_dialog
from stoqlib.gui.editors.backupsettings import BackupSettingsEditor
from stoqlib.lib.decorators import threaded
from stoqlib.lib.threadutils import threadit, schedule_in_main_thread
from stoqlib.lib.translation import stoqlib_gettext as _
from stoqlib.lib.webservice import WebService
from stoqlib.lib.message import warning
from stoqlib.net.server import ServerProxy, ServerError

import stoq


class ResourceStatus(GObject.GObject):
    """The status of a given resource"""

    gsignal('status-changed', int, str)

    (STATUS_NA,
     STATUS_OK,
     STATUS_WARNING,
     STATUS_ERROR) = range(4)

    status_label = {
        STATUS_NA: _("N/A"),
        STATUS_OK: _("OK"),
        STATUS_WARNING: _("WARNING"),
        STATUS_ERROR: _("ERROR"),
    }

    name = None
    label = None
    status = STATUS_NA
    reason = None
    reason_long = None
    priority = 0
    refresh_timeout = int(os.environ.get('STOQ_STATUS_REFRESH_TIMEOUT', 60))

    def __init__(self):
        super(ResourceStatus, self).__init__()

        assert self.name is not None
        GLib.timeout_add_seconds(self.refresh_timeout, self.refresh_and_notify)

        # Schedule first update for right after now. Dont call refresh_and_notify()
        # directly as it will block the interface briefly
        GLib.timeout_add_seconds(1, lambda: self.refresh_and_notify() and False)

    __hash__ = GObject.GObject.__hash__

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.name == other.name

    @property
    def status_str(self):
        return self.status_label[self.status]

    def refresh(self):
        """Refresh the resource status

        Subclasses should override this and update
        :obj:`.status` and :obj:`.reason`

        Note that this will not be running on the main thread,
        so be cautelous with non thread-safe operations.
        """
        raise NotImplementedError

    def get_actions(self):
        """Get the actions that can be run for this resource"""
        return []

    def refresh_and_notify(self):
        """Refresh the resource status and notify for changes"""
        old_status, old_reason = self.status, self.reason
        self.refresh()

        if (self.status, self.reason) != (old_status, old_reason):
            self.emit('status-changed', self.status, self.reason)


class ResourceStatusAction(object):

    def __init__(self, resource, name, label, callback,
                 threaded=True, admin_only=True):
        self.resource = resource
        self.name = name
        self.label = label
        self.callback = callback
        self.threaded = threaded
        self.admin_only = admin_only

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.resource, self.name) == (other.resource, other.name)


class ResourceStatusManager(GObject.GObject):

    gsignal('status-changed', int)
    gsignal('action-started', object)
    gsignal('action-finished', object, object)

    _instance = None

    _messages_registered = False

    def __init__(self):
        super(ResourceStatusManager, self).__init__()

        self._lock = threading.Lock()
        self.running_action = None
        self.resources = collections.OrderedDict()

    #
    #  Public API
    #

    @classmethod
    def get_instance(cls):
        """Get the manager singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
            cls._try_register_messages()
        return cls._instance

    @property
    def status(self):
        """The general status of the resources"""
        if any(resource.status == ResourceStatus.STATUS_ERROR
               for resource in self._iter_resources()):
            return ResourceStatus.STATUS_ERROR
        elif any(resource.status == ResourceStatus.STATUS_WARNING
                 for resource in self._iter_resources()):
            return ResourceStatus.STATUS_WARNING
        elif any(resource.status == ResourceStatus.STATUS_NA
                 for resource in self._iter_resources()):
            return ResourceStatus.STATUS_NA
        else:
            return ResourceStatus.STATUS_OK

    def add_resource(self, resource, refresh=False):
        """Add a :class:`.ResourceStatus` on the manager"""
        assert resource.name not in self.resources
        assert isinstance(resource, ResourceStatus)
        self.resources[resource.name] = resource
        resource.connect('status-changed', self._on_resource__status_changed)
        if refresh:
            self.refresh_and_notify()

    def refresh_and_notify(self, force=False):
        """Refresh the status and notify for changes"""
        # Do not run checks if we are running tests. It breaks the whole suite
        if os.environ.get('STOQ_TESTSUIT_RUNNING', '0') == '1':
            return False
        return self._refresh_and_notify(force=force)

    def handle_action(self, action):
        """Ask the given resource to handle the given action"""
        self.running_action = action
        if action.threaded:
            return threadit(self._handle_action, action)
        else:
            return self._handle_action(action)

    #
    #  Private
    #

    @classmethod
    def _try_register_messages(cls):
        if cls._messages_registered:
            return

        from stoqlib.domain.message import Message
        with api.new_store() as store:
            user = api.get_current_user(store)
            branch = api.get_current_branch(store)
            # We cannot setup correctly if the user or branch are not setup yet.
            if not user or not branch:
                return

            messages = Message.find_active(store, branch, user)
            for msg in messages:
                @register
                class Foo(ResourceStatus):
                    name = msg.id
                    label = _('Message')
                    status = ResourceStatus.STATUS_WARNING
                    reason = msg.content

                    def refresh(self):
                        pass
        cls._messages_registered = True

    def _iter_resources(self):
        return sorted(self.resources.values(), key=lambda r: r.priority)

    def _refresh_and_notify(self, resources=None, force=False):
        resources = resources or self._iter_resources()
        for resource in resources:
            resource.refresh_and_notify()

    def _handle_action(self, action):
        schedule_in_main_thread(self.emit, 'action-started', action)
        try:
            with self._lock:
                retval = action.callback()
        except Exception as e:
            retval = e
            schedule_in_main_thread(
                lambda: warning(_('An error happened when executing "%s"') %
                                (action.label, ), str(retval)) and False)
        finally:
            self.running_action = None
            schedule_in_main_thread(self.emit, 'action-finished',
                                    action, retval)

        return retval

    def _on_resource__status_changed(self, resource, status, message):
        # When a resource changes its status, so do we
        self.emit('status-changed', self.status)


def register(resource_class, refresh=False):
    manager = ResourceStatusManager.get_instance()
    manager.add_resource(resource_class(), refresh=refresh)
    return resource_class


@register
class _ServerStatus(ResourceStatus):

    name = "stoqserver"
    label = _("Online Services")
    priority = 99

    def __init__(self):
        ResourceStatus.__init__(self)
        self._server = ServerProxy()

    @threaded
    def _check_running(self):
        return self._server.check_running()

    def refresh(self):
        if stoq.trial_mode:
            self.status = ResourceStatus.STATUS_NA
            self.reason = (_('Online features are not available in trial mode'))
            self.reason_long = _('Online features require a subscription of Stoq.link')
            return

        if not api.sysparam.get_bool('ONLINE_SERVICES'):
            self.status = ResourceStatus.STATUS_NA
            self.reason = (_("Online services (Stoq.link integration, backup, "
                             "etc) not enabled..."))
            self.reason_long = _('Enable the parameter "Online Services" '
                                 'on the "Admin" app to solve this issue')
            return

        if self._check_running():
            self.status = self.STATUS_OK
            self.reason = _("Online services data hub is running fine.")
            self.reason_long = None
        else:
            self.status = ResourceStatus.STATUS_ERROR
            self.reason = _("Online services data hub not found...")
            package = '<a href="apt://stoq-server">stoq-server</a>'
            self.reason_long = safe_str(
                api.escape(_("Install and configure the %s package "
                             "to solve this issue")) % (package, ))


@register
class _BackupStatus(ResourceStatus):

    name = "backup"
    label = _("Backup")
    priority = 98

    def __init__(self):
        ResourceStatus.__init__(self)
        self._webservice = WebService()
        self._server = ServerProxy()

    @threaded
    def _get_key(self):
        return self._server.call('get_backup_key')

    @threaded
    def _get_server_status(self):
        request = self._webservice.status()
        return request.get_response()

    def refresh(self):
        if stoq.trial_mode:
            self.status = ResourceStatus.STATUS_NA
            self.reason = (_('Online features are not available in trial mode'))
            self.reason_long = _('Online features require a subscription of Stoq.link')
            return

        if not api.sysparam.get_bool('ONLINE_SERVICES'):
            self.status = ResourceStatus.STATUS_NA
            self.reason = _('Backup service not running because '
                            '"Online Services" is disabled')
            self.reason_long = _('Enable the parameter "Online Services" '
                                 'on the "Admin" app to solve this issue')
            return

        try:
            key = self._get_key()
        except ServerError:
            pass
        else:
            if not key:
                self.status = self.STATUS_WARNING
                self.reason = _("Backup key not configured")
                self.reason_long = _('Click on "Configure" button to '
                                     'configure the backup key')
                return

        try:
            response = self._get_server_status()
        except Exception as e:
            self.status = self.STATUS_WARNING
            self.reason = _("Could not communicate with Stoq.link")
            self.reason_long = str(e)
            return

        if response.status_code != 200:
            self.status = self.STATUS_WARNING
            self.reason = _("Could not communicate with Stoq.link")
            self.reason_long = None
            return

        data = response.json()
        if data['latest_backup_date']:
            backup_date = dateutil.parser.parse(data['latest_backup_date'])
            delta = datetime.datetime.today() - backup_date

            if delta.days > 3:
                self.status = self.STATUS_WARNING
                self.reason = _("Backup is late. Last backup date is %s") % (
                    backup_date.strftime('%x'))
                self.reason_long = _("Check your Stoq Server logs to see if "
                                     "there's any problem with it")
            else:
                self.status = self.STATUS_OK
                self.reason = _("Backup is up-to-date. Last backup date is %s") % (
                    backup_date.strftime('%x'))
                self.reason_long = None
        else:
            self.status = self.STATUS_WARNING
            self.reason = _("There's no backup data yet")
            self.reason_long = None

    def get_actions(self):
        if self.status != ResourceStatus.STATUS_NA:
            yield ResourceStatusAction(
                self, 'backup-now',
                _("Backup now"), self._on_backup_now, threaded=True)
            yield ResourceStatusAction(
                self, 'configure',
                _("Configure"), self._on_configure, threaded=False)

    def _on_configure(self):
        key = self._server.call('get_backup_key')

        with api.new_store() as store:
            rv = run_dialog(BackupSettingsEditor, None,
                            store, Settable(key=key))

        if rv:
            key = self._server.call('set_backup_key', rv.key)

    def _on_backup_now(self):
        self._server.call('backup_database')
