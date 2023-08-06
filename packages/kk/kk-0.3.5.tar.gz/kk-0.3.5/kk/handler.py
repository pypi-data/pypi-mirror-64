#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2020-03-27 21:17:57
'''
import asyncio
import datetime
import hashlib
import io
import math
import shutil
import tempfile
import urllib.parse
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import markdown
import tornado.web
import yaml
from bson import ObjectId
from tornado.concurrent import run_on_executor
from tornado_utils import BaseHandler
from tornado_utils import Blueprint
from utils import Dict

bp = Blueprint(__name__)


class BaseHandler(BaseHandler):

    default = {
        'ppt.png': ['.ppt', '.pptx'],
        'word.png': ['.doc', '.docx'],
        'excel.png': ['.xls', '.xlsx'],
        'pdf.png': ['.pdf'],
        'txt.png': ['.txt'],
        'vue.png': ['.vue'],
        'exe.png': ['.exe'],
        'apk.png': ['.apk'],
        'iso.png': ['.iso'],
        'json.png': ['.json', '.yml', '.yaml'],
        'ini.png': ['.ini'],
        'markdown.png': ['.md'],
        'database.png': ['.db', '.sql'],
        'image.png': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.svg', '.ai'],
        'audio.png': ['.amr', '.ogg', '.wav', '.mp3'],
        'video.png': ['.rmvb', '.rm', '.mkv', '.mp4', '.avi', '.wmv', '.flv', '.m3u8'],
        'rar.png': ['.rar', '.tar', '.tgz', '.gz', '.bz2', '.bz', '.xz', '.zip', '.7z'],
        'language-c.png': ['.c', '.h'],
        'language-cpp.png': ['.cpp'],
        'language-csharp.png': ['.cs'],
        'language-python.png': ['.py', '.pyc'],
        'language-bash.png': ['.sh'],
        'language-go.png': ['.go'],
        'language-java.png': ['.java', '.javac', '.class', '.jar'],
        'language-javascript.png': ['.js'],
        'language-html5.png': ['.html'],
        'language-css.png': ['.css', '.less', '.sass', '.scss'],
    }
    icon = {}
    for key, value in default.items():
        for v in value:
            icon[v] = key


@bp.route('/')
class IndexHandler(BaseHandler):

    def get(self):
        if self.app.options.auth:
            if self.current_user:
                self.redirect(f'/disk/{self.current_user.id}')
            else:
                self.redirect(self.get_login_url())
        else:
            self.redirect('/disk')


@bp.route('/share')
class ShareHandler(BaseHandler):

    async def get(self):
        if self.app.options.auth:
            if self.current_user:
                docs = await self.query('files', {'token': self.current_user.token})
                entries = []
                for doc in docs:
                    entries.append(Dict({
                        'path': Path(doc.path),
                        'mtime': doc.mtime,
                        'size': doc.size,
                        'suffix': Path(doc.path).suffix.lower(),
                        'is_dir': doc.is_dir,
                        'key': doc._id,
                    }))
                self.render('index.html', entries=entries, absolute=True)
            else:
                self.redirect(self.get_login_url())
        else:
            self.redirect('/disk')


@bp.route('/disk/?(.*)')
class DiskHandler(tornado.web.StaticFileHandler, BaseHandler):

    executor = ThreadPoolExecutor(10)

    def __init__(self, application, request, **kwargs):
        tornado.web.StaticFileHandler.__init__(self, application, request, path=self.app.root)
        BaseHandler.__init__(self, application, request, path=self.app.root)

    def compute_etag(self):
        if hasattr(self, 'absolute_path'):
            return super().compute_etag()

    @run_on_executor
    def search(self, name):
        entries = []
        q = self.args.q.lower()
        for key, files in self.app.cache.items():
            if self.app.options.auth and not str(key).startswith(name):
                continue
            for doc in files[1]:
                if doc[0].name.lower().find(q) >= 0:
                    entries.append(doc)
        doc = self.get_args(page=1, count=50)
        self.args.total = len(entries)
        self.args.pages = int(math.ceil(len(entries) / doc.count))
        entries = entries[(doc.page - 1) * doc.count:doc.page * doc.count]
        return entries

    @run_on_executor
    def listdir(self, root):
        entries = self.app.scan_dir(root)
        doc = self.get_args(page=1, count=50)
        self.args.total = len(entries)
        self.args.pages = int(math.ceil(len(entries) / doc.count))
        entries = entries[(doc.page - 1) * doc.count:doc.page * doc.count]
        return entries

    @run_on_executor
    def download(self, root):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        filename = urllib.parse.quote(root.name)
        stream = io.BytesIO()
        zf = zipfile.ZipFile(stream, 'a', zipfile.ZIP_DEFLATED, False)
        for f in root.rglob('*'):
            if f.is_file():
                zf.writestr(str(f.relative_to(root)), f.read_bytes())
        #  Mark the files as having been created on Windows so that Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0
        zf.close()
        data = stream.getvalue()
        stream.close()
        self.set_header('Content-Disposition', f'attachment;filename={filename}.zip')
        self.finish(data)

    def get_nodes(self, root):
        nodes = []
        if root in self.app.cache:
            entries = self.app.cache[root][1]
            for doc in entries:
                if doc.is_dir:
                    nodes.append({'title': doc.path.name, 'href': f'/disk/{doc.path}', 'children': self.get_nodes(doc.path)})
                else:
                    nodes.append({'title': doc.path.name, 'href': f'/disk/{doc.path}'})
        return nodes

    def set_headers(self):
        super().set_headers()
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')

    def send_html(self, html):
        self.finish(f'''<html><head>
