#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-archetype-base',
        version = '0.1.0',
        description = 'PyBuilder Python base project structure Plugin',
        long_description = 'External plugin for PyBuilder to generate a base project structure',
        author = 'Arturo GL, Diego BM',
        author_email = 'r2d2006@hotmail.com, diegobm92@gmail.com',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/yeuk0/pybuilder-archetype-base',
        scripts = [],
        packages = [
            'pybuilder_archetype_base',
            'pybuilder_archetype_base.resources',
            'pybuilder_archetype_base.resources.tests',
            'pybuilder_archetype_base.resources.utils.loggers'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {
            'pybuilder_archetype_base': ['resources/*', 'resources/config/*', 'resources/config/logger/*', 'resources/tests/*', 'resources/utils/*', 'resources/utils/loggers/*']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
