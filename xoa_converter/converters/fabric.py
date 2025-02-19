from typing import Any, Type, Protocol, Dict
from xoa_converter import exceptions
from xoa_converter import types
from .rfc2544.adapter import Converter2544
from .rfc3918.adapter import Converter3918
from .rfc2889.adapter import Converter2889


class XenaRfcConverter(Protocol):
    def __init__(self, source_config: str) -> None: ...
    def gen(self) -> Dict[str, Any]: ...


def get_converter(test_suite_type: types.TestSuiteType) -> Type[XenaRfcConverter]:
    """Selecting and returning Converter"""
    if test_suite_type == types.TestSuiteType.RFC2544:
        return Converter2544
    elif test_suite_type == types.TestSuiteType.RFC3918:
        return Converter3918
    elif test_suite_type == types.TestSuiteType.RFC2889:
        return Converter2889
    raise exceptions.UnknowConverterType(test_suite_type)