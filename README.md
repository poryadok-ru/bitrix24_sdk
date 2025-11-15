# Bitrix24 SDK

Bitrix24 SDK предоставляет удобный интерфейс для работы с REST API Bitrix24. Включает полную поддержку Disk API для управления файлами и папками.

## Основные возможности

- Полная поддержка Bitrix24 Disk API
- Типобезопасные Pydantic модели
- Простая загрузка файлов
- Поддержка Python 3.8+

## Установка

```bash
pip install bitrix24-sdk
```

Или из исходников:

```bash
git clone https://github.com/poryadok-ru/bitrix24_sdk.git
cd bitrix24_sdk
pip install .
```

## Архитектура

```
bitrix24_sdk/
├── bitrix_http/     # HTTP клиент и основной BitrixClient
├── config/          # Конфигурация
├── disk/            # Disk API сервисы и модели
└── base/            # Базовые API методы
```

## Использование

```python
from bitrix24_sdk import BitrixClient

# Инициализация
client = BitrixClient(token="your_token", user_id=123)

# Работа с хранилищами
storages = client.disk.get_list()
print(f"Найдено хранилищ: {len(storages.result)}")

# Работа с папками
children = client.disk.get_children(folder_id=123)
folder = client.disk.add_subfolder(123, {"NAME": "Reports"})

# Загрузка файла
with open("report.pdf", "rb") as f:
    result = client.disk.upload_file_complete(
        folder_id=folder.result.id,
        file_content=f.read(),
        file_name="monthly_report.pdf"
    )
    print(f"Файл загружен: {result.result.name}")
```

## API

### Disk API
- `get_list(filter=None, start=None)` - список хранилищ
- `get_children(id, filter=None, start=None)` - содержимое папки
- `add_subfolder(id, data)` - создать подпапку
- `get_file(id)` - информация о файле
- `upload_file_complete(folder_id, file_content, file_name)` - загрузить файл

### Base API
- `methods()` - доступные методы API
- `scope()` - scope авторизации

## Настройки

SDK поддерживает настройку через параметры конструктора BitrixClient или конфигурационные файлы.

## Разработка

```bash
# Клонирование
git clone https://github.com/poryadok-ru/bitrix24_sdk.git
cd bitrix24_sdk

# Виртуальное окружение
python -m venv venv
source venv/bin/activate

# Установка для разработки
pip install -e .
```
