from abc import abstractmethod
from enum import Enum
from json import JSONDecodeError

import requests

from mygp_cli.requests_handling.request_data import RequestData
from mygp_cli.requests_handling.response_data import ResponseData, HttpStatus


class Messenger:
    @abstractmethod
    def send(self, request_data: RequestData) -> ResponseData:
        ...


class PayloadType(Enum):
    JSON = 0
    FORM_DATA = 1


class HttpMessenger(Messenger):

    """Provides a method to send a HTTP request."""
    def send(self, request_data: RequestData) -> ResponseData:
        """Sends the specified HTTP request and returns a response."""

        payload_type: PayloadType
        if request_data.json is not None:
            payload_type = PayloadType.JSON
        else:
            payload_type = PayloadType.FORM_DATA

        headers = request_data.headers

        # print(f"Sending request to {request_data.url.value}, {params}...")

        if request_data.method == RequestData.Method.POST:
            if payload_type == PayloadType.JSON:
                response = requests.post(
                    request_data.url.value,
                    headers=headers,
                    json=request_data.json)
            elif payload_type == PayloadType.FORM_DATA:
                response = requests.post(
                    request_data.url.value,
                    headers=headers,
                    data=request_data.form_parameters)
            else:
                raise RuntimeError(f"Unsupported payload type {payload_type}")
        elif request_data.method == RequestData.Method.GET:
            if payload_type == PayloadType.JSON:
                response = requests.get(
                    request_data.url.value,
                    headers=headers,
                    json=request_data.json)
            elif payload_type == PayloadType.FORM_DATA:
                response = requests.get(
                    request_data.url.value,
                    headers=headers,
                    data=request_data.form_parameters)
            else:
                raise RuntimeError(f"Unsupported payload type {payload_type}")
        else:
            raise RuntimeError(
                f"Unsupported request type {request_data.method}")

        content_type = response.headers.get("content-type")

        try:
            json = response.json()
        except JSONDecodeError:
            json = None

        return ResponseData(
            HttpStatus(response.status_code),
            response.reason,
            content_type,
            json)
