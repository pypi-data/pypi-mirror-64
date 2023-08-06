from dataclasses import dataclass
from typing import Any

from mygp_cli.cli.command import Command, CommandResult, CommandLog
from mygp_cli.cli.parsed_arguments import ParsedArguments
from mygp_cli.requests_handling.messenger import Messenger
from mygp_cli.requests_handling.request_data import RequestData
from mygp_cli.requests_handling.response_data import HttpStatus
from mygp_cli.state import ClientId, ClientSecret, Realm, Url
from mygp_cli.state_storage import StateStorage


@dataclass(frozen=True)
class ObtainAccessTokenRequest:
    """Represents a request to obtain a new access token from Keycloak."""
    url: Url
    realm: Realm
    client_id: ClientId
    client_secret: ClientSecret

    def request_data(self) -> RequestData:
        """
        Builds a RequestData instance that is then used in Messenger.send
        method.
        """
        full_url = self.url.append("realms") \
            .append(self.realm.value) \
            .append("protocol/openid-connect/token")

        return RequestData(
            RequestData.Method.POST,
            full_url, {
                "grant_type": "client_credentials",
                "client_id": self.client_id.value,
                "client_secret": self.client_secret.value
            })


@dataclass(frozen=True)
class ObtainAccessTokenCmd(Command):
    NAME = "get-token"

    def register_parser(self, subparsers: Any) -> None:
        subparsers.add_parser(
            ObtainAccessTokenCmd.NAME,
            help="Requests an access token from the server and saves it to "
                 "the state file.")

    def execute(
            self,
            arguments: ParsedArguments,
            log: CommandLog,
            messenger: Messenger,
            state_storage: StateStorage) -> CommandResult:

        try:
            state = state_storage.load_state()
            request = ObtainAccessTokenRequest(
                state.auth_url(),
                state.realm(),
                state.client_id(),
                state.client_secret())
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
                access_token = json.get("access_token")
                if access_token is None:
                    log.error(
                        f"The server returned a response without the token: "
                        f"'{json}'.")
                    return CommandResult.FAILURE
                else:
                    state_storage.save_state(
                        state.with_access_token(access_token))

                    log.info("TOKEN OBTAINED.")
                    log.info(str(json))
            else:
                log.error(f"The server did not return a JSON response.")
                return CommandResult.FAILURE

            return CommandResult.SUCCESS
        else:
            log.error(
                f"The server returned status {response.status.status_code} ("
                f"{response.reason}).")

            json = response.payload_json
            if json is not None:
                log.error(f"'{json}'.")

            return CommandResult.FAILURE
