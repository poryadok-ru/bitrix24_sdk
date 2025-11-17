from ..config.config import BitrixSettings, load_bitrix_settings
from .client import BitrixHttpClient
from ..base.service import BaseService
from ..disk.service import DiskService
from ..crm.service import CrmService

class BitrixClient:
    """
    Основной клиент для работы с Bitrix24 API.

    Предоставляет доступ ко всем модулям API через унифицированный интерфейс.

    Attributes:
        base: Сервис для работы с базовыми методами API
        disk: Сервис для работы с Disk API
        crm: Сервис для работы с CRM API
        http: HTTP клиент для выполнения запросов

    Example:
        >>> client = BitrixClient(token="your_token", user_id=123)
        >>> storages = client.disk.get_list()
        >>> print(f"Найдено хранилищ: {len(storages.result)}")
        >>> types = client.crm.type_list()
        >>> print(f"Найдено смарт-процессов: {types.total}")
    """

    def __init__(self, token: str, user_id: int | str, settings: BitrixSettings | None = None,) -> None:
        """
        Инициализация клиента Bitrix24.

        Args:
            token: Токен авторизации Bitrix24
            user_id: ID пользователя
            settings: Настройки подключения (опционально)

        Example:
            >>> client = BitrixClient(
            ...     token="yaikpz2ql7745g9k",
            ...     user_id=159096
            ... )
        """
        self.settings = settings or load_bitrix_settings()
        self.http = BitrixHttpClient(
            token=token,
            user_id=user_id,
            settings=self.settings,
        )
    
        self.base = BaseService(self.http)
        self.disk = DiskService(self.http)
        self.crm = CrmService(self.http)