import os
from typing import Optional


class Envar:
    def get(self, variable_name: str) -> Optional[str]: ...
    def set(self, variable_name: str, variable_value: str) -> None: ...


class OsEnvar(Envar):
    def get(self, variable_name: str) -> Optional[str]:
        return os.environ.get(variable_name)

    def set(self, variable_name: str, variable_value: str) -> None:
        os.environ[variable_name] = variable_value
