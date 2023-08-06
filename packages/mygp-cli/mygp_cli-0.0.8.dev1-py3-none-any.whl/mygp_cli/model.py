from __future__ import annotations

from dataclasses import dataclass


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


@dataclass(frozen=True)
class CustomerKey:
    value: str


@dataclass(frozen=True)
class GatewayId:
    value: str


@dataclass(frozen=True)
class OutletId:
    value: str
