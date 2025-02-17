from enum import Enum

JsonStr = str

class TestSuiteType(Enum):
    """Four test suite types supported by Xena Python RFC Converter as the source config files. 
    """
    RFC2544 = "RFC-2544"
    RFC2889 = "RFC-2889"
    RFC3918 = "RFC-3918"
    Y1564 = "Y-1564"