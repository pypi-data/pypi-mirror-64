import sys

from mygp_cli.cli.command import ConsoleLog, CommandResult
from mygp_cli.cli.shell import MyGpCliShell
from mygp_cli.requests_handling.messenger import HttpMessenger
from mygp_cli.state_storage import StateFile


def main():
    shell = MyGpCliShell()
    requested_cmd = shell.parse_args(sys.argv[1:])
    result = requested_cmd.cmd.execute(
        requested_cmd.args, ConsoleLog(), HttpMessenger(), StateFile())

    if result == CommandResult.SUCCESS:
        sys.exit(0)
    elif result == CommandResult.FAILURE:
        sys.exit(1)
    else:
        raise TypeError(f"This should never happen: {result}.")


main()
