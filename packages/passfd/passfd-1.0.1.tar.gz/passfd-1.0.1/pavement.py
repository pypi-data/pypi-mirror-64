import errno
import os
from setuptools import Extension

from paver.easy import *
from paver.path import path
from paver.setuputils import setup


setup(
    name="passfd",
    description="send file descriptors over AF_UNIX sockets via sendmsg(2)",
    url="https://github.com/avocado-framework/avocado-vt",
    version="1.0.1",
    license="GPLv2",
    author="Virt-QE team",
    author_email="skycastlelily@gmail.com",
    ext_modules=[Extension(
        'passfd',
        ['passfd.c'],
        include_dirs=('.',),
        extra_compile_args=['-Wall'])],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: C",
        "Topic :: System :: Networking",
    ]
)

MANIFEST = (
    "LICENSE",
    "setup.py",
    "paver-minilib.zip",
    "passfd.c",
)

@task
def manifest():
    path('MANIFEST.in').write_lines('include %s' % x for x in MANIFEST)

@task
@needs('generate_setup', 'minilib', 'manifest', 'setuptools.command.sdist')
def sdist():
    pass

@task
def clean():
    for p in map(path, ('sendmsg.egg-info', 'dist', 'build', 'MANIFEST.in')):
        if p.exists():
            if p.isdir():
                p.rmtree()
            else:
                p.remove()
    for p in path(__file__).abspath().parent.walkfiles():
        if p.endswith(".pyc") or p.endswith(".pyo"):
            try:
                p.remove()
            except OSError, exc:
                if exc.args[0] == errno.EACCES:
                    continue
                raise
