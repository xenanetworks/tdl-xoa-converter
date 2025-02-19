Installing XOA Converter
=====================================

XOA Converter is available to install and upgrade via the `Python Package Index <https://pypi.org/>`_. Alternatively, you can also install and upgrade from the source file.

* If you prefer installing/upgrading/uninstalling automatically, go to Section `From PyPi Using pip`_.
* If you prefer installing/upgrading manually, go to Section `Manually From Source`_.

Prerequisites
-------------

Before installing XOA Converter, please make sure your environment has installed `Python <https://www.python.org/>`_ and ``pip``.

Python
^^^^^^^

XOA Converter requires that you `install Python <https://realpython.com/installing-python/>`_ on your system.

.. note:: 

    XOA Converter requires Python >= 3.8.

``pip``
^^^^^^^

Make sure ``pip`` is installed on your system. ``pip`` is the `package installer for Python <https://packaging.python.org/guides/tool-recommendations/>`_ . You can use it to install packages from the `Python Package Index <https://pypi.org/>`_  and other indexes.

Usually, ``pip`` is automatically installed if you are:

* working in a `virtual Python environment <https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments>`_ (`virtualenv <https://virtualenv.pypa.io/en/latest/#>`_ or `venv <https://docs.python.org/3/library/venv.html>`_ ). It is not necessary to use ``sudo pip`` inside a virtual Python environment.
* using Python downloaded from `python.org <https://www.python.org/>`_ 

If you don't have ``pip`` installed, you can:

* Download the script, from https://bootstrap.pypa.io/get-pip.py.
* Open a terminal/command prompt, ``cd`` to the folder containing the ``get-pip.py`` file and run:

.. code-block:: console

    $ python3 get-pip.py

.. seealso::

    Read more details about this script in `pypa/get-pip <https://github.com/pypa/get-pip>`_.

    Read more about installation of ``pip`` in `pip installation <https://pip.pypa.io/en/stable/installation/>`_.


From PyPi Using ``pip``
------------------------

Install
^^^^^^^^

``pip`` is the recommended installer for XOA Converter. The most common usage of ``pip`` is to install from the `Python Package Index <https://pypi.org/>`_ using `Requirement Specifiers <https://pip.pypa.io/en/stable/cli/pip_install/#requirement-specifiers>`_.

.. code-block:: console

    $ pip install tdl-xoa-converter         # latest version
    $ pip install tdl-xoa-converter==1.0.1     # specific version
    $ pip install tdl-xoa-converter>=1.0.1     # minimum version

Upgrade
^^^^^^^^

To upgrade XOA Converter package from PyPI:

.. code-block:: console

    $ pip install tdl-xoa-converter -U


Uninstall
^^^^^^^^^^^

To uninstall XOA Converter using ``pip``:


.. code-block:: console

    $ pip uninstall tdl-xoa-converter

.. seealso::

    For more information, see the `pip uninstall <https://pip.pypa.io/en/stable/cli/pip_uninstall/#pip-uninstall>`_ reference.



Manually From Source
----------------------

Install or Upgrade
^^^^^^^^^^^^^^^^^^^

If for some reason you need to install or upgrade XOA Converter manually from source, the steps are:

First, make sure Python packages `wheel <https://wheel.readthedocs.io/en/stable/>`_ and  `setuptools <https://setuptools.pypa.io/en/latest/index.html>`_ are installed on your system. Install ``wheel`` and ``setuptools`` using ``pip``:


.. code-block:: console

    $ pip install wheel setuptools

Then, download the XOA Converter source distribution from `XOA Converter Releases <https://github.com/xenanetworks/tdl-xoa-converter/releases>`_. Unzip the archive and run the ``setup.py`` script to install the package:

.. code-block:: console

    $ python3 setup.py install


If you want to distribute, you can build ``.whl`` file for distribution from the source:

.. code-block:: console

    $ python3 setup.py bdist_wheel
