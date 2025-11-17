from typing import Optional, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..bitrix_http import BitrixHttpClient

from .models import TypeListParams, TypeList, ItemListParams, ItemList


class CrmService:
    """
    Сервис для работы с Bitrix24 CRM API.
    
    Предоставляет методы для работы со смарт-процессами и другими сущностями CRM.
    
    Attributes:
        _http: HTTP клиент для выполнения запросов
    
    Example:
        >>> client = BitrixClient(token="...", user_id=123)
        >>> types = client.crm.type_list()
        >>> print(f"Найдено смарт-процессов: {types.total}")
    """
    
    def __init__(self, http: "BitrixHttpClient"):
        self._http = http

    def type_list(
        self,
        order: Optional[Dict[str, str]] = None,
        filter: Optional[Dict[str, Any]] = None,
        start: Optional[int] = None
    ) -> TypeList:
        """
        Получить список пользовательских типов (смарт-процессов).
        
        Args:
            order: Объект сортировки формата { field: 'ASC'|'DESC' }
            filter: Объект фильтрации смарт-процессов
            start: Параметр для постраничной навигации (start = (N-1) * 50)
        
        Returns:
            TypeList: Список смарт-процессов
        
        Example:
            >>> # Получить все смарт-процессы, отсортированные по убыванию id
            >>> types = client.crm.type_list(order={"id": "DESC"})
            >>> 
            >>> # Получить смарт-процессы с фильтром
            >>> types = client.crm.type_list(
            ...     filter={
            ...         "isAutomationEnabled": "Y",
            ...         "isBizProcEnabled": "Y"
            ...     }
            ... )
            >>> 
            >>> # Получить вторую страницу результатов
            >>> types = client.crm.type_list(start=50)
        """
        params = TypeListParams(order=order, filter=filter, start=start)
        return self._http.call_pydantic(
            method="crm.type.list",
            params=params.to_bx_params(),
            model=TypeList,
        )

    def item_list(
        self,
        entity_type_id: int,
        select: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None,
        order: Optional[Dict[str, str]] = None,
        start: Optional[int] = None,
        use_original_uf_names: Optional[bool] = None
    ) -> ItemList:
        """
        Получить список элементов определенного типа объекта CRM.
        
        Args:
            entity_type_id: Идентификатор системного или пользовательского типа (обязательный)
            select: Список полей для выборки или ['*'] для всех полей
            filter: Объект фильтрации элементов
            order: Объект сортировки формата { field: 'ASC'|'DESC' }
            start: Параметр для постраничной навигации (start = (N-1) * 50)
            use_original_uf_names: Использовать оригинальные имена пользовательских полей (True/False)
        
        Returns:
            ItemList: Список элементов CRM
        
        Example:
            >>> # Получить все лиды (entityTypeId=1) с базовыми полями
            >>> items = client.crm.item_list(
            ...     entity_type_id=1,
            ...     select=["id", "title", "name", "lastName"]
            ... )
            >>> 
            >>> # Получить лиды с фильтром и сортировкой
            >>> items = client.crm.item_list(
            ...     entity_type_id=1,
            ...     select=["id", "title", "stageId", "opportunity"],
            ...     filter={"stageId": "NEW"},
            ...     order={"id": "DESC"}
            ... )
            >>> 
            >>> # Получить вторую страницу результатов
            >>> items = client.crm.item_list(
            ...     entity_type_id=1,
            ...     start=50
            ... )
        """
        params = ItemListParams(
            entity_type_id=entity_type_id,
            select=select,
            filter=filter,
            order=order,
            start=start,
            use_original_uf_names=use_original_uf_names
        )
        return self._http.call_pydantic(
            method="crm.item.list",
            params=params.to_bx_params(),
            model=ItemList,
        )
