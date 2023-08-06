import os
from suext import __version__
from setuptools import setup, find_packages

SETUP_DIR = os.path.dirname(__file__)

with open(os.path.join(SETUP_DIR, 'README.rst'), 'rb') as f:
    README = f.read().decode('utf-8')

with open(os.path.join(SETUP_DIR, 'requirements.txt'), 'r') as f:
    REQUIREMENTS = f.read()

# allow setup.py to be run from any  path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='suext',
    version=__version__,
    license='MIT',
    description=(
        'Utility for showing any file extension and MIME type info. '
        'Support show files information in a directory as list or table.'
    ),
    long_description=README,
    url='https://github.com/arsensokolov/ext',
    author='Arseny Sokolov',
    author_email='me@arsen.pw',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'suext=suext:_main'
        ]
    },
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
        'Operating System :: Microsoft :: Windows :: Windows XP',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Shells',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: System Shells',
        'Topic :: Utilities'
    ],
)
