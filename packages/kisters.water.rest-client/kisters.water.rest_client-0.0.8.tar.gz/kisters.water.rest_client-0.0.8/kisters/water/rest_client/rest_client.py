import functools
from typing import Iterable, Optional, Union

import msgpack
import requests

from .auth import Authentication


class RESTClient:
    def __init__(self, url: str, *, authentication: Authentication = None):
        self._url = url.rstrip("/")
        self._auth = authentication
        self._session = requests.Session()

    @property
    def url(self):
        return self._url

    @property
    def session(self):
        return self._session

    def _construct_url(
        self, resource: Optional[Union[str, Iterable[str]]] = None
    ) -> str:
        if resource is None:
            return self.url
        if isinstance(resource, str):
            return "/".join((self.url, resource))
        return "/".join((self.url, *resource))

    def __getattr__(self, name):
        return functools.partial(self.request, name)

    @staticmethod
    def _verify_response(response):
        if response.status_code == 422:
            raise ValueError(response.json())
        response.raise_for_status()

    def request(
        self,
        method: str,
        resource: Optional[Union[str, Iterable[str]]] = None,
        *,
        msgpack_json: Optional[bool] = None,
        **kwargs,
    ):
        headers = kwargs.pop("headers", {})
        if self._auth:
            headers["Authorization"] = f"Bearer {self._auth.get_access_token()}"
        if msgpack_json:
            headers["accept"] = "application/x-msgpack"
            if kwargs.get("json"):
                if kwargs.get("data"):
                    raise ValueError(
                        "Option msgpack_json requires data kwarg to be unset"
                    )
                else:
                    kwargs["data"] = msgpack.packb(kwargs.pop("json"))
                    headers["content-type"] = "application/x-msgpack"
        resp = self._session.request(
            method, self._construct_url(resource), headers=headers, **kwargs
        )
        self._verify_response(resp)
        if resp.headers.get("Content-Type") == "application/x-msgpack":
            return msgpack.unpackb(resp.content, raw=False)
        if resp.headers.get("Content-Type") == "application/json":
            return resp.json()
        return resp
