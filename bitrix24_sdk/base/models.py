from typing import Optional, List

from pydantic import BaseModel, Field

from ..utils import BitrixParams


class MethodsParams(BitrixParams):
    """Параметры для метода methods."""
    full: Optional[bool] = Field(True, description="Если параметр принимает значение true, то метод вернет список всех методов")
    scope: Optional[str] = Field(None,description="Показ методов, входящих в указанное разрешение. Если задан параметр без значения (methods?scope=&auth=xxxxx), то будут выведены все общие методы.")


class Methods(BaseModel):
    """Ответ метода methods."""
    result: Optional[List[str]] = Field(None, description="Массив со списком разрешений")


class ScopeParams(BitrixParams):
    """Параметры для метода scope."""
    full: Optional[bool] = Field(True, description="Если параметр принимает значение true, то метод вернет полный список разрешений")

class Scope(BaseModel):
    """Ответ метода scope."""
    result: Optional[List[str]] = Field(None, description="Массив со списком разрешений")
