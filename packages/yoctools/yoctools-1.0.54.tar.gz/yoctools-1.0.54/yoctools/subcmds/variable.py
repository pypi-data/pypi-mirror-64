# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Variable(Command):
    common = True
    helpSummary = "Display variables for the current project"
    helpUsage = """
%prog [option] [<variable>...]
"""
    helpDescription = """
Display variables for the current project
"""
    def _Options(self, p):
        p.add_option('-b', '--board',
                     dest='board_name', action='store', type='str', default=None,
                     help='show all source code file')

    def Execute(self, opt, args):
        yoc = YoC()
        solution = yoc.getSolution(opt.board_name)
        if len(args) == 0:
            for k, v in solution.variables.items():
                put_string("%-10s = %s" % (k, v))
        else:
            for arg in args:
                var = solution.variables.get(arg)
                put_string(var)
