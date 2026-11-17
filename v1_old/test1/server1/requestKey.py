#!/usr/bin/env python3

import requests
import database

# Функция запроса к коммуникатору и получение ключа
def key(host):
    # Получаем хост доверенного сервера, хотя на самом деле здесь нужно сравнение двух списков и перебор по совпадениям
    communicator_host = database.communicator("localhost:8001")
    params = None
    headers = {
        "X-Communicator-Search": host
    }
    response = requests.get(communicator_host, params, headers)

    if response.status_code == 200:
        try: 
            return response.json()  # автоматически парсит JSON в словарь/список
        except Exception:
            pass
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)