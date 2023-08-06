import logging
from abc import abstractmethod, ABC
# noinspection PyProtectedMember
from argparse import _SubParsersAction
from enum import Enum
from typing import Tuple, Dict

from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.requests_handling.messenger import Messenger
from mygp_cli.requests_handling.request_data import RequestData
from mygp_cli.requests_handling.response_data import HttpStatus
from mygp_cli.state import State
from mygp_cli.state_storage import StateStorage


class CommandLog:
    @abstractmethod
    def debug(self, message: str) -> None:
        ...

    @abstractmethod
    def info(self, message: str) -> None:
        ...

    @abstractmethod
    def warn(self, message: str) -> None:
        ...

    @abstractmethod
    def error(self, message: str) -> None:
        ...


class ConsoleLog(CommandLog):
    def __init__(self) -> None:
        # create logger
        self._logger = logging.getLogger('mygp-cli')
        self._logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(message)s')

        # add formatter to ch
        console_handler.setFormatter(formatter)

        # add ch to logger
        self._logger.addHandler(console_handler)

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
    """
    The result of the Command.execute() method.
    """
    SUCCESS = 0
    FAILURE = 1


class Command:
    """
    Defines a contract for command line commands provided by mygp-cli tool.
    """
    @abstractmethod
    def register_parser(self, subparsers: _SubParsersAction) -> None:
        ...

    @abstractmethod
    def execute(
            self,
            arguments: ParsedArguments,
            log: CommandLog,
            messenger: Messenger,
            state_storage: StateStorage) -> CommandResult:
        ...


class RequestCommand(Command, ABC):
    """
    A specialization of Command that sends an HTTP request and then expects
    a response JSON payload which is further processed. Both the creation of
    the request and processing of JSON response are exposed as abstract methods
    to be implemented by inheriting command classes.
    """

    @abstractmethod
    def register_parser(self, subparsers: _SubParsersAction) -> None:
        ...

    def execute(
            self,
            arguments: ParsedArguments,
            log: CommandLog,
            messenger: Messenger,
            state_storage: StateStorage) -> CommandResult:
        try:
            state = state_storage.load_state()
            request = self._prepare_request(arguments, state)
        except RuntimeError as err:
            log.error(str(err))
            return CommandResult.FAILURE

        response = messenger.send(request)

        success_statuses = frozenset([
            HttpStatus.ok(),
            HttpStatus.created(),
            HttpStatus.accepted()])

        if response.status in success_statuses:
            log.info(
                f"The server returned status {response.status.status_code} ("
                f"{response.reason}).")

            json = response.payload_json

            if json is not None:
                return self._process_json_response(json, state, log,
                                                   state_storage)
            else:
                log.error(f"The server did not return a JSON response.")
                return CommandResult.FAILURE
        else:
            log.error(
                f"The server returned status {response.status.status_code} ("
                f"{response.reason}).")

            json = response.payload_json
            if json is not None:
                log.error(f"'{json}'.")

            return CommandResult.FAILURE

    @abstractmethod
    def _prepare_request(
            self, arguments: ParsedArguments, state: State) -> RequestData:
        ...

    @abstractmethod
    def _process_json_response(
            self,
            json: Dict,
            state: State,
            log: CommandLog,
            state_storage: StateStorage) -> CommandResult:
        ...
