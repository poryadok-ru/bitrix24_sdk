from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union

from ..utils import BitrixParams


class FolderInfo(BaseModel):
    """Информация о папке."""
    id: int = Field(..., description="Идентификатор", alias="ID")
    name: str = Field(..., description="Название папки", alias="NAME")
    code: Optional[str] = Field(None, description="символьный код", alias="CODE")
    storage_id: int = Field(..., alias="STORAGE_ID", description="Идентификатор хранилища")
    type: str = Field(..., alias="TYPE", description="Тип объекта (обычно 'folder')")
    parent_id: Optional[int] = Field(None, alias="PARENT_ID", description="Идентификатор родительской папки")
    deleted_type: int = Field(..., alias="DELETED_TYPE", description="Маркер удаления (0 — не удалена, 1 — удалена/в корзине)")
    create_time: datetime = Field(..., alias="CREATE_TIME", description="Время создания")
    update_time: datetime = Field(..., alias="UPDATE_TIME", description="Время изменения")
    delete_time: Optional[datetime] = Field(None, alias="DELETE_TIME", description="Время перемещения в корзину (если есть)")
    detail_url: str = Field(..., alias="DETAIL_URL", description="Ссылка на просмотр списка файлов папки")


class FileInfo(BaseModel):
    """Информация о файле."""
    id: int = Field(..., description="Идентификатор файла", alias="ID")
    name: str = Field(..., description="Название файла", alias="NAME")
    code: Optional[str] = Field(None, description="Символьный код", alias="CODE")
    storage_id: int = Field(..., alias="STORAGE_ID", description="Идентификатор хранилища")
    type: str = Field(..., alias="TYPE", description="Тип объекта (обычно 'file')")
    parent_id: Optional[int] = Field(None, alias="PARENT_ID", description="Идентификатор родительской папки")
    deleted_type: int = Field(..., alias="DELETED_TYPE", description="Маркер удаления (0 — не удалена, 1 — удалена/в корзине)")
    create_time: datetime = Field(..., alias="CREATE_TIME", description="Время создания")
    update_time: datetime = Field(..., alias="UPDATE_TIME", description="Время изменения")
    delete_time: Optional[datetime] = Field(None, alias="DELETE_TIME", description="Время перемещения в корзину")
    created_by: int = Field(..., alias="CREATED_BY", description="Идентификатор пользователя, создавшего файл")
    updated_by: int = Field(..., alias="UPDATED_BY", description="Идентификатор пользователя, изменившего файл")
    deleted_by: Optional[int] = Field(None, alias="DELETED_BY", description="Идентификатор пользователя, переместившего в корзину файл")
    download_url: str = Field(..., alias="DOWNLOAD_URL", description="URL для скачивания файла приложением")
    detail_url: str = Field(..., alias="DETAIL_URL", description="Ссылка на страницу детальной информации о файле")


class GetChildrenParams(BitrixParams):
    """Параметры для disk.folder.getchildren."""
    id: int = Field(..., description="Идентификатор папки")
    filter: Optional[Dict[str, Any]] = Field(None, description="Необязательный параметр. Поддерживает фильтрацию по полям, которые указаны в disk.folder.getfields как USE_IN_FILTER: true.")
    start: Optional[int] = Field(None, alias="START", description="Порядковый номер элемента списка, начиная с которого необходимо возвращать следующие элементы при вызове текущего метода")


class GetChildren(BaseModel):
    """Ответ метода disk.folder.getchildren."""
    result: Optional[List[Union[FolderInfo, FileInfo]]] = Field(None, description="Список папок и файлов")
    next: Optional[int] = Field(None, description="Номер следующего элемента для постраничной навигации")


class StorageInfo(BaseModel):
    """Информация о хранилище."""
    id: str = Field(..., description="Идентификатор хранилища", alias="ID")
    name: str = Field(..., description="Название хранилища", alias="NAME")
    code: Optional[str] = Field(None, description="Символьный код", alias="CODE")
    module_id: str = Field(..., description="Идентификатор модуля", alias="MODULE_ID")
    entity_type: str = Field(..., description="Тип сущности", alias="ENTITY_TYPE")
    entity_id: str = Field(..., description="Идентификатор сущности", alias="ENTITY_ID")
    root_object_id: str = Field(..., description="Идентификатор корневой папки", alias="ROOT_OBJECT_ID")


