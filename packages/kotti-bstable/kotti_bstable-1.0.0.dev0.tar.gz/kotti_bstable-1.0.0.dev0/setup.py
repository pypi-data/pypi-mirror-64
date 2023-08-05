# -*- coding: utf-8 -*-
import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    CHANGES = ''

version = '1.0.0'

install_requires = [
    'Kotti>=1.2.4',
    'kotti_tinymce',
]

tests_require = [
    'pytest-cov',
    'pytest-pep8',
    'mock',
    'webtest',
]


setup(
    name='kotti_bstable',
    version=version,
    description="Bootstraptable for Kotti",
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Pylons',
        'Framework :: Pyramid',
        'License :: Repoze Public License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Oshane Bailey',
    author_email='b4.oshany@gmail.com',
    url='https://github.com/b4oshany/kotti_bstable',
    keywords='kotti web cms wcms pylons pyramid sqlalchemy bootstrap',
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[],
    dependency_links=[],
    entry_points={
        'fanstatic.libraries': [
            'kotti_bstable = kotti_bstable.fanstatic:library',
        ],
    },
    extras_require={
        'tests': tests_require,
    },
)
