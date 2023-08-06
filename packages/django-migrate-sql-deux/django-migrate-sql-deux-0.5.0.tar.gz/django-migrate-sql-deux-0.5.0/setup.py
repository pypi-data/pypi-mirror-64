#!/usr/bin/env python
import re
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex

        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


def get_version(package):
    """
    Get migrate_sql version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


with open('README.rst') as readme_file:
    readme = readme_file.read()


VERSION = get_version('migrate_sql')

setup(
    name='django-migrate-sql-deux',
    version=VERSION,
    description='Migration support for raw SQL in Django',
    long_description=readme,
    author='Festicket',
    author_email='dev@festicket.com',
    packages=find_packages(),
    package_dir={'migrate_sql': 'migrate_sql'},
    license='BSD',
    zip_safe=False,
    url='https://github.com/festicket/django-migrate-sql',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[],
)
