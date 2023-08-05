#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from mesonui.repository.mesonapi import MesonAPI
from .backendimpl import BackendImplementionApi
from os.path import join as join_paths
from ..buildsystem import Meson
import logging
import re
import os


class KDevelopBackend(BackendImplementionApi):
    def __init__(self, meson_api: MesonAPI):
        super(self.__class__, self).__init__(meson_api)
        self.backend: str = '\'kdevelop\''
        self.project_name = re.sub(r'[^a-z0-9]', '_', self.projectinfo['descriptive_name'])
        self.source: str = self.mesoninfo['directories']['source']
        self.build: str = self.mesoninfo['directories']['build']
        self.meson = Meson()

    def generator(self):
        logging.info(f'Generating {self.backend} project')
        self.generate_project()

    def generate_project(self):
        # Generate the .kdev4 file.
        with open(join_paths(self.build, f'{self.project_name}.kdev4'), 'w') as file:
            file.write('[Project]\n')
            file.write('CreatedFrom=meson.build\n')
            file.write('Manager=KDevMesonManager\n')
            file.write(f'Name={self.project_name}\n')

        # Make .kdev4/ directory.
        if not os.path.exists(join_paths(self.build, '.kdev')):
            os.mkdir(join_paths(self.build, '.kdev'))

        # Generate the .kdev4/ file.
        with open(join_paths(self.build, '.kdev', f'{self.project_name}.kdev4'), 'w') as file:
            file.write('[Buildset]\n')
            file.write(f'BuildItems=@Variant({self._variant()})\n\n')

            file.write('[MesonManager]\n')
            file.write(f'Current Build Directory Index=0\n')
            file.write(f'Number of Build Directories=1\n\n')

            file.write('[MesonManager][BuildDir 0]\n')
            file.write('Additional meson arguments=\n')
            file.write(f'Build Build Path={self.build}\n')
            file.write(f'Meson Generator Backend={self.buildoptions[1]["value"]}\n')
            file.write(f'Meson executable={self.meson.exe}\n')

    def _variant(self) -> str:
        variant: str = '\\x00\\x00\\x00\\t\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x0b\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x16'
        for i in self.project_name:
            variant + f'\\x00{i}'
        return variant
