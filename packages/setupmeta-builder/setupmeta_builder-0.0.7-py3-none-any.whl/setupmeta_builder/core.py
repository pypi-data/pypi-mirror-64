# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# all attrs from spec:
# https://packaging.python.org/guides/distributing-packages-using-setuptools/
# ----------

import os
import json
import subprocess
from pathlib import Path
from collections import ChainMap

import fsoopify

from .licenses import LICENSES
from .requires_resolver import DefaultRequiresResolver
from .version_resolver import update_version
from .utils import get_global_funcnames

class SetupAttrContext:
    def __init__(self, root_path=None):
        self._setup_attrs = {}
        self._root_path = Path(root_path) if root_path else Path.cwd()
        self._state = {}
        self._pkgit_conf: dict = None

    @property
    def setup_attrs(self):
        return self._setup_attrs

    @property
    def root_path(self):
        return self._root_path

    @property
    def state(self):
        '''
        a dict for store cached state.
        '''
        return self._state

    def get_fileinfo(self, relpath: str) -> fsoopify.FileInfo:
        '''get `FileInfo`.'''
        return fsoopify.FileInfo(str(self._root_path / relpath))

    def get_text_content(self, relpath: str) -> str:
        '''get file content or `None`'''
        fileinfo = self.get_fileinfo(relpath)
        if fileinfo.is_file():
            return fileinfo.read_text()

    def get_pkgit_conf(self) -> dict:
        if self._pkgit_conf is None:
            global_conf_path = Path.home() / '.pkgit.json'
            if global_conf_path.is_file():
                global_conf = json.loads(global_conf_path.read_text('utf-8'))
            else:
                global_conf = {}

            cwd_conf_text = self.get_text_content('.pkgit.json')
            if cwd_conf_text:
                cwd_conf = json.loads(cwd_conf_text)
            else:
                cwd_conf = {}

            self._pkgit_conf = ChainMap(cwd_conf, global_conf)

        return self._pkgit_conf

    def _run_git(self, argv: list):
        gitdir = str(self.root_path / '.git')
        argv = ['git', f'--git-dir={gitdir}'] + argv
        return subprocess.run(argv, encoding='utf-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


class SetupMetaBuilder:
    will_update_attrs = [
        'packages',
        'py_modules',
        'long_description',
        'name',
        'version',
        'author',
        'author_email',
        'url',
        'license',
        'classifiers',
        'scripts',
        'entry_points',
        'zip_safe',
        'include_package_data',
        'setup_requires',
        'install_requires',
        'tests_require',
        'extras_require',
    ]

    def __init__(self):
        self.requires_resolver = DefaultRequiresResolver()
        from .classifiers import IClassifierUpdater
        self.classifier_updaters = [
            cls() for cls in IClassifierUpdater.All
        ]

    def fill_ctx(self, ctx: SetupAttrContext):
        for attr in self.will_update_attrs:
            if attr not in ctx.setup_attrs:
                getattr(self, f'update_{attr}')(ctx)

    def update_packages(self, ctx: SetupAttrContext):
        from setuptools import find_packages

        ctx.setup_attrs['packages'] = find_packages(where=str(ctx.root_path))

    def update_py_modules(self, ctx: SetupAttrContext):
        # description:
        # https://packaging.python.org/guides/distributing-packages-using-setuptools/#py-modules
        #   If your project contains any single-file Python modules that aren’t part of a package,
        #   set py_modules to a list of the names of the modules (minus the .py extension)
        #   in order to make setuptools aware of them.

        packages = ctx.setup_attrs['packages']
        if packages:
            return # only discover if no packages.

        proj_name = ctx.root_path.name

        py_modules = []
        search_names = []
        search_names.append(proj_name)
        if proj_name.startswith('python-'):
            search_names.append(proj_name[len('python-'):])
        if proj_name.endswith('-python'):
            search_names.append(proj_name[:-len('-python')])
        for name in search_names:
            if ctx.get_fileinfo(f'{name}.py').is_file():
                py_modules.append(name)
                break

        if py_modules:
            ctx.setup_attrs['py_modules'] = py_modules

    def update_long_description(self, ctx: SetupAttrContext):
        rst = ctx.get_text_content('README.rst')
        if rst is not None:
            ctx.setup_attrs['long_description'] = rst
            return

        md = ctx.get_text_content('README.md')
        if md is not None:
            ctx.setup_attrs['long_description'] = md
            ctx.setup_attrs['long_description_content_type'] = 'text/markdown'
            return

        ctx.setup_attrs.setdefault('long_description', '')

    def update_name(self, ctx: SetupAttrContext):
        def parse_name():
            packages = ctx.setup_attrs.get('packages')
            if packages:
                ns = set()
                for pkg in packages:
                    ns.add(pkg.partition('.')[0])
                if len(ns) > 1:
                    raise RuntimeError(f'unable to pick name from: {ns}')
                return list(ns)[0]

            py_modules = ctx.setup_attrs.get('py_modules')
            if py_modules:
                ns = set()
                for mod in py_modules:
                    ns.add(mod.partition('.')[0])
                if len(ns) > 1:
                    raise RuntimeError(f'unable to pick name from: {ns}')
                return list(ns)[0]

            raise RuntimeError(f'unable to parse name: no packages or modules found')

        name = parse_name()
        if name:
            ctx.setup_attrs['name'] = name

    def update_version(self, ctx: SetupAttrContext):
        update_version(ctx)

    def update_author(self, ctx: SetupAttrContext):
        author = ctx.get_pkgit_conf().get('author')
        if author:
            ctx.setup_attrs['author'] = author

    def update_author_email(self, ctx: SetupAttrContext):
        author_email = ctx.get_pkgit_conf().get('author_email')
        if author_email:
            ctx.setup_attrs['author_email'] = author_email

    def update_url(self, ctx: SetupAttrContext):
        def get_url_from_remote(name):
            git_remote_get_url = ctx._run_git(['remote', 'get-url', name])
            if git_remote_get_url.returncode != 0:
                return
            return git_remote_get_url.stdout.strip()

        git_remote = ctx._run_git(['remote'])
        if git_remote.returncode != 0:
            return
        lines = git_remote.stdout.strip().splitlines()
        if 'origin' in lines:
            git_url = get_url_from_remote('origin')
        else:
            git_url = None

        if git_url:
            from .utils import parse_homepage_from_git_url
            url = parse_homepage_from_git_url(git_url)
            if url:
                ctx.setup_attrs['url'] = url


    def update_license(self, ctx: SetupAttrContext):
        from .licenses import update_license
        update_license(ctx)

    def update_classifiers(self, ctx: SetupAttrContext):
        # see: https://pypi.org/classifiers/
        classifiers = []

        for updater in self.classifier_updaters:
            updater.update_classifiers(ctx, classifiers)

        ctx.setup_attrs['classifiers'] = list(sorted(set(classifiers)))

    def update_scripts(self, ctx: SetupAttrContext):
        pass

    def update_entry_points(self, ctx: SetupAttrContext):
        entry_points = {}
        console_scripts = self._get_entry_points_console_scripts(ctx)
        if console_scripts:
            entry_points['console_scripts'] = console_scripts
        ctx.setup_attrs['entry_points'] = entry_points

    def _get_entry_points_console_scripts(self, ctx: SetupAttrContext):
        name = ctx.setup_attrs.get('name')
        console_scripts = []
        if name:
            csf = ctx.get_fileinfo(os.path.join(name, 'entry_points_console_scripts.py'))
            if csf.is_file():
                for fn in get_global_funcnames(csf):
                    if not fn.startswith('_'):
                        script_name = fn.replace('_', '-')
                        console_scripts.append(
                            f'{script_name}={name}.entry_points_console_scripts:{fn}'
                        )
        return console_scripts

    def update_zip_safe(self, ctx: SetupAttrContext):
        ctx.setup_attrs['zip_safe'] = False

    def update_include_package_data(self, ctx: SetupAttrContext):
        ctx.setup_attrs['include_package_data'] = True

    def update_setup_requires(self, ctx: SetupAttrContext):
        pass

    def update_install_requires(self, ctx: SetupAttrContext):
        requires = self.requires_resolver.resolve_install_requires(ctx)
        if requires is not None:
            ctx.setup_attrs['install_requires'] = requires

    def update_tests_require(self, ctx: SetupAttrContext):
        requires = self.requires_resolver.resolve_tests_require(ctx)
        if requires is not None:
            ctx.setup_attrs['tests_require'] = requires

    def update_extras_require(self, ctx: SetupAttrContext):
        requires = self.requires_resolver.resolve_extras_require(ctx)
        if requires is not None:
            ctx.setup_attrs['extras_require'] = requires
