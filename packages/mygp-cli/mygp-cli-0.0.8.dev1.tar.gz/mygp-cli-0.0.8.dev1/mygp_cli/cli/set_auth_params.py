# noinspection PyProtectedMember
from argparse import _SubParsersAction
from dataclasses import dataclass

from mygp_cli.cli.command import Command, CommandLog, CommandResult
from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.requests_handling.messenger import Messenger
from mygp_cli.state import STATE_VAR_AUTH_URL, STATE_VAR_REALM, \
    STATE_VAR_CLIENT_ID, \
    STATE_VAR_CLIENT_SECRET, STATE_VAR_API_URL
from mygp_cli.state_storage import StateStorage, State


@dataclass(frozen=True)
class SetAuthParamsCmd(Command):
    # pylint: disable=invalid-name
    NAME = "set-auth"

    def register_parser(self, subparsers: _SubParsersAction) -> None:
        parser = subparsers.add_parser(
            SetAuthParamsCmd.NAME,
            help="Configures the authentication parameters so an access token "
                 "can be obtained from the server.")

        parser.add_argument("--api-url", dest="api-url", help='API URL')
        parser.add_argument(
            "--auth-url", dest="auth-url", help='authentication URL')
        parser.add_argument("--realm", help='authentication realm')
        parser.add_argument("--cid", help='client ID')
        parser.add_argument("--secret", help='client secret')

    def execute(
            self,
            arguments: ParsedArguments,
            log: CommandLog,
            messenger: Messenger,
            state_storage: StateStorage) -> CommandResult:

        state = state_storage.load_state()

        state = self._set_state_var_from_args(arguments, state, log, "api-url",
                                              STATE_VAR_API_URL)
        state = self._set_state_var_from_args(arguments, state, log, "auth-url",
                                              STATE_VAR_AUTH_URL)
        state = self._set_state_var_from_args(arguments, state, log, "realm",
                                              STATE_VAR_REALM)
        state = self._set_state_var_from_args(arguments, state, log, "cid",
                                              STATE_VAR_CLIENT_ID)
        state = self._set_state_var_from_args(arguments, state, log, "secret",
                                              STATE_VAR_CLIENT_SECRET)

        if state.modified:
            state_storage.save_state(state)
        else:
            log.info(
                "Please specify one or more of authentication parameters. Type "
                "--help for more information.")

        return CommandResult.SUCCESS

    @staticmethod
    def _set_state_var_from_args(
            arguments: ParsedArguments,
            state: State,
            log: CommandLog,
            arg_name: str,
            state_var_name: str) -> State:
        if arg_name in arguments:
            value = arguments[arg_name]

            if value is not None:
                if isinstance(value, str):
                    log.debug(f"Setting the state variable {state_var_name}.")
                    return state.with_var(state_var_name, value)
                else:
                    raise RuntimeError("Unsupported state variable type.")
            else:
                return state
        else:
            return state
