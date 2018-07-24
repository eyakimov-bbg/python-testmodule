from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

import re
import os.path
import sys

class cythonize_build_ext(build_ext):
    user_options = build_ext.user_options + [
        ('cythonize', None, 'run cythonize before building extensions.'),
    ]
    boolean_options = build_ext.boolean_options + ['cythonize']

    def initialize_options(self):
        super(cythonize_build_ext, self).initialize_options()
        self.cythonize = False

    def finalize_options(self):
        if self.distribution.ext_modules:
            if self.cythonize:
                self._cythonize()

        super(cythonize_build_ext, self).finalize_options()

    def _cythonize(self):
        try:
            from Cython.Build import cythonize
        except ImportError:
            print("You must first install cython to use --cythonize")
            sys.exit(1)

        def pyx_if_exists(source):
            pyx = re.sub("\.c$|\.cpp$", ".pyx", source)
            if os.path.isfile(pyx):
                return pyx
            return source

        for mod in self.distribution.ext_modules:
            mod.sources = list(map(pyx_if_exists, mod.sources))

        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules, include_path=['declarations'])


setup(
    name='testlib',
    description='testlib',
    version='0.1.0',
    author='Evgeny Yakimov',
    author_email='eyakimov@bloomberg.net',
    packages=['testlib'],
    cmdclass={"build_ext": cythonize_build_ext},
    ext_modules=[Extension(
        'testlib.puts',
        sources=['testlib/puts.c'],
    )])
