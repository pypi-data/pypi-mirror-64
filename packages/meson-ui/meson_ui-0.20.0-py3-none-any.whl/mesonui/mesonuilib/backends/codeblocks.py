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
from ..buildsystem import Ninja
import logging
import os
import re
import xml.etree.ElementTree as ETree

BUILD_OPTION_EXECUTABLE = 1
BUILD_OPTION_STATIC_LIBRARY = 2
BUILD_OPTION_SHARED_LIBRARY = 3
BUILD_OPTION_COMMANDS_ONLY = 4
CBP_VERSION_MAJOR = 1
CBP_VERSION_MINOR = 6


class CodeBlocksBackend(BackendImplementionApi):
    def __init__(self, meson_api: MesonAPI):
        super(self.__class__, self).__init__(meson_api)
        self.backend: str = '\'codeblocks\''
        self.project_name = re.sub(r'[^a-z0-9]', '_', self.projectinfo['descriptive_name'])
        self.compiler = self.targetsinfo[0]['target_sources'][0]['compiler'][0]
        self.source: str = self.mesoninfo['directories']['source']
        self.build: str = self.mesoninfo['directories']['build']
        self.includes: list = []
        self.scripts: list = []
        self.sources: list = []
        self.defs: list = []
        self.ninja = Ninja(self.source, self.build)

    def generator(self):
        logging.info(f'Generating {self.backend} project')
        self.generate_project()

    def generate_project(self):
        root = ETree.Element('CodeBlocks_project_file')
        tree = ETree.ElementTree(root)
        ETree.SubElement(root, 'FileVersion', {'major': f'{CBP_VERSION_MAJOR}', 'minor': f'{CBP_VERSION_MINOR}'})
        project = ETree.SubElement(root, 'Project')
        ETree.SubElement(project, 'Option', {'title': self.project_name})
        ETree.SubElement(project, 'Option', {'makefile_is_custom': '1'})
        ETree.SubElement(project, 'Option', {'compiler': self.compiler})
        ETree.SubElement(project, 'Option', {'virtualFolders': 'Meson Files'})

        build = ETree.SubElement(project, 'Build')

        for target in self.targetsinfo:
            build_target = ETree.SubElement(build, 'Target', {'title': target['name']})
            output = join_paths(self.build, target['id'])
            ETree.SubElement(build_target, 'Option', {'output': output})
            ETree.SubElement(build_target, 'Option', {'working_dir': os.path.split(output)[0]})
            ETree.SubElement(build_target, 'Option', {'object_output': join_paths(os.path.split(output)[0], target['id'])})
            ty = {
                'executable': f'{BUILD_OPTION_EXECUTABLE}',
                'static library': f'{BUILD_OPTION_STATIC_LIBRARY}',
                'shared library': f'{BUILD_OPTION_SHARED_LIBRARY}',
                'custom': f'{BUILD_OPTION_COMMANDS_ONLY}',
                'run': f'{BUILD_OPTION_COMMANDS_ONLY}'
            }[target['type']]
            ETree.SubElement(build_target, 'Option', {'type': ty})

            compiler = target
            if compiler:
                ETree.SubElement(build_target, 'Option', {'compiler': self.compiler})

            compiler = ETree.SubElement(build_target, 'Compiler')

            for define in self.defs:
                ETree.SubElement(compiler, 'Add', {'option': define})

            for include_dir in self.includes:
                ETree.SubElement(compiler, 'Add', {'directory': include_dir})

            make_commands = ETree.SubElement(build_target, 'MakeCommands')
            ETree.SubElement(make_commands, 'Build', {'command': f'{self.ninja.exe} -v {target["name"]}'})
            ETree.SubElement(make_commands, 'CompileFile', {'command': f'{self.ninja.exe} -v {target["name"]}'})
            ETree.SubElement(make_commands, 'Clean', {'command': f'{self.ninja.exe} -v clean'})
            ETree.SubElement(make_commands, 'DistClean', {'command': f'{self.ninja.exe} -v clean'})

        for target in self.targetsinfo:
            for target_file in self.sources:
                unit = ETree.SubElement(project, 'Unit', {'filename': join_paths(self.source, target_file)})
                ETree.SubElement(unit, 'Option', {'target': target['name']})

                base = os.path.splitext(os.path.basename(target_file))[0]
                header_exts = ('h', 'hpp')
                for ext in header_exts:
                    header_file = os.path.abspath(
                        join_paths(self.source, os.path.dirname(target_file), join_paths(base + '.' + ext)))
                    if os.path.exists(header_file):
                        unit = ETree.SubElement(project, 'Unit', {'filename': header_file})
                        ETree.SubElement(unit, 'Option', {'target': target['name']})

        for file in self.scripts:
            unit = ETree.SubElement(project, 'Unit', {'filename': join_paths(self.source, file)})
            ETree.SubElement(unit, 'Option', {'virtualFolder': join_paths('Meson Files', os.path.dirname(file))})

        project_file = join_paths(self.build, f'{self.project_name}.cbp')
        tree.write(project_file, 'unicode', True)

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