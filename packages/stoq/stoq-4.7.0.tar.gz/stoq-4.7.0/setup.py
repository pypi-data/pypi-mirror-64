# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

#
# Copyright (C) 2005-2011 Async Open Source
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
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
# Author(s): Stoq Team <stoq-devel@async.com.br>
#

#
# Dependency checking
#

from stoq.lib.dependencies import DependencyChecker
dc = DependencyChecker()
dc.text_mode = True
# We don't need latest kiwi in here
dc.check_kiwi((3, 0, 0))

#
# Package installation
#

import os
import sys

from kiwi.dist import setup, listfiles, listpackages

from stoq import website, version


building_egg = 'bdist_egg' in sys.argv


def listplugins(plugins, exts):
    plugin_dir = os.path.join('$datadir', 'plugins')
    dirs = []
    for package in listpackages('plugins'):
        # strip plugins
        dirs.append(package.replace('.', '/'))
    files = []
    for directory in dirs:
        install_dir = os.path.join('$datadir', directory)
        files.append((install_dir, listfiles(directory, '*.py')))
        files.append((install_dir, listfiles(directory, '*.plugin')))

    for plugin in plugins:
        for kind, suffix in exts:
            x = listfiles('plugins', plugin, kind, suffix)
            if x:
                path = os.path.join(plugin_dir, '%s', '%s')
                files.append((path % (plugin, kind), x))

        files.append((os.path.join(plugin_dir, plugin),
                      listfiles('plugins', plugin, '*.py')))

    return files


def list_recursive(base_dir, extentions, prefix='$datadir'):
    files = []
    base_dir = os.path.join(*base_dir.split('/'))
    for root, _, _ in os.walk(base_dir):
        parts = root.split(os.sep)
        _prefix = os.path.join(prefix, *parts[1:])
        for ext in extentions:
            files.append((_prefix, listfiles(*(parts + [ext]))))
    return files


packages = listpackages('stoq')
packages.extend(listpackages('stoqlib', exclude='stoqlib.tests'))

scripts = [
    'bin/stoq',
    'bin/stoqdbadmin',
]
data_files = [
    ('$datadir/csv', listfiles('data', 'csv', '*.csv')),
    ('$datadir/csv/ibpt_tables', listfiles('data', 'csv', 'ibpt_tables', '*.csv')),
    ('$datadir/csv/cest', listfiles('data', 'csv', 'cest', '*.csv')),
    ('$datadir/glade', listfiles('data', 'glade', '*.ui')),
    ('$datadir/misc', listfiles('data/misc', '*.*')),
    ('$datadir/pixmaps', listfiles('data', 'pixmaps', '*.png')),
    ('$datadir/pixmaps', listfiles('data', 'pixmaps', '*.svg')),
    ('$datadir/pixmaps', listfiles('data', 'pixmaps', '*.jpg')),
    ('$datadir/pixmaps', listfiles('data', 'pixmaps', '*.gif')),
    ('$datadir/pixmaps', listfiles('data', 'pixmaps', '*.bmp')),
    ('$datadir/scripts', listfiles('data', 'scripts', '*.py')),
    ('$datadir/scripts', listfiles('data', 'scripts', '*.sh')),
    ('$datadir/sql', listfiles('data', 'sql', '*.sql')),
    ('$datadir/sql', listfiles('data', 'sql', '*.py')),
    ('$datadir/uixml', listfiles('data', 'uixml', '*.xml')),
    ('$datadir/html', listfiles('data', 'html', '*.html')),
    ('$datadir/html/css', listfiles('data', 'html', 'css', '*.css')),
    ('$datadir/html/images', listfiles('data', 'html', 'images', '*.png')),
    ('$datadir/html/js', listfiles('data', 'html', 'js', '*.js')),
    ('$datadir/docs', ['AUTHORS', 'CONTRIBUTORS', 'COPYING', 'COPYING.pt_BR',
                       'COPYING.stoqlib', 'README', 'docs/copyright']),
]

if building_egg:
    data_files.append(('', ['__main__.py']))

data_files += list_recursive('data/template', ['*html', '*css'])
data_files += list_recursive('data/pixmaps/hicolor', ['*png', '*svg'])

if building_egg:
    data_files.extend([
        ('$datadir/docs/manual/pt_BR',
         listfiles('docs/manual/pt_BR', '*.page')),
        ('$datadir/docs/manual/pt_BR',
         listfiles('docs/manual/pt_BR', '*.xml')),
        ('$datadir/docs/manual/pt_BR',
         listfiles('docs/manual/pt_BR/figures', '*.png')),
        ('$datadir/docs/manual/pt_BR',
         listfiles('docs/manual/pt_BR/figures', '*.svg')),
    ])
else:
    data_files.extend([
        ('/etc/udev/rules.d', listfiles('data', 'udev', '10-stoq.rules')),
        ('share/applications', ['stoq.desktop']),
        ('share/doc/stoq',
         ['AUTHORS', 'CONTRIBUTORS', 'COPYING', 'COPYING.pt_BR',
          'COPYING.stoqlib', 'README', 'docs/copyright']),
        ('share/gnome/help/stoq/C',
         listfiles('docs/manual/pt_BR', '*.page')),
        ('share/gnome/help/stoq/C',
         listfiles('docs/manual/pt_BR', '*.xml')),
        ('share/gnome/help/stoq/C/figures',
         listfiles('docs/manual/pt_BR/figures', '*.png')),
        ('share/gnome/help/stoq/C/figures',
         listfiles('docs/manual/pt_BR/figures', '*.svg')),
        ('share/icons/hicolor/48x48/apps', ['data/pixmaps/stoq.png']),
        ('share/polkit-1/actions', ['data/br.com.stoq.createdatabase.policy']),
    ])

PLUGINS = ['ecf', 'nfe', 'books', 'optical']
PLUGIN_EXTS = [('csv', '*csv'),
               ('glade', '*.ui'),
               ('sql', '*.sql'),
               ('sql', '*.py')]

data_files += listplugins(PLUGINS, PLUGIN_EXTS)

# TODO: Put additional requirements that are not on pypi here. See:
# https://pythonhosted.org/setuptools/setuptools.html#dependencies-that-aren-t-in-pypi
# Try to make a way to integrate it with debian packaging, just like the
# dependencies bellow.
install_requires = []
with open('requirements.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('https://'):
            # requirements.txt file format is a bit different from setup install_requires argument
            package = line.split('=')[-1]
            line = '%s @ %s' % (package, line)
        install_requires.append(line)


setup(name='stoq',
      version=version,
      author="Async Open Source",
      author_email="stoq-devel@async.com.br",
      description="A powerful retail system",
      long_description="""
      Stoq is an advanced retails system which has as main goals the
      usability, good devices support, and useful features for retails.
      """,
      url=website,
      license="GNU GPL 2.0 and GNU LGPL 2.1 (see COPYING and COPYING.stoqlib)",
      packages=packages,
      data_files=data_files,
      scripts=scripts,
      install_requires=install_requires,
      setup_requires=['pycairo'],  # workaround to force pycairo installation before PyGObject
      zip_safe=building_egg)
