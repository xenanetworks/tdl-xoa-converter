Convert GUI Test Config into XOA
======================================================

To converter Xena RFC GUI test configuration files into XOA RFC json format, you need to do the following steps.


Step 1. Create Project Folder
------------------------------

First, create a folder on your computer at a location you want. This folder will be the place where you keep your XOA RFC test suites and a simple Python program to load and run them using XOA RFC test framework.

Let's create a folder called ``/my_xoa_project``

.. code-block::
    :caption: Create project folder

    /my_xoa_project
        |


Step 2. Create Necessary Files
--------------------------------

Create a ``main.py`` file inside the folder ``/my_xoa_project``.

Then, on the same level as ``main.py``, create a folder ``/pluginlib`` for keeping your test suites.

After that, create a ``__init__.py`` inside folder ``/pluginlib`` to make it into a `package <https://docs.python.org/3/tutorial/modules.html#packages>`_.

.. code-block::
    :caption: Create necessary files

    /my_xoa_project
        |
        |- main.py
        |- /pluginlib
            |- __init__.py
            |


Step 3. Install XOA RFC Core
-------------------------------------

If you have already installed XOA RFC Core in your system, either to your global namespace or in a virtual environment, you can skip this step.


Step 4. Copy XOA RFC Test Suite Plugin into Project Folder
-------------------------------------------------------------------

Copy a test suite plugin, e.g. ``/plugin2544`` from `XOA RFC Test Suite <https://github.com/xenanetworks/xena-rfc-test-suites>`_ into ``/my_xoa_project/pluginlib``.

Copy your test configuration ``json`` file, e.g. ``my2544_data.json`` into ``/my_xoa_project`` for easy access.

.. code-block::
    :caption: Copy test suite plugin into project

    /my_xoa_project
        |
        |- main.py
        |- my2544_data.json
        |- /pluginlib
            |- __init__.py
            |- /plugin2544


Step 5. Convert Test Config from Xena to XOA RFC
---------------------------------------------------------

First, import ``xoa_core`` and ``xoa_converter`` into your Python code.

.. code-block:: python

    from xoa_core import controller
    from xoa_converter.entry import converter
    from xoa_converter.types import TestSuiteType

Then, to use the converter, you need the target schema for the old file to be converted into. After that, simply provide the target schema, the old config file to the converter function and get the new config file:

.. literalinclude:: ../code_example/using_converter.py
    :language: python
    :emphasize-lines: 11, 22-23, 31-32, 35-36