# noinspection PyProtectedMember
from argparse import _SubParsersAction
from dataclasses import dataclass, field
from typing import List, Dict

from mygp_cli.cli.command import CommandLog, CommandResult, \
    RequestCommand
from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.model import Url, GatewayId, OutletId
from mygp_cli.requests_handling.request_data import RequestData, HeadersBuilder
from mygp_cli.state import State
from mygp_cli.state_storage import StateStorage


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
class CreateSandboxCustomerCmd(RequestCommand):
    # pylint: disable=invalid-name
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

    def _prepare_request(
            self,
            arguments: ParsedArguments,
            state: State) -> RequestData:
        request = CreateSandboxCustomerRequest(
            state.api_url(),
            state.access_token())
        return request.request_data()

    def _process_json_response(
            self,
            json: Dict,
            state: State,
            log: CommandLog,
            state_storage: StateStorage) -> CommandResult:
        customer_key = json.get("customer_key")

        if customer_key is None:
            log.error(
                f"The server returned a response without the company "
                f"key: '{json}'.")
            return CommandResult.FAILURE
        else:
            state_storage.save_state(
                state.with_customer_key(customer_key))
            log.info("CUSTOMER CREATED.")
            log.info(str(json))
            return CommandResult.SUCCESS
