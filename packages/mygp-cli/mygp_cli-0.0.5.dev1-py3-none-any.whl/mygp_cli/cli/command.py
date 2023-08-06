# noinspection PyProtectedMember
from argparse import _SubParsersAction
from enum import Enum
from typing import Tuple
import logging

from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.requests_handling.messenger import Messenger
from mygp_cli.state_storage import StateStorage


class CommandLog:
    def debug(self, message: str) -> None: ...

    def info(self, message: str) -> None: ...

    def warn(self, message: str) -> None: ...

    def error(self, message: str) -> None: ...


class ConsoleLog(CommandLog):
    def __init__(self) -> None:
        # create logger
        self._logger = logging.getLogger('mygp-cli')
        self._logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self._logger.addHandler(ch)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warn(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3


LogEntry = Tuple[LogLevel, str]


class CommandResult(Enum):
    SUCCESS = 0
    FAILURE = 1


class Command:
    def register_parser(self, subparsers: _SubParsersAction) -> None: ...

    def execute(
            self,
            arguments: ParsedArguments,
            log: CommandLog,
            messenger: Messenger,
            state_storage: StateStorage) -> CommandResult: ...
