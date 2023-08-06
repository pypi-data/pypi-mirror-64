*****************
``suext`` Utility
*****************

**Installation**

``pip install suext``

**Usage:**

- ``suext [-t|--table] [-m|--mime] [-d|--description] <filename>``
- ``suext [-t|--table] [-m|--mime] [-d|--description] <dirname>``
- ``suext -h|--help``
- ``suext -v|--version``

**Options:**

- ``<filename>`` Full or relative path to filename for showing file extension.
- ``<dirname>`` Full or relative path to directory for showing all files extension in this directories.
- ``-t --table`` Display result as table.
- ``-m --mime`` Display mime type.
- ``-d --description`` Display mime type description.
- ``-h --help`` Show help screen.
- ``-v --version`` Show current utility version.

Examples
****************

**Get 1 file extension:**

``$ suext README.rst``

Output:

``rst``

**Get file extension with filename and MIME type:**

``$ suext -m README.rst``

Output:

::

    README.rst
    rst
    text/plain

**Get file extension with filename and MIME description:**

``$ suext -d README.rst``

Output:

::

    README.rst
    rst
    ASCII text

**Get file extension with filename, MIME type and descriptin as table:**

``$ suext -t -m -d README.rst``

Output:

::

    File name    File extension    MIME type    MIME description
    -----------  ----------------  -----------  ------------------
    README.rst   rst               text/plain   ASCII text

**Get files extensions with filenames, MIME types and descriptions in current directory as table:**

``$ suext -t -m -d .``

Output:

::

    File name         File extension    MIME type                 MIME description
    ----------------  ----------------  ------------------------  ------------------------------------------------
    .gitignore        gitignore         text/plain                ASCII text
    LICENSE           LICENSE           text/plain                ASCII text
    README.rst        rst               text/plain                ASCII text
    requirements.txt  txt               text/plain                ASCII text
    setup.py          py                text/x-python             Python script, ASCII text executable
    suext.py          py                text/x-python             Python script, ASCII text executable
    suext.pyc         pyc               application/octet-stream  python 2.7 byte-compiled
    upload.sh         sh                text/x-shellscript        Bourne-Again shell script, ASCII text executable
