# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Search(Command):
    common = True
    helpSummary = "Search for components whose name or summary contains <query>"
    helpUsage = """
%prog [option] <query>
"""
    helpDescription = """
Search for components whose name or summary contains <query>
"""

    def _Options(self, p):
        p.add_option('-u', '--upgrade',
                     dest='upgrade', action='store_true',
                     help='upgrade component from OCC')

    def Execute(self, opt, args):
        if len(args) != 1:
            self.Usage()

        yoc = YoC()
        if opt.upgrade or yoc.occ_components == None:
            yoc.gitee_update()

        for component in yoc.occ_components:
            search_text = args[0].lower()
            if component.name.lower().find(search_text) >= 0:
                component.show(key=[args[0]])
            else:
                component.load_package()
                if component.description.lower().find(search_text) >= 0:
                    component.show(key=[args[0]])
