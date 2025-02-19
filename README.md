![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tdl-xoa-converter) [![PyPI](https://img.shields.io/pypi/v/tdl-xoa-converter)](https://pypi.python.org/pypi/tdl-xoa-converter) ![GitHub](https://img.shields.io/github/license/xenanetworks/tdl-xoa-converter) [![Documentation Status](https://readthedocs.com/projects/xena-networks-tdl-xoa-converter/badge/?version=latest)](https://docs.xenanetworks.com/projects/tdl-xoa-converter/en/latest/?badge=latest)

# XOA Converter

XOA Converter is a supporting tool for you to quickly migrate your Xena Windows desktop RFC test suite configurations into XOA RFC.

## Introduction

The XOA Converter is an open-source tool hosted on Xena Networks' GitHub repository. It is designed to help you migrate your Xena Windows desktop RFC test suite configurations into XOA RFC test suites, enabling a seamless transition to the XOA RFC ecosystem for network automation and testing.

Key features of the XOA Converter include:

1. Conversion support: The tool supports conversion of Valkyrie test suite configuration files to XOA RFC-compatible format, facilitating the integration of existing test cases into the XOA RFC framework.

2. Ease of use: The XOA Converter is designed to be user-friendly, with a straightforward process for converting test suite configuration files.

3. Compatibility: The converter ensures that the migrated test suite configurations are compatible with XOA RFC Core and can be executed within the XOA RFC ecosystem.

> The purpose of XOA Converter is ONLY to convert Xena Windows desktop test suite RFC configuration files into XOA RFC configuration files. Thus only four test suite types are supported by XOA Converter as the source config files. 

# Documentation

The user documentation is hosted:
[XOA Converter Documentation](https://docs.xenanetworks.com/projects/tdl-xoa-converter)


# Installation

## Install Using pip

Make sure Python ``pip`` is installed on you system. If you are using virtualenv, then pip is already installed into environments created by virtualenv, and using sudo is not needed. If you do not have pip installed, download this file: https://bootstrap.pypa.io/get-pip.py and run ``python get-pip.py``.

To install/upgrade:

``` shell
pip install tdl-xoa-converter -U
```

## Install From Source Code

Make sure these packages are installed ``wheel``, ``setuptools`` on your system.

``` shell
pip install wheel setuptools
```


To install from source of python packages:

``` shell
python setup.py install
```


## Build From Source Code for Distribution

If you want to build a ``.whl`` file for distribution, you can use the following command:

``` shell
python setup.py bdist_wheel
```

## Quick Start

Here is a quick start guide to get you started with XOA Converter:

Install the latest version of XOA Converter using pip:

``` shell
pip install tdl-xoa-converter -U
```

Code example to convert `.x2544` into XOA RFC 2544 test configuration:

``` python
import asyncio
import json
from xoa_core import controller
from xoa_converter.entry import converter
from xoa_converter.types import TestSuiteType

async def start():
    SOURCE_CONFIG_FILE = "my_old2544_config.x2544" # source config file to be converted

    core_ctrl = await controller.MainController() # create an instance of xoa rfc core controller
    info = core_ctrl.get_test_suite_info("RFC-2544") # get 2544 test suite information from the core's registration
    target_schema = json.load(info['schema']) # get the target json schema

    with open(SOURCE_CONFIG_FILE, 'r') as source_data_file:
        target_config = converter(
            test_suite_type=TestSuiteType.RFC2544, 
            source_config=source_data_file.read(), 
            target_schema=target_schema
        )
        print(target_config)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
```