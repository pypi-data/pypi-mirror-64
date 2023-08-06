import fnmatch
import glob
import os
import sys

import setuptools.command.build_ext


APPLE = sys.platform == 'darwin'


BASE_DIR = os.path.dirname(__file__)
ABOUT = {}


def _read_about():
    with open(os.path.join(BASE_DIR, 'omnibus_dev', '__about__.py'), 'rb') as f:
        src = f.read()
        if sys.version_info[0] > 2:
            src = src.decode('UTF-8')
        exec(src, ABOUT)


_read_about()


PACKAGE_DATA = [
]


INSTALL_REQUIRES = [
]

EXTRAS_REQUIRE = {
}


EXT_MODULES = []


if __name__ == '__main__':
    setuptools.setup(
        name=ABOUT['__title__'],
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        python_requires='>=3.7',

        classifiers=[
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: ' + '.'.join(map(str, sys.version_info[:2])),
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python',
        ],

        # zip_safe=True,

        setup_requires=['setuptools'],

        packages=setuptools.find_packages(
            include=['omnibus_dev', 'omnibus_dev.*'],
            exclude=['tests', '*.tests', '*.tests.*'],
        ),
        py_modules=['omnibus_dev'],

        package_data={'omnibus_dev': PACKAGE_DATA},
        include_package_data=True,

        entry_points={},

        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,

        ext_modules=EXT_MODULES,
    )
