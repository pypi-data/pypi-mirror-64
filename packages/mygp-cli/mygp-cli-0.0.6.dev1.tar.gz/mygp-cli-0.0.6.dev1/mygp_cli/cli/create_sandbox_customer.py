# noinspection PyProtectedMember
from argparse import _SubParsersAction
from dataclasses import dataclass, field
from typing import List

from mygp_cli.cli.command import Command, CommandLog, CommandResult
from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.requests_handling.messenger import Messenger
from mygp_cli.requests_handling.request_data import RequestData, HeadersBuilder
from mygp_cli.requests_handling.response_data import HttpStatus
from mygp_cli.state import Url
from mygp_cli.state_storage import StateStorage


@dataclass(frozen=True)
class GatewayId:
    value: str


@dataclass(frozen=True)
class OutletId:
    value: str


@dataclass(frozen=True)
class CreateSandboxCustomerRequest:
    api_url: Url
    access_token: str
    gateways: List[GatewayId] = field(default_factory=list)
    outlets: List[OutletId] = field(default_factory=list)

    def request_data(self) -> RequestData:
        """
        Builds a RequestData instance that is then used in Messenger.send
        method.
        """
        full_url = self.api_url.append("v1/sandbox/customers")

        headers = HeadersBuilder().add_auth_bearer(self.access_token).build()

        json = {}
        if len(self.gateways) > 0:
            json["gateways"] = list(map(lambda g: g.value, self.gateways))
        if len(self.outlets) > 0:
            json["outlets"] = list(map(lambda g: g.value, self.outlets))

        return RequestData(
            RequestData.Method.POST,
            full_url,
            headers=headers,
            json=json)


@dataclass(frozen=True)
class CreateSandboxCustomerCmd(Command):
    NAME = "add-customer"

    def register_parser(self, subparsers: _SubParsersAction) -> None:
        parser = subparsers.add_parser(
            CreateSandboxCustomerCmd.NAME,
            help="Creates a new customer.")

        parser.add_argument(
            "--gateways", nargs="+",
            metavar=("GATEWAY-ID1", "GATEWAY-ID2"),
            help='a space-separated list of gateway IDs')
        parser.add_argument(
            "--outlets", nargs="+",
            metavar=("OUTLET-ID1", "OUTLET-ID2"),
            help='a space-separated list of gateway outlets')

    def execute(self, arguments: ParsedArguments, log: CommandLog,
                messenger: Messenger,
                state_storage: StateStorage) -> CommandResult:

        try:
            state = state_storage.load_state()
            request = CreateSandboxCustomerRequest(
                state.api_url(),
                state.access_token())
        except RuntimeError as err:
            log.error(str(err))
            return CommandResult.FAILURE

        response = messenger.send(request.request_data())

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
                company_key = json.get("company_key")

                if company_key is None:
                    log.error(
                        f"The server returned a response without the company "
                        f"key: '{json}'.")
                    return CommandResult.FAILURE
                else:
                    state_storage.save_state(
                        state.with_company_key(company_key))
            else:
                log.error(f"The server did not return a JSON response.")
                return CommandResult.FAILURE

            log.info("CUSTOMER CREATED.")
            log.info(str(json))

            return CommandResult.SUCCESS
        else:
            log.error(
                f"The server returned status {response.status.status_code} ("
                f"{response.reason}).")

            json = response.payload_json
            if json is not None:
                log.error(f"'{json}'.")

            return CommandResult.FAILURE
