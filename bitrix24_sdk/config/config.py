import os
from pydantic import BaseModel, Field, Extra
from json import JSONDecodeError


CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIR, "bitrix_settings.json")


class BitrixSettings(BaseModel, extra="forbid"):
    BASE_URL: str = Field(..., title="Базовый url Bitrix24")
    TIMEOUT: float = Field(60, title="Время на отправку запроса")


def load_bitrix_settings(path: str | None = None, override: BitrixSettings | None = None) -> BitrixSettings:
    if override is not None:
        return override

    config_path = path or DEFAULT_CONFIG_PATH

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return BitrixSettings.model_validate_json(f.read())


    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")

    except JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON в файле {config_path}") from e

    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки настроек Bitrix: {e}")


if __name__ == "__main__":
    settings = load_bitrix_settings()
    print(settings.BASE_URL)
