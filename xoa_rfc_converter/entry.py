import json
from enum import Enum
from .converters import fabric
from . import types


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name.upper()
        else:
            return super().default(obj)


def converter(
    test_suite_type: types.TestSuiteType,
    source_config: types.JsonStr,
) -> str:
    """Convert an Valkyrie test suite application's config file into Xena Python RFC test suite config.

    :param test_suite_type: Registered test suite type.
    :type test_suite_type: types.TestSuiteType
    :param source_config:  Old application config data from .v2544, .v3918, .v2889 files.
    :type source_config: types.JsonStr
    :return: JSON string of the converted config file
    :rtype: str
    """
    converter_class = fabric.get_converter(test_suite_type)
    _model = converter_class(source_config=source_config).gen()
    return json.dumps(_model, indent=2, cls=ComplexEncoder)
