#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2020-03-27 21:40:13
'''
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from apscheduler.schedulers.tornado import TornadoScheduler
from handler import bp as bp_disk
from tornado.options import define
from tornado.options import options
from tornado_utils import Application
from tornado_utils import bp_user
from utils import AioEmail
from utils import Dict
from utils import Motor

define('root', default='.', type=str)
define('auth', default=False, type=bool)


class Application(Application):

    async def initialize(self):
        self.opt = Dict()
        self.email = AioEmail()
        self.db = Motor('pan')
        self.root = Path(options.root)
        self.cache = {}
        self.scan()
        self.sched = TornadoScheduler()
        self.sched.add_job(self.scan, 'cron', minute='0', hour='*')
        self.sched.start()

    def scan_dir(self, root):
        if not root.exists():
            return []
        st_mtime = root.stat().st_mtime
        if root in self.cache and st_mtime == self.cache[root][0]:
            entries = self.cache[root][1]
        else:
            entries = []
            for item in root.iterdir():
                if not item.exists():
                    continue
                if item.name.startswith('.'):
                    continue
                path = item.relative_to(self.root)
                stat = item.stat()
                filesize = stat.st_size
                if filesize / (1024 * 1024 * 1024.0) >= 1:
                    size = '%.1f GB' % (filesize / (1024 * 1024 * 1024.0))
                elif filesize / (1024 * 1024.0) >= 1:
                    size = '%.1f MB' % (filesize / (1024 * 1024.0))
                else:
                    size = '%.1f KB' % (filesize / 1024.0)
                mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
                entries.append(Dict({
                    'path': path,
                    'mtime': mtime,
                    'size': size,
                    'is_dir': item.is_dir(),
                }))
            entries.sort(key=lambda x: str(x.path).lower())
            self.cache[root] = [st_mtime, entries]

        return entries

    def scan_thread(self):
        self.scan_dir(self.root)
        for f in self.root.rglob('*'):
            if f.is_dir():
                self.scan_dir(f)

    def scan(self):
        dirs = [self.root] + [f for f in self.root.rglob('*') if f.is_dir()]
        with ThreadPoolExecutor(10) as executor:
            executor.map(self.scan_dir, dirs)
        self.logger.info(f'scan result: {len(self.cache)} dirs')


def main():
    app = Application()
    app.register(bp_disk, bp_user)
    app.run(max_buffer_size=1024 * 1024 * 1024)


if __name__ == '__main__':
    main()
