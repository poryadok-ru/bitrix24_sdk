import io
import requests
from typing import Optional, TYPE_CHECKING, List
from .models import (
    GetChildrenParams, GetChildren,
    GetListParams, GetList, GetStorageParams, GetStorage,
    GetFolderParams, GetFolder, AddFolderParams, AddFolder,
    AddSubfolderParams, AddSubfolder, GetFileParams, GetFile,
    DeleteTreeParams, DeleteTree, UploadFileParams, UploadFile,
    GetUploadUrl, FileInfo, UploadFileComplete
)
from typing import Dict, Any

if TYPE_CHECKING:
    from http_client import BitrixHttpClient


class DiskService:
    """
    Сервис для работы с Bitrix24 Disk API.

    Предоставляет методы для управления файлами и папками:
    - Получение списка хранилищ
    - Работа с папками (создание, получение содержимого)
    - Работа с файлами (загрузка, получение информации)
    - Управление правами доступа

    Attributes:
        _http: HTTP клиент для выполнения запросов

    Example:
        >>> client = BitrixClient(token="...", user_id=123)
        >>> # Получить хранилища
        >>> storages = client.disk.get_list()
        >>> # Создать папку
        >>> folder = client.disk.add_subfolder(123, {"NAME": "Reports"})
        >>> # Загрузить файл
        >>> with open("report.pdf", "rb") as f:
        ...     result = client.disk.upload_file_complete(
        ...         folder.result.id, f.read(), "report.pdf"
        ...     )
    """

    def __init__(self, http: "BitrixHttpClient") -> None:
        self._http = http

    def get_children(self, id: int | str, filter: Optional[Dict[str, Any]] = None, start: Optional[int] = None) -> GetChildren:
        """
        Получить содержимое папки (файлы и подпапки).

        Args:
            id: ID папки
            filter: Опциональный фильтр по полям
            start: Начальная позиция для пагинации

        Returns:
            GetChildren: Список файлов и папок

        Example:
            >>> children = client.disk.get_children(123)
            >>> print(f"В папке {len(children.result)} элементов")
            >>> for item in children.result:
            ...     print(f"- {item.name} ({item.type})")
        """
        params = GetChildrenParams(id=id, filter=filter, start=start)
        return self._http.call_pydantic(
            method="disk.folder.getchildren",
            params=params.to_bx_params(),
            model=GetChildren,
        )

    def get_list(self, filter: Optional[Dict[str, Any]] = None, start: Optional[int] = None) -> GetList:
        """
        Получить список доступных хранилищ.

        Args:
            filter: Фильтр по полям
            start: Начальная позиция для пагинации

        Returns:
            GetList: Список хранилищ
        """
        params = GetListParams(filter=filter, start=start)
        return self._http.call_pydantic(
            method="disk.storage.getlist",
            params=params.to_bx_params(),
            model=GetList,
        )

    def get_storage(self, id: str) -> GetStorage:
        """
        Получить информацию о хранилище по ID.

        Args:
            id: ID хранилища

        Returns:
            GetStorage: Информация о хранилище
        """
        params = GetStorageParams(id=id)
        return self._http.call_pydantic(
            method="disk.storage.get",
            params=params.to_bx_params(),
            model=GetStorage,
        )

    def get_folder(self, id: int) -> GetFolder:
        """
        Получить информацию о папке по ID.

        Args:
            id: ID папки

        Returns:
            GetFolder: Информация о папке
        """
        params = GetFolderParams(id=id)
        return self._http.call_pydantic(
            method="disk.folder.get",
            params=params.to_bx_params(),
            model=GetFolder,
        )

    def add_folder(self, id: str, data: Dict[str, Any]) -> AddFolder:
        """
        Создать папку в корне хранилища.

        Args:
            id: ID хранилища
            data: Данные папки, обязательно поле "NAME"

        Returns:
            AddFolder: Информация о созданной папке
        """
        params = AddFolderParams(id=id, data=data)
        return self._http.call_pydantic(
            method="disk.storage.addfolder",
            params=params.to_bx_params(),
            model=AddFolder,
        )

    def add_subfolder(self, id: int, data: Dict[str, Any]) -> AddSubfolder:
        """
        Создать подпапку в указанной папке.

        Args:
            id: ID родительской папки
            data: Данные папки, обязательно поле "NAME"

        Returns:
            AddSubfolder: Информация о созданной папке

        Example:
            >>> result = client.disk.add_subfolder(123, {"NAME": "Новая папка"})
            >>> print(f"Папка создана: {result.result.name}")
        """
        params = AddSubfolderParams(id=id, data=data)
        return self._http.call_pydantic(
            method="disk.folder.addsubfolder",
            params=params.to_bx_params(),
            model=AddSubfolder,
        )

    def get_file(self, id: int) -> GetFile:
        """
        Получить информацию о файле по ID.

        Args:
            id: ID файла

        Returns:
            GetFile: Информация о файле
        """
        params = GetFileParams(id=id)
        return self._http.call_pydantic(
            method="disk.file.get",
            params=params.to_bx_params(),
            model=GetFile,
        )

    def delete_tree(self, id: int) -> DeleteTree:
        """
        Уничтожить папку и все дочерние элементы навсегда.

        Args:
            id: ID папки

        Returns:
            DeleteTree: Результат удаления
        """
        params = DeleteTreeParams(id=id)
        return self._http.call_pydantic(
            method="disk.folder.deletetree",
            params=params.to_bx_params(),
            model=DeleteTree,
        )

    def upload_file(self, id: int, data: Dict[str, Any], file_content: Optional[str] = None,
                   generate_unique_name: Optional[bool] = None, rights: Optional[List[Dict[str, Any]]] = None) -> UploadFile:
        """
        Загрузить файл в папку (с base64 или получить uploadUrl).

        Args:
            id: ID папки
            data: Данные файла, обязательно поле "NAME"
            file_content: Содержимое файла в Base64
            generate_unique_name: Генерировать уникальное имя при конфликте
            rights: Права доступа

        Returns:
            UploadFile или GetUploadUrl: Результат загрузки или URL для загрузки
        """
        params = UploadFileParams(
            id=id, data=data, file_content=file_content,
            generate_unique_name=generate_unique_name, rights=rights
        )

        raw_result = self._http.call(method="disk.folder.uploadfile", params=params.to_bx_params())

        result = raw_result['result']
        if 'uploadUrl' in result and 'field' in result:
            return GetUploadUrl.model_validate(raw_result)
        else:
            return UploadFile.model_validate(raw_result)

    def upload_file_complete(self, folder_id: int, file_content: bytes, file_name: str, content_type: str = 'application/pdf') -> UploadFileComplete:
        """
        Загрузить файл в папку Bitrix24 Disk.

        Выполняет полную загрузку файла: получает upload URL и отправляет файл.

        Args:
            folder_id: ID папки для загрузки
            file_content: Содержимое файла в байтах
            file_name: Имя файла
            content_type: MIME тип файла

        Returns:
            UploadFileComplete: Информация о загруженном файле

        Raises:
            Exception: При ошибке загрузки

        Example:
            >>> with open("document.pdf", "rb") as f:
            ...     content = f.read()
            >>> result = client.disk.upload_file_complete(
            ...     folder_id=123,
            ...     file_content=content,
            ...     file_name="report.pdf"
            ... )
            >>> print(f"Файл загружен: {result.result.name}")
        """
        upload_info = self.get_upload_url(folder_id)
        upload_url = upload_info.result.upload_url
        field_name = upload_info.result.field

        file_obj = io.BytesIO(file_content)
        files = {field_name: (file_name, file_obj, content_type)}
        response = requests.post(upload_url, files=files)

        if response.status_code == 200:
            return UploadFileComplete.model_validate(response.json())
        else:
            raise Exception(f"Ошибка загрузки: {response.status_code}, {response.text}")

    def get_upload_url(self, id: int) -> GetUploadUrl:
        """
        Получить URL для загрузки файла (двухэтапная загрузка).

        Args:
            id: ID папки

        Returns:
            GetUploadUrl: URL и поле для загрузки файла
        """
        return self._http.call_pydantic(
            method="disk.folder.uploadfile",
            params={"id": id},
            model=GetUploadUrl,
        )