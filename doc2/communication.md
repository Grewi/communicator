# Communicator

Система взаимного доверия. Основана на серверах подтверждающих доверие дргих серверов. В качестве таких серверов могут выступать сервисы которые в процессе взаимодействия убедились в легитимности  такого адреса, либо специально созданные для этого сервера. Запись о легитимности должна присутствовать на обоих серверах: тот кто проверяет и тот кого проверяют. 
Список коммуникационных серверов должен максимально прозрачным для пользователя, процесс добавления может быть только с явным согласием. Также должен быть доступен процесс валидации записей.
Коммуникационные сервера могут участвовать в поиске по имени хоста и пользователя.
Запрос  к такому серверу, при положительном результате, должен вернуть имя пользователя, хост и публичный ключ
Запрос к искомому серверу должен подтвердить легитимность самого коммуникационного сервера.

Коммуникационные сервера могут использоваться для организации локальных сетей, в том числе и без доступа к глобальной сети.

Работа коммуникационных серверов напоминает серификационные центры, но с некоторыми существенными различаями:
    1. Один адрем может подтверждаться любым количеством коммуникацинных серверов
    2. Организация коммуникационного сервера доступна любому сообществу пользователей
    3. Процес максимально прозрачный для пользователя 

## Пример запроса адреса 
**Запрос**
```
GET / HTTP/1.1
Host: example.com
X-Communicator-Search: user@78.107.58.16
Accept: application/json
Connection: close
```
**Ответы**
```
HTTP/1.1 200 OK
X-Communicator-Search: user@78.107.58.16
Content-Type: application/json; charset=utf-8
Content-Length: 109
Connection: close

{
    "status":"ok",
    "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINGOAlvG+Yl6GXw5qoTOGMGf8Qy8/ePD4QqNFonWZ8xB grewi@grewi"
    "start": 1781422307,
    "end": 1781422307
}
```
```
HTTP/1.1 404 OK
X-Communicator-Search: user@78.107.58.16
Connection: close
```

## Запрос от коммуникационного сервера
Данным запросом коммуникационный сервер сообщает, что готов к обмену записями

```
GET / HTTP/1.1
Host: example.com
X-User-Name: user
X-Communicator-Add: user@78.107.58.16
Accept: application/json
Connection: close
```
```
HTTP/1.1 200 OK
X-Communicator-Search: user@78.107.58.16
Content-Type: application/json; charset=utf-8
Content-Length: 109
Connection: close

{
    "status":"ok"
}
```

## Пример запроса 
Запрос к коммуникационному серверу от пользовательского сервера на добавление адреса

```
POST / HTTP/1.1
Host: example.com
X-Communicator-Add: user@78.107.58.16
Accept: application/json
Content-Type: application/json; charset=utf-8
Content-Length: 136
Connection: close

{
    "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINGOAlvG+Yl6GXw5qoTOGMGf8Qy8/ePD4QqNFonWZ8xB grewi@grewi"
}
```

**Ответы**
```
HTTP/1.1 200 OK
X-Communicator-Add: user@78.107.58.16
Content-Type: application/json; charset=utf-8
Content-Length: 109
Connection: close

{
    "status":"ok",
    "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINGOAlvG+Yl6GXw5qoTOGMGf8Qy8/ePD4QqNFonWZ8xB grewi@grewi"
    "start": 1781422307,
    "end": 1781422307
}
```

```
HTTP/1.1 200 OK
X-Communicator-Add: user@78.107.58.16
Content-Type: application/json; charset=utf-8
Content-Length: 109
Connection: close

{
    "status":"error",
    "description": ""
}
```
