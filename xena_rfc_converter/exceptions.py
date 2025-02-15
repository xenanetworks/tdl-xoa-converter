
from typing import Any


class UnknowConverterType(Exception):
    def __init__(self, converter_type: Any) -> None:
        self.tyconverter_type = converter_type
        self.msg = f"{converter_type=} converter is not implemented!"
        super().__init__(self.msg)


class FailedLoadModelModule(Exception):
    def __init__(self, module_path: str) -> None:
        self.module_path = module_path
        self.msg = f"Failed to load module {module_path=}"
        super().__init__(self.msg)