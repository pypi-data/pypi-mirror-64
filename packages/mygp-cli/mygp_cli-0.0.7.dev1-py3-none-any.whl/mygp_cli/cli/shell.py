import argparse
import sys
from typing import Dict

from attr import dataclass

from mygp_cli.cli.add_gateways import AddGatewaysToCustomerCmd
from mygp_cli.cli.command import Command
from mygp_cli.cli.create_sandbox_customer import CreateSandboxCustomerCmd
from mygp_cli.cli.obtain_access_token import ObtainAccessTokenCmd
from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.cli.set_auth_params import SetAuthParamsCmd


@dataclass(frozen=True)
class RequestedCommand:
    cmd: Command
    args: ParsedArguments


class MyGpCliShell:
    def __init__(self):
        self.__init_parser()

    def parse_args(self, args) -> RequestedCommand:
        if len(args) == 0:
            self._parser.print_help()
            sys.exit(0)
            # noinspection PyUnreachableCode,PyTypeChecker
            return None
        else:
            parsed_args = self._parser.parse_args(args)

            args_dict = vars(parsed_args)

            requested_cmd_name = args_dict[MyGpCliShell._CMD_NAME_KEY]
            requested_cmd = self._commands[requested_cmd_name]

            # remove the command name key from the dictionary to enable easier
            # testing
            args_dict.pop(MyGpCliShell._CMD_NAME_KEY)

            return RequestedCommand(requested_cmd, args_dict)

    def __init_parser(self):
        self._parser = argparse.ArgumentParser(
            description='mygp sandbox CLI')

        self._commands: Dict[str, Command] = {
            SetAuthParamsCmd.NAME: SetAuthParamsCmd(),
            ObtainAccessTokenCmd.NAME: ObtainAccessTokenCmd(),
            CreateSandboxCustomerCmd.NAME: CreateSandboxCustomerCmd(),
            AddGatewaysToCustomerCmd.NAME: AddGatewaysToCustomerCmd()
        }

        subparsers = self._parser.add_subparsers(
            # the name of the parsed command will be stored under a special key
            # in the Namespace dictionary
            dest=MyGpCliShell._CMD_NAME_KEY,
            required=True,
            title="command",
            description="Specifies one of the mygp commands to be executed.",
            help="one of the commands to be executed (REQUIRED)")

        for cmd in self._commands.values():
            cmd.register_parser(subparsers)

    def print_help(self):
        self._parser.print_help()

    _CMD_NAME_KEY = "command_name"
