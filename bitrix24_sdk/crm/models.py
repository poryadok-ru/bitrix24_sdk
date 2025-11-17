from datetime import datetime
from ..utils import BitrixParams
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class TypeListParams(BitrixParams):
    """Параметры для crm.type.list."""
    order: Optional[Dict[str, str]] = Field(None, description="Объект сортировки: { field: 'ASC'|'DESC' }")
    filter: Optional[Dict[str, Any]] = Field(None, description="Объект фильтрации смарт-процессов")
    start: Optional[int] = Field(None, description="Параметр для постраничной навигации (start = (N-1) * 50)")


class TypeInfo(BaseModel):
    """Информация о смарт-процессе (типе)."""
    id: int = Field(..., description="Идентификатор смарт-процесса")
    title: str = Field(..., description="Название смарт-процесса")
    code: str = Field(..., description="Символьный код")
    created_by: int = Field(..., alias="createdBy", description="ID пользователя, создавшего смарт-процесс")
    entity_type_id: int = Field(..., alias="entityTypeId", description="ID типа сущности")
    custom_section_id: Optional[int] = Field(None, alias="customSectionId", description="ID пользовательского раздела")
    is_categories_enabled: str = Field(..., alias="isCategoriesEnabled", description="Включены свои воронки и туннели продаж (Y/N)")
    is_stages_enabled: str = Field(..., alias="isStagesEnabled", description="Включены свои стадии и канбан (Y/N)")
    is_begin_close_dates_enabled: str = Field(..., alias="isBeginCloseDatesEnabled", description="Включены даты начала и завершения (Y/N)")
    is_client_enabled: str = Field(..., alias="isClientEnabled", description="Включены клиенты (Y/N)")
    is_use_in_userfield_enabled: str = Field(..., alias="isUseInUserfieldEnabled", description="Использование в пользовательских полях (Y/N)")
    is_link_with_products_enabled: str = Field(..., alias="isLinkWithProductsEnabled", description="Связь с товарами (Y/N)")
    is_mycompany_enabled: str = Field(..., alias="isMycompanyEnabled", description="Включена компания (Y/N)")
    is_documents_enabled: str = Field(..., alias="isDocumentsEnabled", description="Включены документы (Y/N)")
    is_source_enabled: str = Field(..., alias="isSourceEnabled", description="Включены источники (Y/N)")
    is_observers_enabled: str = Field(..., alias="isObserversEnabled", description="Включены наблюдатели (Y/N)")
    is_recyclebin_enabled: str = Field(..., alias="isRecyclebinEnabled", description="Включена корзина (Y/N)")
    is_automation_enabled: str = Field(..., alias="isAutomationEnabled", description="Включены роботы и триггеры (Y/N)")
    is_biz_proc_enabled: str = Field(..., alias="isBizProcEnabled", description="Включен дизайнер бизнес процессов (Y/N)")
    is_set_open_permissions: str = Field(..., alias="isSetOpenPermissions", description="Открытые права доступа (Y/N)")
    is_payments_enabled: str = Field(..., alias="isPaymentsEnabled", description="Включены платежи (Y/N)")
    is_counters_enabled: str = Field(..., alias="isCountersEnabled", description="Включены счетчики (Y/N)")
    created_time: datetime = Field(..., alias="createdTime", description="Время создания")
    updated_time: datetime = Field(..., alias="updatedTime", description="Время обновления")
    updated_by: int = Field(..., alias="updatedBy", description="ID пользователя, обновившего смарт-процесс")


class TimeInfo(BaseModel):
    """Информация о времени выполнения запроса."""
    start: float = Field(..., description="Время начала выполнения")
    finish: float = Field(..., description="Время окончания выполнения")
    duration: float = Field(..., description="Общая длительность")
    processing: float = Field(..., description="Время обработки")
    date_start: str = Field(..., description="Дата и время начала")
    date_finish: str = Field(..., description="Дата и время окончания")
    operating: float = Field(..., description="Время работы")


class TypeListResult(BaseModel):
    """Результат метода crm.type.list."""
    types: List[TypeInfo] = Field(..., description="Список смарт-процессов")


class TypeList(BaseModel):
    """Ответ метода crm.type.list."""
    result: TypeListResult = Field(..., description="Результат запроса")
    time: Optional[TimeInfo] = Field(None, description="Информация о времени выполнения запроса")
    total: Optional[int] = Field(None, description="Общее количество найденных записей")


class ItemListParams(BitrixParams):
    """Параметры для crm.item.list."""
    entity_type_id: int = Field(..., serialization_alias="entityTypeId", description="Идентификатор системного или пользовательского типа")
    select: Optional[List[str]] = Field(None, description="Список полей для выборки или ['*'] для всех полей")
    filter: Optional[Dict[str, Any]] = Field(None, description="Объект фильтрации элементов")
    order: Optional[Dict[str, str]] = Field(None, description="Объект сортировки: { field: 'ASC'|'DESC' }")
    start: Optional[int] = Field(None, description="Параметр для постраничной навигации (start = (N-1) * 50)")
    use_original_uf_names: Optional[bool] = Field(None, serialization_alias="useOriginalUfNames", description="Использовать оригинальные имена пользовательских полей (Y/N)")
    
    def to_bx_params(self) -> Dict[str, Any]:
        """Преобразовать параметры в формат Bitrix API."""
        params = super().to_bx_params()
        if "useOriginalUfNames" in params and isinstance(params["useOriginalUfNames"], bool):
            params["useOriginalUfNames"] = "Y" if params["useOriginalUfNames"] else "N"
        return params


class Item(BaseModel):
    """Элемент CRM (динамическая модель, поля зависят от параметра select)."""
    id: Optional[int] = Field(None, description="Идентификатор элемента")
    title: Optional[str] = Field(None, description="Название элемента")
    
    model_config = {"extra": "allow"}  


class ItemListResult(BaseModel):
    """Результат метода crm.item.list."""
    items: List[Item] = Field(..., description="Список элементов CRM")


class ItemList(BaseModel):
    """Ответ метода crm.item.list."""
    result: ItemListResult = Field(..., description="Результат запроса")
    total: Optional[int] = Field(None, description="Общее количество найденных элементов")
    next: Optional[int] = Field(None, description="Значение для следующего запроса в параметр start")
    time: Optional[TimeInfo] = Field(None, description="Информация о времени выполнения запроса")
