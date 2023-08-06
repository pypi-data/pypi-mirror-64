# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import shutil
import pickle
import json
import codecs

from .tools import *
from .component import *
from .occ import *
from .log import logger
from .solution import *
from .repo import *


class Configure:
    def __init__(self):
        self.yoc_version = 'v7.2-dev'
        self.lastUpdateTime = 0
        self.gitlab_token = ''
        self.github_token = ''
        self.gitee_token = '2e92430c127107e35938ea26a9f519e2'
        self.username = ''
        self.password = ''
        self.occ_host = 'occ.t-head.cn'
        self.repo = 'git@gitee.com:yocopen'
        self.init = False

        self.yoc_path = os.getcwd()
        if not self.yoc_path:
            self.yoc_path = '/'
        tmp_path = self.yoc_path
        while tmp_path != '/':
            f = os.path.join(tmp_path, '.yoc')
            if os.path.exists(f):
                self.yoc_path = tmp_path
                conf = yaml_load(f)
                if conf:
                    self.init = True
                    for k, v in conf.items():
                        if v:
                            self.__dict__[k] = v
                break
            tmp_path = os.path.dirname(tmp_path)

    def save(self, yoc_file=None):
        if not yoc_file:
            yoc_file = os.path.join(self.yoc_path, '.yoc')
        with codecs.open(yoc_file, 'w', 'UTF-8') as f:
            for k, v in self.__dict__.items():
                if k not in ['yoc_path', 'init', 'repo', 'gitee_token'] and v:
                    f.write("{}: {}\n".format(k, v))
        self.init = True

    def search_pacakge_yaml(self, subpath=[]):
        paths = []
        if subpath:
            for sub in subpath:
                p = os.path.join(self.yoc_path, sub)
                if os.path.exists(p):
                    paths.append(p)
        else:
            paths.append(self.yoc_path)

        package_list = []

        while paths:
            path = paths[0]
            filename = os.path.join(path, 'package.yaml')
            if os.path.isfile(filename):
                package_list.append(filename)
            else:
                files = os.listdir(path)
                for file in files:
                    p = os.path.join(path, file)
                    if os.path.isdir(p):
                        paths.append(p)
            del paths[0]
        return package_list


class YoC:
    def __init__(self):
        self.occ = None
        self.occ_components = None
        self.conf = Configure()
        self.yoc_path = self.conf.yoc_path

        try:
            compenent_db = os.path.join(self.yoc_path, '.components.db')
            with open(compenent_db, "rb") as f:
                self.occ_components = pickle.load(f)
                if len(self.occ_components) == 0:
                    self.occ_components = None
        except:
            self.occ_components = None

        if not self.occ_components:
            self.conf.lastUpdateTime = 0

        # scanning yoc all components
        self.components = ComponentGroup()
        package_yamls = self.conf.search_pacakge_yaml(
            ['boards', 'components'])

        filename = os.path.join(os.getcwd(), 'package.yaml')
        if os.path.isfile(filename):
            package_yamls.append(filename)

        for filename in package_yamls:
            pack = Component(self.conf, filename)

            if pack.version == '':
                pack.version = self.conf.yoc_version

            if not self.components.add(pack):
                pre_component = self.components.get(pack.name)
                logger.error('component `%s` is multiple (%s : %s)' %
                             (pack.name, pre_component.path, pack.path))
                exit(0)

    def check_depend(self, component):
        def _check_depend(component):
            component.load_package()

            for name in component.depends:
                c = self.components.get(name)
                if c:
                    if c not in depends:
                        depends.append(c)
                    if component not in c.depends_on:
                        c.depends_on.append(component)
                    _check_depend(c)

        depends = ComponentGroup()

        _check_depend(component)
        return depends

    def check_depend_on(self, component):
        depends_on = ComponentGroup()
        for c in self.components:
            c.load_package()
            if component.name in c.depends:
                depends_on.append(c)
        return depends_on

    def getSolution(self, board_name=None):
        for component in self.components:
            if component.path == os.getcwd():
                if board_name:
                    if self.components.get(board_name):
                        component.load_package()
                        component.hw_info.board_name = board_name
                    else:
                        put_string("board component `%s` not found in current workspace, please install it: yoc install %s " %(board_name, board_name))
                        exit(-1)
                components = self.components.get_depend(component)
                components.add(component)
                solution = Solution(components)

                return solution

    def download_component(self, name, update=True):
        if self.components.get(name) == None:
            if update:
                # self.occ_update()
                self.gitee_update()

            component = self.occ_components.get(name)
            if component:
                depends = self.occ_components.get_depend(component)
                depends.add(component)

                return depends

    def remove_component(self, name):
        component = self.components.get(name)
        if component:
            if not component.depends_on:                     # 如果没有组件依赖它
                for dep in component.depends:
                    p = self.components.get(dep)
                    if p:
                        if name in p.depends_on:
                            del p.depends_on[name]
                        self.remove_component(dep)

                shutil.rmtree(component.path)
                self.components.remove(component)
                return True
            else:
                logger.info("remove fail, %s depends on:" % component.name)
                for dep in component.depends_on:
                    logger.info('  ' + dep.name)
                return False

    def upload(self, name):
        component = self.components.get(name)
        if component:
            component.load_package()
            if not os.path.isdir(os.path.join(component.path, '.git')):
                if self.occ == None:
                    self.occ = OCC(self.conf)
                self.occ.login()
                zip_file = component.zip(self.yoc_path)
                if self.occ.upload(component.version, component.type, zip_file) == 0:
                    put_string("component upload success: " + component.name)
                else:
                    put_string("component upload fail: " + component.name)
                # self.save_version()

    def uploadall(self):
        if self.occ == None:
            self.occ = self.occ = OCC(self.conf)
        self.occ.login()
        for component in self.components:
            component.load_package()
            zip_file = component.zip(self.yoc_path)
            if self.occ.upload(component.version, component.type, zip_file) == 0:
                put_string("component upload success: " + component.name)
            else:
                put_string("component upload fail: " + component.name)

    def update(self):
        for component in self.components:
            component.load_package()
            component.download(self.yoc_path)

    def gitee_update(self):
        repo = RepoGitee(self.conf.gitee_token)
        self.occ_components = ComponentGroup()
        for p in repo.projects():
            pack = Component(self.conf)
            if type(p) == bytes:
                p = bytes.decode(p)
            pack.loader_json(json.loads(p))
            pack.path = os.path.join(self.conf.yoc_path, pack.path)
            self.occ_components.add(pack)
        with open(os.path.join(self.yoc_path, '.components.db'), "wb") as f:
            pickle.dump(self.occ_components, f)
            self.conf.save()

    def occ_update(self):
        if self.occ == None:
            self.occ = self.occ = OCC(self.conf)

            components, time = self.occ.yocComponentList(
                '614193542956318720', self.conf.lastUpdateTime)
            if components:
                self.occ_components = components
                self.conf.lastUpdateTime = time
                for component in self.occ_components:
                    component.path = os.path.join(
                        self.yoc_path, component.path)

                with open(os.path.join(self.yoc_path, '.components.db'), "wb") as f:
                    pickle.dump(self.occ_components, f)
                    self.conf.save()

    def list(self):
        for component in self.components:
            component.load_package()
            component.show()
            # if component.depends:
            #     put_string('  ', 'depends:')
            #     for v in component.depends:
            #         put_string('    -', v)
            # if component.depends_on:
            #     put_string('  ', 'depends_on:')
            #     for p in component.depends_on:
            #         put_string('    -', p.name)
