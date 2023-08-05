Command line playlist bookkeeping
=================================

When following multiple series, keeping track of which episodes were
watched can become a tedious task. This project aims to offload this
task to a database.

Installation
------------

Via `PyPI <https://pypi.python.org/pypi/playlistdb>`__:

::

   pip install playlistdb

From source:

::

   git clone https://github.com/jfjlaros/playlist.git
   cd playlist
   pip install .

Usage
-----

The program ``playlist`` is used to add and remove files and to set
configuration options per directory, i.e., for every directory a new
entry is added to the database.

The ``add`` command can be used to add files, any configuration specific
for these files can be added with the ``config`` subcommand.

::

   playlist add *.mkv
   playlist config '-sid 1'

This adds all files with extension ``.mkv`` to the database. The
configuration ``-sid 1``, a command line option for
`mplayer <http://www.mplayerhq.hu>`__, is added for the current
directory.

An overview of the database contents for the current directory can be
seen with the ``show`` subcommand.

::

   $ playlist show
   Playlist:
   * 00 - Credits.mkv
     00 - Intro.mkv
     01 - Episode 1.mkv
     02 - Episode 2.mkv
     03 - Episode 3.mkv

   Config: -sid 1

The ``*`` marks the current file, this file is next in line to be
played.

Entries can be removed by using the ``remove`` subcommand:

::

   playlist remove '00 - Credits.mkv'

The current file can be retrieved with the ``current`` subcommand and
set to a specific file with the ``set`` subcommand. The configuration
can be retrieved with ``show_config``:

::

   $ playlist current
   00 - Intro.mkv
   $ playlist set '01 - Episode 1.mkv'
   $ playlist current
   01 - Episode 1.mkv
   $ playlist show_config
   -sid 1

Finally, the ``next`` subcommand will show the current file and will set
the current file to the next entry.

::

   $ playlist next
   01 - Episode 1.mkv
   $ playlist next
   02 - Episode 2.mkv

The output of these commands can be passed to any program. It may be
convenient to make an alias for particular application, for example:

::

   alias playnext='mplayer $(playlist show_config) "$(playlist next)"'

Database
--------

The database is stored in ``$HOME/.cache/playlist/db.yml``. Since it is
stored in `YAML <https://en.wikipedia.org/wiki/Yaml>`__ format, it can
easily be modified using any text editor.

The database entry for our example looks as follows:

.. code:: yaml

   /media/Show:
     config: -sid 1
     files:
     - 00 - Intro.mkv
     - 01 - Episode 1.mkv
     - 02 - Episode 2.mkv
     - 03 - Episode 3.mkv
     offset: 3

The top-level key ``/media/Show`` is also the name of the directory that
contains the files to be played, the configuration for this directory is
stored in the ``config`` variable, the file list is stored in ``files``.
The ``offset`` variable contains the index of the current file. If this
index is larger or equal to the length of the list, then the playlist is
finished.
