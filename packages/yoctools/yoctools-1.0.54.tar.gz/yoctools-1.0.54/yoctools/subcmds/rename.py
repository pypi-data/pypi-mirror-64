# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *
import os


class Rename(Command):
    common = True
    helpSummary = "Component rename <old_name> to <new_name>"
    helpUsage = """
%prog <old_name> <new_name>
"""
    helpDescription = """
Component rename <old_name> to <new_name>.
"""

    def Execute(self, opt, args):
        yoc = YoC()
        if len(args) == 2:
            old_name = args[0]
            new_name = args[1]
            component = yoc.components.get(old_name)
            if component:
                dep_on = yoc.check_depend_on(component)
                if component.rename(new_name):
                    for c in dep_on:
                        for v in c.pack.depends:
                            if old_name in v:
                                c.pack.depends.remove(v)
                        c.pack.depends.append({component.name: component.version})
                        c.pack.save()
                        put_string("component %s package.yaml is upgraded." % c.name)
                    put_string("component `%s` -> `%s` success." % (old_name, new_name))
                else:
                    put_string("component rename fail.")
            else:
                put_string("component `%s` not found." % old_name)

