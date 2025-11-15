from typing import Optional, TYPE_CHECKING

from .models import Methods, MethodsParams, Scope, ScopeParams

if TYPE_CHECKING:
    from http_client import BitrixHttpClient


class BaseService:
    """Служебные методы Bitrix."""

    def __init__(self, http: "BitrixHttpClient") -> None:
        self._http = http

    def methods(self, full: bool = None, scope: Optional[str] = None) -> Methods:
        params = MethodsParams(full=full, scope=scope)
        return self._http.call_pydantic(
            method="methods",
            params=params.to_bx_params(),
            model=Methods,
        )

    def scope(self, full: bool = None) -> Scope:
        params = ScopeParams(full=full)
        return self._http.call_pydantic(
            method="scope",
            params=params.to_bx_params(),
            model=Scope,
        )