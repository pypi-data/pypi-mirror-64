# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
from yoctools import *


class Upload(Command):
    common = True
    helpSummary = "Upload compoent to OCC"
    helpUsage = """
%prog [option] [<component>...]
"""
    helpDescription = """
upload compoent to OCC
"""

    def _Options(self, p):
        p.add_option('-g', '--git',
                     dest='update_git', action='store_true',
                     help='upload code to git repo')
        p.add_option('-o', '--occ',
                     dest='update_occ', action='store_true',
                     help='upload code to OCC')


    def Execute(self, opt, args):
        if not (opt.update_git or opt.update_occ):
            self.Usage()
            return

        yoc = YoC()
        count = len(args)
        if opt.update_git:
            repo = RepoGitee(yoc.conf.gitee_token)
            for component in yoc.components:
                if component.name in args or count == 0:
                    component.load_package()
                    ssh_url = repo.create_project(
                        component.name, component.json_dumps())
                    if ssh_url:
                        component.upload()

        if opt.update_occ:
            if count == 0:
                yoc.uploadall()
            else:
                for name in args:
                    yoc.upload(name)