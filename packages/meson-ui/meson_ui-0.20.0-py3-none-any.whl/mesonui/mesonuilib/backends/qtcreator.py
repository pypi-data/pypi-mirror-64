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
import logging
import os
import re


class QtCreatorBackend(BackendImplementionApi):
    def __init__(self, meson_api: MesonAPI):
        super(self.__class__, self).__init__(meson_api)
        self.backend: str = '\'qtcreator\''
        self.project_name = re.sub(r'[^a-z0-9]', '_', self.projectinfo['descriptive_name'])
        self.source: str = self.mesoninfo['directories']['source']
        self.build: str = self.mesoninfo['directories']['build']
        self.includes: list = []
        self.scripts: list = []
        self.sources: list = []
        self.defs: list = []

    def generator(self):
        logging.info(f'Generating {self.backend} project')
        self.generate_project()

    def generate_project(self):
        # Generate the .creator file.
        with open(join_paths(self.build, f'{self.project_name}.creator'), 'w') as file:
            file.write('[General]')

        # Generate the .config file.
        with open(join_paths(self.build, f'{self.project_name}.config'), 'w') as file:
            file.write('// Add predefined macros for your project here. For example:')
            file.write('// #define THE_ANSWER 42')
            for item in self.defs:
                item = ' '.join(item.split('='))
                file.write(f'#define {item}\n')

        # Generate the .files file.
        with open(join_paths(self.build, f'{self.project_name}.files'), 'w') as file:
            for item in self.sources + self.scripts:
                file.write(os.path.relpath(item, self.build) + '\n')

        # Generate the .includes file.
        with open(join_paths(self.build, f'{self.project_name}.includes'), 'w') as file:
            for item in self.includes:
                file.write(os.path.relpath(item, self.build) + '\n')

    def find_includes(self):
        include_dirs: list = []
        for target in self.targetsinfo:
            for includes in target['target_sources'][0]['parameters']:
                if includes.startswith('-I') or includes.startswith('/I'):
                    logging.info(f'add include: {includes}')
                    include_dirs.append([includes])
        self.includes = include_dirs

    def find_definitions(self):
        definitions: list = []
        for target in self.targetsinfo:
            for defs in target['target_sources'][0]['parameters']:
                if defs.startswith('-D'):
                    logging.info(f'add def: {defs}')
                    definitions.append([defs])
        self.defs = definitions

    def find_source_files(self):
        sources: list = []
        for target in self.targetsinfo:
            for file in target['target_sources'][0]['sources']:
                logging.info(f'add source: {file}')
                sources.append([file])
        self.source = sources

    def find_build_files(self):
        self.scripts = self.buildsystem_files
