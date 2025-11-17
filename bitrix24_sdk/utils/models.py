from typing import Dict, Any
from pydantic import BaseModel


class BitrixParams(BaseModel):
    """Базовый класс для параметров Bitrix24 API с автоматическим преобразованием."""
    
    def to_bx_params(self) -> Dict[str, Any]:
        params = self.model_dump(exclude_none=True, by_alias=True)
        dict_fields = ['data', 'filter']
        for field_name in dict_fields:
            if field_name in params and isinstance(params[field_name], dict):
                field_dict = params.pop(field_name)
                for key, value in field_dict.items():
                    params[f'{field_name}[{key}]'] = value

        return params

