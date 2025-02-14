Convert Xena RFC GUI Test Config into Xena Python RFC
======================================================

To converter your old test configuration files into new Xena Python RFC json format, you need to do the following steps.


Step 1. Create Project Folder
------------------------------

First, create a folder on your computer at a location you want. This folder will be the place where you keep your Xena Python RFC test suites and a simple Python program to load and run them using Xena Python RFC Core framework.

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


Step 3. Install Xena Python RFC Core
-------------------------------------

If you have already installed Xena Python RFC Core in your system, either to your global namespace or in a virtual environment, you can skip this step.

Read more about `` 


Step 4. Copy Xena Python RFC Test Suite Plugin into Project Folder
-------------------------------------------------------------------

Copy a test suite plugin, e.g. ``/plugin2544`` from `Xena Python RFC Test Suite <https://github.com/xenanetworks/xena-rfc-test-suites>`_ into ``/my_xoa_project/pluginlib``.

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


Step 5. Convert Test Config from Xena to Xena Python RFC
---------------------------------------------------------

First, import ``xena-rfc-core`` and ``xena-rfc-converter`` into your Python code. If you haven't installed ``xena-rfc-core`` Python package in your environment, please go to `Xena Python RFC Core <https://github.com/xenanetworks/xena-python-rfc-core>`_.

.. code-block:: python

    from xena-rfc-core import controller
    from xena-rfc-converter.entry import converter
    from xena-rfc-converter.types import TestSuiteType

Then, to use the converter, you need the target schema for the old file to be converted into. After that, simply provide the target schema, the old config file to the converter function and get the new config file:

.. literalinclude:: ../code_example/using_converter.py
    :language: python
    :emphasize-lines: 11, 22-23, 31-32, 35-36