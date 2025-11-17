from typing import Optional, TYPE_CHECKING

from .models import Methods, MethodsParams, Scope, ScopeParams

if TYPE_CHECKING:
    from ..bitrix_http import BitrixHttpClient


class BaseService:
    """Служебные методы Bitrix."""

    def __init__(self, http: "BitrixHttpClient") -> None:
        self._http = http

    def methods(self, full: bool = None, scope: Optional[str] = None) -> Methods:
        """
        Получить список доступных методов API.

        Args:
            full: Возвращать полную информацию о методах
            scope: Фильтр по scope

        Returns:
            Methods: Список доступных методов
        """
        params = MethodsParams(full=full, scope=scope)
        return self._http.call_pydantic(
            method="methods",
            params=params.to_bx_params(),
            model=Methods,
        )

    def scope(self, full: bool = None) -> Scope:
        """
        Получить информацию о scope авторизации.

        Args:
            full: Возвращать полную информацию

        Returns:
            Scope: Информация о scope
        """
        params = ScopeParams(full=full)
        return self._http.call_pydantic(
            method="scope",
            params=params.to_bx_params(),
            model=Scope,
        )