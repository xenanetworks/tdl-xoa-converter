![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xena-rfc-converter) [![PyPI](https://img.shields.io/pypi/v/xena-rfc-converter)](https://pypi.python.org/pypi/xena-rfc-converter) ![GitHub](https://img.shields.io/github/license/xenanetworks/xena-python-rfc-converter) [![Documentation Status](https://readthedocs.com/projects/xena-networks-xena-python-rfc-converter/badge/?version=latest)](https://docs.xenanetworks.com/projects/xena-python-rfc-converter/en/latest/?badge=latest)

# Xena Python RFC Converter

Xena Python RFC Converter is a supporting tool for you to quickly migrate your Xena Windows desktop RFC test suite configurations into Xena Python RFC.

## Introduction

The Xena Python RFC Converter is an open-source tool hosted on Xena Networks' GitHub repository. It is designed to help you migrate your Xena Windows desktop RFC test suite configurations into Xena Python RFC, enabling a seamless transition to the Xena Python RFC ecosystem for network automation and testing.

Key features of the Xena Python RFC Converter include:

1. Conversion support: The tool supports conversion of Valkyrie test suite configuration files to Xena Python RFC-compatible format, facilitating the integration of existing test cases into the Xena Python RFC framework.

2. Ease of use: The Xena Python RFC Converter is designed to be user-friendly, with a straightforward process for converting test suite configuration files.

3. Compatibility: The converter ensures that the migrated test suite configurations are compatible with Xena Python RFC Core and can be executed within the Xena Python RFC ecosystem.

> The purpose of Xena Python RFC Converter is ONLY to convert Xena Windows desktop test suite RFC configuration files into Xena Python RFC configuration files. Thus only four test suite types are supported by Xena Python RFC Converter as the source config files. 

# Documentation

The user documentation is hosted:
[Xena Python RFC Converter Documentation](https://docs.xenanetworks.com/projects/xena-python-rfc-converter)


# Installation

## Install Using pip

Make sure Python ``pip`` is installed on you system. If you are using virtualenv, then pip is already installed into environments created by virtualenv, and using sudo is not needed. If you do not have pip installed, download this file: https://bootstrap.pypa.io/get-pip.py and run ``python get-pip.py``.

To install/upgrade:

``` shell
pip install xena-rfc-converter -U
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

Here is a quick start guide to get you started with Xena Python RFC Converter:

Install the latest version of Xena Python RFC Converter using pip:

``` shell
pip install xena-rfc-converter -U
```

Code example to convert `.v2544` into Xena Python RFC 2544 test configuration:

``` python
import asyncio
import json
from xena_rfc_core import controller
from xena-rfc-converter.entry import converter
from xena-rfc-converter.types import TestSuiteType

async def start():
    SOURCE_CONFIG_FILE = "my_old2544_config.v2544" # source config file to be converted

    core_ctrl = await controller.MainController() # create an instance of xena rfc core controller
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