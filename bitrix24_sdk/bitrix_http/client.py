import requests
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel

from ..config.config import BitrixSettings, load_bitrix_settings


class BitrixHttpClient:
    """Низкоуровневый HTTP-клиент для Bitrix24."""

    def __init__(self, token: str, user_id: int | str, settings: BitrixSettings | None = None,
                 session: Optional[requests.Session] = None,) -> None:
        """
        Инициализация HTTP-клиента.

        Args:
            token: Токен авторизации Bitrix24
            user_id: ID пользователя
            settings: Настройки подключения
            session: HTTP-сессия (опционально)
        """
        self.settings = settings or load_bitrix_settings()
        self._token = token
        self._user_id = str(user_id)
        self._timeout = self.settings.TIMEOUT

        base = self.settings.BASE_URL.rstrip("/")
        self._base_url = f"{base}/{self._user_id}/{self._token}/"

        self._session = session or requests.Session()

    def call(self, method: str, params: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Any:
        """
        Выполнить вызов метода Bitrix24 API.

        Args:
            method: Название метода API
            params: Параметры запроса
            files: Файлы для загрузки

        Returns:
            Ответ от API в виде словаря

        Raises:
            RuntimeError: При ошибке в ответе Bitrix24
        """
        url = f"{self._base_url}{method}.json"

        resp = self._session.post(
            url,
            data=params or {},
            files=files,
            timeout=self._timeout,
        )

        resp.raise_for_status()
        data = resp.json()

        if "error" in data: raise RuntimeError( f"Bitrix error {data['error']}: {data.get('error_description')}")
        return data

    def call_pydantic(self, method: str, params: Optional[Dict[str, Any]], model: Type[BaseModel],
                      files: Optional[Dict[str, Any]] = None) -> BaseModel:
        """
        Вызвать метод и сразу получить Pydantic-модель на основе result.

        Args:
            method: Название метода API
            params: Параметры запроса
            model: Pydantic модель для валидации
            files: Файлы для загрузки

        Returns:
            Валидированная Pydantic модель
        """
        raw_result = self.call(method=method, params=params, files=files)
        return model.model_validate(raw_result)
