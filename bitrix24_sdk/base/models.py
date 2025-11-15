from typing import Optional, List

from pydantic import BaseModel, Field


class MethodsParams(BaseModel):
    full: Optional[bool] = Field(True, description="Если параметр принимает значение true, то метод вернет список всех методов")
    scope: Optional[str] = Field(None,description="Показ методов, входящих в указанное разрешение. Если задан параметр без значения (methods?scope=&auth=xxxxx), то будут выведены все общие методы.")

    def to_bx_params(self) -> dict:
        return self.model_dump(exclude_none=True)

class Methods(BaseModel):
    result: Optional[List[str]] = Field(None, description="Массив со списком разрешений")


class ScopeParams(BaseModel):
    full: Optional[bool] = Field(True, description="Если параметр принимает значение true, то метод вернет полный список разрешений")

    def to_bx_params(self) -> dict:
        return self.model_dump(exclude_none=True)

class Scope(BaseModel):
    result: Optional[List[str]] = Field(None, description="Массив со списком разрешений")