<link rel="stylesheet" href="/static/bower_components/highlightjs/styles/monokai_sublime.css">
</head><body style="margin:0;width:100%;height:100%">{html}
<script src="/static/bower_components/highlightjs/highlight.pack.min.js"></script>
<script>hljs.initHighlightingOnLoad()</script>
</body></html>''')

    async def check_auth(self, name):
        if not self.app.options.auth:
            return True

        if not self.current_user:
            if not self.args.key or self.request.method not in ['GET', 'HEAD']:
                raise tornado.web.HTTPError(403)
            else:
                doc = await self.db.files.find_one({'_id': ObjectId(self.args.key)})
                if not (doc and name.startswith(doc.name)):
                    raise tornado.web.HTTPError(403)
        elif name.split('/')[0] != str(self.current_user.id):
            raise tornado.web.HTTPError(403)

    async def get(self, name, include_body=True):
        await self.check_auth(name)
        path = self.root / name
        if self.args.q:
            entries = await self.search(name)
            self.render('index.html', entries=entries, absolute=True)
        elif self.args.f == 'tree':
            nodes = self.get_nodes(path)
            self.finish({'nodes': nodes})
        elif self.args.f == 'download':
            self.set_header('Content-Type', 'application/octet-stream')
            filename = urllib.parse.quote(path.name)
            if path.is_file():
                self.set_header('Content-Disposition', f'attachment;filename={filename}')
                await super().get(name, include_body)
            else:
                await self.download(path)
        elif path.is_file():
            if self.args.f == 'preview':
                if path.suffix.lower() in ['.yml', '.yaml']:
                    doc = yaml.load(open(path))
                    self.finish(doc)
                elif path.suffix.lower() == '.md':
                    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables', 'markdown.extensions.toc']
                    html = markdown.markdown(path.read_text(), extensions=exts)
                    self.send_html(html)
                elif path.suffix.lower() == '.ipynb':
                    with tempfile.NamedTemporaryFile('w+', suffix=f'.html', delete=True) as fp:
                        command = f'jupyter nbconvert --to html --template full --output {fp.name} {path}'
                        dl = await asyncio.create_subprocess_shell(command)
                        await dl.wait()
                        self.finish(fp.read().replace('<link rel="stylesheet" href="custom.css">', ''))
                elif path.suffix.lower() in ['.py', '.sh', '.h', '.c', '.cpp', '.js', '.css', '.html', '.java', '.go', '.ini', '.vue']:
                    self.send_html(f'''<pre><code>{ tornado.escape.xhtml_escape(path.read_text()) }</code></pre>''')
                elif path.suffix.lower() in ['.mp4', '.flv', '.m3u8']:
                    url = self.request.path
                    if self.app.options.auth:
                        url += '?token=' + (self.args.key or self.current_user.token)
                    html = [
                        '<html><head>',
                        '<link rel="stylesheet" href="/static/src/css/DPlayer.min.css">',
                        '</head><body>',
                        '<div id="video"></div>',
                        '<script src="/static/src/js/flv.min.js"></script>',
                        '<script src="/static/src/js/hls.min.js"></script>',
                        '<script src="/static/src/js/DPlayer.min.js"></script>',
                        '<script>new DPlayer({container: document.getElementById("video"), autoplay: true, video: { type: "auto", url: "' + url + '" } })</script>',
                        '</body></html>'
                    ]
                    self.send_html(''.join(html))
                else:
                    await super().get(name, include_body)
            else:
                await super().get(name, include_body)
        else:
            entries = await self.listdir(path)
            self.render('index.html', entries=entries, absolute=False)

    async def merge(self, path):
        dirname = Path(f'/tmp/{self.args.guid}')
        filename = path / self.args.name
        filename.parent.mkdir(parents=True, exist_ok=True)
        chunks = int(list(dirname.glob("*"))[0].name.split('_')[0])
        md5 = hashlib.md5()
        with filename.open('wb') as fp:
            for i in range(int(chunks)):
                chunk = dirname / f'{chunks}_{i}'
                data = chunk.read_bytes()
                md5.update(data)
                fp.write(data)
        md5 = md5.hexdigest()
        if self.args.md5 and self.args.md5 != 'undefined' and self.args.md5 != md5:
            self.finish({'err': 1, 'msg': f'check md5 failed'})
        else:
            shutil.rmtree(dirname)
            self.finish({'err': 0})

    async def upload(self, path):
        if self.args.action == 'merge':
            await self.merge(path)
        elif self.args.chunks and self.args.chunk:
            filename = Path(f'/tmp/{self.args.guid}/{self.args.chunks}_{self.args.chunk}')
            filename.parent.mkdir(parents=True, exist_ok=True)
            filename.write_bytes(self.request.files['file'][0].body)
            self.finish({'err': 0})
        else:
            path.mkdir(parents=True, exist_ok=True)
            for items in self.request.files.values():
                for item in items:
                    filename = path / item.filename
                    filename.write_bytes(item.body)
            self.finish({'err': 0})

    async def post(self, name):
        await self.check_auth(name)
        path = self.root / name
        if self.args.action and not path.exists():
            self.finish({'err': 1, 'msg': f'{name} not exists'})
        elif self.args.action == 'rename':
            if self.args.filename.find('/') >= 0:
                return self.finish({'err': 1, 'msg': '文件名不可包含/'})
            new_path = path.parent / self.args.filename
            if new_path.exists():
                self.finish({'err': 1, 'msg': '文件名重复'})
            else:
                path.rename(new_path)
                self.finish({'err': 0})
        elif self.args.action == 'move':
            home_dir = self.root / str(self.current_user.id) if self.app.options.auth else self.root
            new_path = home_dir / self.args.dirname.lstrip('/') / path.name
            if not new_path.parent.exists():
                new_path.parent.mkdir(parents=True, exist_ok=True)
            elif new_path.parent.is_file():
                return self.finish({'err': 1, 'msg': '目标文件夹为文件'})
            path.rename(new_path)
            self.finish({'err': 0})
        elif self.args.action == 'share':
            url = f'{self.request.host}/disk/{name}'
            if not self.app.options.auth:
                self.finish({'err': 0, 'url': url})
            else:
                doc = await self.db.files.find_one({'token': self.current_user.token, 'name': name})
                if not doc:
                    filesize = path.stat().st_size
                    if filesize / (1024 * 1024 * 1024.0) >= 1:
                        size = '%.1f GB' % (filesize / (1024 * 1024 * 1024.0))
                    elif filesize / (1024 * 1024.0) >= 1:
                        size = '%.1f MB' % (filesize / (1024 * 1024.0))
                    else:
                        size = '%.1f KB' % (filesize / 1024.0)
                    doc = {
                        'token': self.current_user.token,
                        'name': name,
                        'path': str(path.relative_to(self.root)),
                        'mtime': path.stat().st_mtime,
                        'size': size,
                        'is_dir': path.is_dir(),
                        'created_at': datetime.datetime.now().replace(microsecond=0)
                    }
                    doc = await self.db.files.find_one_and_update({'token': self.current_user.token, 'name': name},
                                                                  {'$set': doc},
                                                                  upsert=True,
                                                                  return_document=True)
                self.finish({'err': 0, 'url': f'{url}?key={doc._id}'})
        elif self.args.action == 'unshare':
            if not self.app.options.auth:
                self.finish({'err': 0})
            else:
                await self.db.files.delete_one({'token': self.current_user.token, 'name': name})
                self.finish({'err': 0})
        elif self.args.action == 'delete':
            await self.delete(name)
        else:
            await self.upload(path)

    async def delete(self, name):
        await self.check_auth(name)
        path = self.root / name
        if not path.exists():
            return self.finish({'err': 1, 'msg': f'{name} not exists'})
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)
        self.finish({'err': 0})
