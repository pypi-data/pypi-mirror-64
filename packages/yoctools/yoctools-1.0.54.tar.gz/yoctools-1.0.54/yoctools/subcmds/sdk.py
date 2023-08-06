# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
from yoctools import *


class Sdk(Command):
    common = True
    helpSummary = "Generate current solution SDK"
    helpUsage = """
%prog
"""
    helpDescription = """
generate current solution SDK.
"""
    # def _Options(self, p):
    #     p.add_option('-a', '--all',
    #                  dest='show_all', action='store_true',
    #                  help='show the complete list of commands')

    def Execute(self, opt, args):
        yoc = YoC()
        solution = yoc.getSolution()
        if solution:
            solution.install()
            pack = solution.solution_component.pack
            if pack:
                for d in solution.solution_component.depends:
                    pack.build_config.libs.append(d)
                pack.build_config.libpath.append('yoc_sdk/lib')
                pack.build_config.include.append('yoc_sdk/include')
                pack.depends = {}
                pack.hw_info.reset()
                pack.hw_info.cpu_name = solution.cpu_name
                pack.hw_info.ld_script = 'yoc_sdk/' + solution.ld_script_component.name + '/' + solution.ld_script_component.pack.hw_info.ld_script
                # text = pack.dumps()
                # print(text)
                pack.save()

