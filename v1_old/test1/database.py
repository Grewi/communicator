#!/usr/bin/env python3

# Здесь будем имитировать базу данных

# Список доверенных серверов
def communicators():
    return {
        "localhost:8001": "http://localhost:8001"
    }

# Функция для поиска урл коммуникатора
def communicator(name):
    data = communicators()
    return data.get(name)
