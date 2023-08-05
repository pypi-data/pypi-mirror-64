#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from subprocess import check_output
from subprocess import STDOUT
from os.path import join
from pathlib import Path
import json


class MesonScriptReader:
    def __init__(self, sourcedir: Path = None):
        self._sourcedir: Path = sourcedir

    def _introspect(self, args: list) -> any:
        cmd: list = ['meson', 'introspect']
        cmd.extend(args)
        return check_output(cmd, stderr=STDOUT)

    def _scan(self, group: str) -> any:
        info: any = json.loads(self._introspect([group, '--force-object-output', join(self._sourcedir, 'meson.build')]))
        return info

    def extract_from(self, group: str) -> any:
        #
        # We need to make sure to return None if testlogs.json is not found. So
        # check to see if the group is "testlog" and if so give nothing back
        if group == 'testlog':
            return None
        elif group == 'buildoptions':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'tests':
            return self._scan(group=f'--{group}')
        elif group == 'benchmarks':
            return self._scan(group=f'--{group}')
        elif group == 'projectinfo':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'scan-dependencies':
            info = self._scan(group=f'--{group}')
            return info['scan_dependencies']
        elif group == 'dependencies':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'targets':
            info = self._scan(group=f'--{group}')
            return info[group]
        else:
            raise Exception(f'Group tag {group} not found in extract via data options!')
