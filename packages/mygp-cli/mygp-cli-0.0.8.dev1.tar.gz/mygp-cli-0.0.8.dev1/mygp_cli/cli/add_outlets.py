# noinspection PyProtectedMember
from argparse import _SubParsersAction
from dataclasses import dataclass
from typing import List, Dict

from mygp_cli.cli.command import RequestCommand, CommandLog, CommandResult
from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.model import CustomerKey, OutletId
from mygp_cli.requests_handling.request_data import RequestData, HeadersBuilder
from mygp_cli.state import Url, State
from mygp_cli.state_storage import StateStorage


@dataclass(frozen=True)
class AddOutletsToCustomerRequest:
    api_url: Url
    access_token: str
    customer_key: CustomerKey
    outlets: List[OutletId]

    def request_data(self) -> RequestData:
        """
        Builds a RequestData instance that is then used in Messenger.send
        method.
        """
        full_url = self.api_url\
            .append(f"v1/sandbox"
                    f"/customers/{self.customer_key.value}/add-outlets")

        headers = HeadersBuilder().add_auth_bearer(self.access_token).build()

        json = {
            "outlets": list(map(lambda x: x.value, self.outlets))
        }

        return RequestData(
            RequestData.Method.POST,
            full_url,
            headers=headers,
            json=json)


@dataclass(frozen=True)
class AddOutletsToCustomerCmd(RequestCommand):
    # pylint: disable=invalid-name
    NAME = "add-outlets"

    def register_parser(self, subparsers: _SubParsersAction) -> None:
        parser = subparsers.add_parser(
            AddOutletsToCustomerCmd.NAME,
            help="Adds outlets to a customer.")

        parser.add_argument(
            "--customer", dest="customer-key", metavar="CUSTOMER KEY",
            help='customer key (if not specified, the one from the state file '
                 'will be used)')

        parser.add_argument(
            "--outlets", nargs="+",
            metavar=("OUTLET-ID1", "OUTLET-ID2"),
            help='a space-separated list of outlet IDs')

    def _prepare_request(
            self,
            arguments: ParsedArguments,
            state: State) -> RequestData:
        outlets = arguments["outlets"]

        if isinstance(outlets, List):
            outlets_ids = list(map(lambda x: OutletId(x), outlets))

            if isinstance(arguments["customer-key"], str):
                customer_key = CustomerKey(arguments["customer-key"])
            else:
                customer_key = state.customer_key()

            request = AddOutletsToCustomerRequest(
                state.api_url(),
                state.access_token(),
                customer_key,
                outlets_ids)
            return request.request_data()
        else:
            raise RuntimeError(
                "outlets parameter should be a list of strings.")

    def _process_json_response(
            self,
            json: Dict,
            state: State,
            log: CommandLog,
            state_storage: StateStorage) -> CommandResult:
        return CommandResult.SUCCESS
