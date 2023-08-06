# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from yoctools import *


class Install(Command):
    common = True
    helpSummary = "Install component into project environment"
    helpUsage = """
%prog [option] [<component>...]
"""
    helpDescription = """
Install component into project environment
"""

    def _Options(self, p):
        self.jobs = 1
        p.add_option('-j', '--jobs',
                     dest='jobs', action='store', type='int',
                     help="projects to fetch simultaneously (default %d)" % self.jobs)

    def Execute(self, opt, args):
        yoc = YoC()
        components = ComponentGroup()
        if len(args) > 0:
            for name in args:
                depends = yoc.download_component(name)
                if depends:
                    for c in depends:
                        components.add(c)

        else:
            components = yoc.components

        if opt.jobs:
            jobs = opt.jobs
        else:
            jobs = 4
            self.download(jobs, components)

    def download(self, jobs, components):
        task_pool = threadpool.ThreadPool(jobs)

        tasks = []
        np = Progress('Fetching components', len(components))
        for component in components:
            component.np = np
            tasks.append(component)

        def thread_execture(component):
            component.np.update(msg=component.name)
            component.download()

        requests = threadpool.makeRequests(thread_execture, tasks)
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()

        np.end()
