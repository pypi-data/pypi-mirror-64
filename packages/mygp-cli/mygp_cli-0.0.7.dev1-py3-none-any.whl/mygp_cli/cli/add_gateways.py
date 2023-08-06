# noinspection PyProtectedMember
from argparse import _SubParsersAction
from dataclasses import dataclass
from typing import List, Dict

from mygp_cli.cli.command import RequestCommand, CommandLog, CommandResult
from mygp_cli.cli.create_sandbox_customer import GatewayId
from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.model import CustomerKey
from mygp_cli.requests_handling.request_data import RequestData, HeadersBuilder
from mygp_cli.state import Url, State
from mygp_cli.state_storage import StateStorage


@dataclass(frozen=True)
class AddGatewaysToCustomerRequest:
    api_url: Url
    access_token: str
    customer_key: CustomerKey
    gateways: List[GatewayId]

    def request_data(self) -> RequestData:
        """
        Builds a RequestData instance that is then used in Messenger.send
        method.
        """
        full_url = self.api_url\
            .append(f"v1/sandbox"
                    f"/customers/{self.customer_key.value}/add-gateways")

        headers = HeadersBuilder().add_auth_bearer(self.access_token).build()

        json = {
            "gateways": list(map(lambda g: g.value, self.gateways))
        }

        return RequestData(
            RequestData.Method.POST,
            full_url,
            headers=headers,
            json=json)


@dataclass(frozen=True)
class AddGatewaysToCustomerCmd(RequestCommand):
    # pylint: disable=invalid-name
    NAME = "add-gateways"

    def register_parser(self, subparsers: _SubParsersAction) -> None:
        parser = subparsers.add_parser(
            AddGatewaysToCustomerCmd.NAME,
            help="Adds gateways to a customer.")

        parser.add_argument(
            "--customer", dest="customer-key", metavar="CUSTOMER KEY",
            help='customer key (if not specified, the one from the state file '
                 'will be used)')

        parser.add_argument(
            "--gateways", nargs="+",
            metavar=("GATEWAY-ID1", "GATEWAY-ID2"),
            help='a space-separated list of gateway IDs')

    def _prepare_request(
            self,
            arguments: ParsedArguments,
            state: State) -> RequestData:
        gateways = arguments["gateways"]

        if isinstance(gateways, List):
            gateways_ids = list(map(lambda g: GatewayId(g), gateways))

            if isinstance(arguments["customer-key"], str):
                customer_key = CustomerKey(arguments["customer-key"])
            else:
                customer_key = state.customer_key()

            request = AddGatewaysToCustomerRequest(
                state.api_url(),
                state.access_token(),
                customer_key,
                gateways_ids)
            return request.request_data()
        else:
            raise RuntimeError(
                "gateways parameter should be a list of strings.")

    def _process_json_response(
            self,
            json: Dict,
            state: State,
            log: CommandLog,
            state_storage: StateStorage) -> CommandResult:
        return CommandResult.SUCCESS
