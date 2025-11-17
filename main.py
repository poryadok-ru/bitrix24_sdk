from bitrix24_sdk.bitrix_http.http_client import BitrixClient

if __name__ == "__main__":
    client = BitrixClient(token="6i0pounvys7ll0pl", user_id=159096)
    response = client.crm.type_list(filter={"title": "Отклики"})
    