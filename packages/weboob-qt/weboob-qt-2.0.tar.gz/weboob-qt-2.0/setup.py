#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright(C) 2010-2014 Christophe Benz, Laurent Bachelier
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import glob
import os
import subprocess
import sys
from distutils.cmd import Command
from distutils.log import WARN

from setuptools import find_packages, setup


PY3 = sys.version_info.major >= 3


class BuildQt(Command):
    description = 'build Qt applications'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce('Building Qt applications...', WARN)
        make = self.find_executable('make', ('gmake', 'make'))
        if not PY3:
            pyuic5 = self.find_executable(
                'pyuic5',
                ('python2-pyuic5', 'pyuic5-python2.7', 'pyuic5'))
        else:
            pyuic5 = self.find_executable(
                'pyuic5',
                ('python3-pyuic5', 'pyuic5-python3.7', 'pyuic5-python3.6', 'pyuic5-python3.5', 'pyuic5'))
        if not pyuic5 or not make:
            print('Install missing component(s) (see above) or disable Qt applications (with --no-qt).',
                  file=sys.stderr)
            sys.exit(1)

        subprocess.check_call(
            [make,
             '-f', 'build.mk',
             '-s', '-j2',
             'all',
             'PYUIC=%s%s' % (pyuic5, ' WIN32=1' if sys.platform == 'win32' else '')])

    @staticmethod
    def find_executable(name, names):
        envname = '%s_EXECUTABLE' % name.upper()
        if os.getenv(envname):
            return os.getenv(envname)
        paths = os.getenv('PATH', os.defpath).split(os.pathsep)
        exts = os.getenv('PATHEXT', os.pathsep).split(os.pathsep)
        for name in names:
            for path in paths:
                for ext in exts:
                    fpath = os.path.join(path, name) + ext
                    if os.path.exists(fpath) and os.access(fpath, os.X_OK):
                        return fpath
        print('Could not find executable: %s' % name, file=sys.stderr)


def install_weboob():
    data_files = [
        ('share/man/man1', glob.glob('man/*')),
    ]
    data_files.extend([
        ('share/applications', glob.glob('desktop/*')),
        ('share/icons/hicolor/64x64/apps', glob.glob('icons/*')),
    ])

    requirements = [
        'weboob',
        'PyQt5',
    ]

    try:
        if sys.argv[1] == 'requirements':
            print('\n'.join(requirements))
            sys.exit(0)
    except IndexError:
        pass

    setup(
        packages=find_packages(),
        data_files=data_files,
        cmdclass={
            'build_qt': BuildQt,
        },
    )


if os.getenv('WEBOOB_SETUP'):
    args = os.getenv('WEBOOB_SETUP').split()
else:
    args = sys.argv[1:]

args.insert(0, 'build_qt')

sys.argv = [sys.argv[0]] + args

install_weboob()
