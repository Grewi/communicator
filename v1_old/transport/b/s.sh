#! /bin/bash

# 1. Создаем корневой CA (самоподписанный)
openssl req -x509 -newkey rsa:4096 \
    -keyout ca.key \
    -out ca.crt \
    -days 365 \
    -nodes \
    -subj "/CN=My Custom CA"

# 2. Создаем серверный сертификат и подписываем его
openssl req -newkey rsa:4096 \
    -keyout server.key \
    -out server.csr \
    -nodes \
    -subj "/CN=localhost"

openssl x509 -req -days 365 \
    -in server.csr \
    -CA ca.crt \
    -CAkey ca.key \
    -set_serial 01 \
    -out server.crt

# 3. Создаем клиентский сертификат (для тестирования mTLS)
openssl req -newkey rsa:4096 \
    -keyout client.key \
    -out client.csr \
    -nodes \
    -subj "/CN=client"

openssl x509 -req -days 365 \
    -in client.csr \
    -CA ca.crt \
    -CAkey ca.key \
    -set_serial 02 \
    -out client.crt

# Удаляем временные CSR-файлы (опционально)
rm *.csr