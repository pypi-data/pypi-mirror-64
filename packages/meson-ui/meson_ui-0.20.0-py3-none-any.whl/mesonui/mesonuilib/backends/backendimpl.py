#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#


class BackendImplementionApi:
    def __init__(self, meson_api):
        self.meson_api = meson_api

    @property
    def projectinfo(self):
        return self.meson_api.get_object(group='projectinfo', extract_method='loader')

    @property
    def targetsinfo(self):
        return self.meson_api.get_object(group='targets', extract_method='loader')

    @property
    def mesoninfo(self):
        return self.meson_api.get_object(group='meson-info', extract_method='loader')

    @property
    def testinfo(self):
        return self.meson_api.get_object(group='tests', extract_method='loader')

    @property
    def buildoptions(self):
        return self.meson_api.get_object(group='buildoptions', extract_method='loader')

    @property
    def buildsystem_files(self):
        return self._meson_api.get_object(group='buildsystem-files', extract_method='loader')

    def generator(self):
        raise NotImplementedError('IDE Backend "generate" method not iemented!')

    def generate_project(self):
        raise NotImplementedError('IDE Backend "generate_project" method not iemented!')

    def find_includes(self):
        pass

    def find_definitions(self):
        pass

    def find_source_files(self):
        pass

    def find_compiler_args(self):
        pass

    def find_build_files(self):
        pass
