import typing as t
import requests
from requests import Response
from uuid import UUID
from urllib.parse import urljoin
from datetime import datetime, timezone
from json import dumps

from logging import Logger
from .encoders import CustomJSONEncoder


class Writer:
    def __init__(self, url: str, logger: t.Optional[Logger] = None,) -> None:
        self.url = url
        self._logger = logger

    def _post(self, url: str, data: t.Any) -> Response:
        return requests.post(
            urljoin(self.url, url),
            data=dumps(data, cls=CustomJSONEncoder),
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )

    def _get(self, url: str, data: t.Any) -> Response:
        return requests.get(urljoin(self.url, url), params=data,)

    def get_traces(self, keyword: str = "") -> int:
        res = self._get("api/v1/traces", {"keyword": keyword})
        res.raise_for_status()
        if self._logger is not None:
            self._logger.info(f"traces: {keyword}")
        return res.json()

    def add_scalars(
        self, values: t.Dict[str, float], ts: t.Optional[datetime] = None
    ) -> int:
        _ts = ts if ts is not None else datetime.now(timezone.utc)
        res = self._post("api/v1/add-scalars", data={"values": values, "ts": _ts,})
        res.raise_for_status()
        if self._logger is not None:
            self._logger.info(f"add-scalars: {values}")
        return res.json()
