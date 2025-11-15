import requests
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel

from config.config import BitrixSettings, load_bitrix_settings


class BitrixHttpClient:
    """Низкоуровневый HTTP-клиент для Bitrix24."""

    def __init__(self, token: str, user_id: int | str, settings: BitrixSettings | None = None,
                 session: Optional[requests.Session] = None,) -> None:
        """

        :param token:
        :param user_id:
        :param settings:
        :param session:
        """
        self.settings = settings or load_bitrix_settings()
        self._token = token
        self._user_id = str(user_id)
        self._timeout = self.settings.TIMEOUT

        base = self.settings.BASE_URL.rstrip("/")
        self._base_url = f"{base}/{self._user_id}/{self._token}/"

        self._session = session or requests.Session()

    def call(self, method: str, params: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self._base_url}{method}.json"

        resp = self._session.post(
            url,
            data=params or {},
            files=files,
            timeout=self._timeout,
        )

        print(resp.text)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data: raise RuntimeError( f"Bitrix error {data['error']}: {data.get('error_description')}")
        return data

    def call_pydantic(self, method: str, params: Optional[Dict[str, Any]], model: Type[BaseModel],
                      files: Optional[Dict[str, Any]] = None) -> BaseModel:
        """
        Вызвать метод и сразу получить Pydantic-модель на основе result.
        """
        raw_result = self.call(method=method, params=params, files=files)
        return model.model_validate(raw_result)
