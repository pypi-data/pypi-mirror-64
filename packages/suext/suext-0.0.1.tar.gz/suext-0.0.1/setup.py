import os

from setuptools import setup, find_packages

SETUP_DIR = os.path.dirname(__file__)

with open(os.path.join(SETUP_DIR, 'README.rst'), 'rb') as f:
    README = f.read().decode('utf-8')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='suext',
    version='0.0.1',
    license='MIT',
    description=(
        'Utility for showing any file extension. '
        'Support show files extension in a directory.'
    ),
    long_description=README,
    url='https://github.com/arsensokolov/ext',
    author='Arseny Sokolov',
    author_email='me@arsen.pw',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'suext=suext:main'
        ]
    },
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
        'Topic :: System',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Shells',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: System Shells',
        'Topic :: Utilities'
    ],
)