class GetListParams(BitrixParams):
    """Параметры для disk.storage.getlist."""
    filter: Optional[Dict[str, Any]] = Field(None, description="Необязательный параметр. Поддерживает фильтрацию по полям, которые указаны в disk.storage.getfields как USE_IN_FILTER: true.")
    start: Optional[int] = Field(None, alias="START", description="Порядковый номер элемента списка, начиная с которого необходимо возвращать следующие элементы при вызове текущего метода")


class GetList(BaseModel):
    """Ответ метода disk.storage.getlist."""
    result: Optional[List[StorageInfo]] = Field(None, description="Список доступных хранилищ")


class GetStorageParams(BitrixParams):
    """Параметры для disk.storage.get."""
    id: str = Field(..., description="Идентификатор хранилища")


class GetStorage(BaseModel):
    """Ответ метода disk.storage.get."""
    result: Optional[StorageInfo] = Field(None, description="Информация о хранилище")


class GetFolderParams(BitrixParams):
    """Параметры для disk.folder.get."""
    id: int = Field(..., description="Идентификатор папки")


class GetFolder(BaseModel):
    """Ответ метода disk.folder.get."""
    result: Optional[FolderInfo] = Field(None, description="Информация о папке")


class AddFolderParams(BitrixParams):
    """Параметры для disk.storage.addfolder."""
    id: str = Field(..., description="Идентификатор хранилища")
    data: Dict[str, Any] = Field(..., description="Массив, описывающий папку. Обязательное поле NAME — имя новой папки.")


class AddFolder(BaseModel):
    """Ответ метода disk.storage.addfolder."""
    result: Optional[FolderInfo] = Field(None, description="Информация о созданной папке")


class AddSubfolderParams(BitrixParams):
    """Параметры для disk.folder.addsubfolder."""
    id: int = Field(..., description="Идентификатор родительской папки")
    data: Dict[str, Any] = Field(..., description="Массив, описывающий папку. Обязательное поле NAME — имя новой папки.")


class AddSubfolder(BaseModel):
    """Ответ метода disk.folder.addsubfolder."""
    result: Optional[FolderInfo] = Field(None, description="Информация о созданной подпапке")


class GetFileParams(BitrixParams):
    """Параметры для disk.file.get."""
    id: int = Field(..., description="Идентификатор файла")


class GetFile(BaseModel):
    """Ответ метода disk.file.get."""
    result: Optional[FileInfo] = Field(None, description="Информация о файле")


class DeleteTreeParams(BitrixParams):
    """Параметры для disk.folder.deletetree."""
    id: int = Field(..., description="Идентификатор папки")


class DeleteTree(BaseModel):
    """Ответ метода disk.folder.deletetree."""
    result: Optional[bool] = Field(None, description="Результат удаления (true если успешно)")


class UploadFileParams(BitrixParams):
    """Параметры для disk.folder.uploadfile."""
    id: int = Field(..., description="Идентификатор папки")
    data: Dict[str, Any] = Field(..., description="Массив, описывающий файл. Обязательное поле NAME — имя файла.")
    file_content: Optional[str] = Field(None, alias="fileContent", description="Файл в формате Base64")
    generate_unique_name: Optional[bool] = Field(None, alias="generateUniqueName", description="Уникализировать имя файла")
    rights: Optional[List[Dict[str, Any]]] = Field(None, description="Массив прав доступа")


class UploadFile(BaseModel):
    """Ответ метода disk.folder.uploadfile."""
    result: Optional[FileInfo] = Field(None, description="Информация о загруженном файле")


class UploadUrlInfo(BaseModel):
    """Информация для двухэтапной загрузки файла."""
    field: str = Field(..., description="Имя поля для загрузки файла")
    upload_url: str = Field(..., alias="uploadUrl", description="URL для загрузки файла")


class GetUploadUrl(BaseModel):
    """Ответ метода disk.folder.uploadfile (для получения URL загрузки)."""
    result: Optional[UploadUrlInfo] = Field(None, description="Информация для загрузки файла")


class UploadFileComplete(BaseModel):
    """Ответ метода полной загрузки файла."""
    result: Optional[FileInfo] = Field(None, description="Информация о загруженном файле")


