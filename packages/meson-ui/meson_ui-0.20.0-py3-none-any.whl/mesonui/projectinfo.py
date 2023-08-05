#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#


class ProjectInfo:
    def get_description(self) -> str:
        return 'Meson-UI is a build GUI for Meson build system.'

    def get_version(self) -> str:
        return '0.20.0'

    def get_license(self) -> str:
        return 'Apache-2.0'

    def get_project_name(self) -> str:
        return 'meson-ui'

    def get_packages(self) -> list:
        return ['mesonui',
                'mesonui.containers',
                'mesonui.dashboard',
                'mesonui.mesonuilib',
                'mesonui.repository',
                'mesonui.models',
                'mesonui.view',
                'mesonui.ui',
                'mesonui.mesonuilib.appconfig',
                'mesonui.mesonuilib.backends',
                'mesonui.mesonuilib.ninjabuild',
                'mesonui.mesonuilib.mesonbuild']
