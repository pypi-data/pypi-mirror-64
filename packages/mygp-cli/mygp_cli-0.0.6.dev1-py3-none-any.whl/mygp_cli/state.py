from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Url:
    value: str

    def append(self, path: str) -> Url:
        url_ends_with_slash = self.value.endswith("/")
        path_starts_with_slash = path.startswith("/")

        if url_ends_with_slash & path_starts_with_slash:
            return Url(self.value + path[1:])
        elif url_ends_with_slash & (not path_starts_with_slash):
            return Url(self.value + path)
        elif (not url_ends_with_slash) & path_starts_with_slash:
            return Url(self.value + path)
        else:
            return Url(self.value + "/" + path)


@dataclass(frozen=True)
class Realm:
    value: str


@dataclass(frozen=True)
class ClientId:
    value: str


@dataclass(frozen=True)
class ClientSecret:
    value: str


STATE_VAR_API_URL = "api_url"
STATE_VAR_AUTH_URL = "auth_url"
STATE_VAR_CLIENT_ID = "client_id"
STATE_VAR_CLIENT_SECRET = "client_secret"
STATE_VAR_COMPANY_KEY = "company_key"
STATE_VAR_REALM = "auth_realm"
STATE_VAR_TOKEN = "access_token"


@dataclass(frozen=True)
class State:
    _state_data: Dict[str, str]
    modified: bool = False

    def api_url(self) -> Url:
        return Url(self._get_mandatory(STATE_VAR_API_URL))

    def auth_url(self) -> Url:
        return Url(self._get_mandatory(STATE_VAR_AUTH_URL))

    def realm(self) -> Realm:
        return Realm(self._get_mandatory(STATE_VAR_REALM))

    def client_id(self) -> ClientId:
        return ClientId(self._get_mandatory(STATE_VAR_CLIENT_ID))

    def client_secret(self) -> ClientSecret:
        return ClientSecret(self._get_mandatory(STATE_VAR_CLIENT_SECRET))

    def access_token(self) -> str:
        return self._get_mandatory(STATE_VAR_TOKEN)

    def with_var(self, variable_name: str, variable_value: str) -> State:
        updated_state = self.state_dict()
        updated_state[variable_name] = variable_value
        return State(updated_state, True)

    def with_access_token(self, access_token: str) -> State:
        return self.with_var(STATE_VAR_TOKEN, access_token)

    def with_company_key(self, company_key: str) -> State:
        return self.with_var(STATE_VAR_COMPANY_KEY, company_key)

    def state_dict(self) -> Dict[str, str]:
        return self._state_data.copy()

    def _get_mandatory(self, variable_name: str) -> str:
        if variable_name not in self._state_data:
            raise RuntimeError(
                f"Missing {variable_name} state variable.")
        return self._state_data[variable_name]
