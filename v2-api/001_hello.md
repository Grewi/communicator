# 1 hello

## 1 request 

### **1-1-1** Неавторизованный запрос

>Пример не авторизованного запроса
Присутствуют стандартные заголовки http 
Тело запроса не шифруется

1. api - Номер версии api 
2. number - номер запроса 
3. host - от кого пришёл запрос
4. contact - является ли данный запрос запросом на добавление в контакты.
5. lang - Предпочтительный язык общения

```
POST / HTTP/1.1
Host: com.example.com
Accept: application/json
Content-Type: application/json; charset=utf-8
Content-Length: 136
Connection: close

{
    "api":"1.0.0",
    "number":"1-1-1"
    "host":"com2.exemple.com",
    "contact": true,
    "lang": "ru",
    "text": "Небольшая строка текста"
}
```

### **1-1-2** Не авторизованный запрос 

>Пример авторизованного запроса
Присутствует заголовок alias 
тело запроса шифруется

```
POST / HTTP/1.1
Host: com.example.com
alias: 123456789
Content-Length: 136
Connection: close

{
    "api":"1.0.0",
    "number":"1-1-2"
    "host":"com2.exemple.com",
    "lang": "ru"
}
```
## 2 response - ответ от сервера 

### **1-2-1** Пример ответа по неатризованному запросу

>Пример ответа без авторизации

1. api - Номер версии api 
2. number - номер запроса 
3. host - от кого пришёл ответ 
4. data - Поля стандартного ответа 

```
POST / HTTP/1.1
Host: com2.example.com
Accept: application/json
Content-Type: application/json; charset=utf-8
Content-Length: 136
Connection: close

{
    "api":"1.0.0",
    "number":"1-2-1"
    "host":"com.exemple.com",
    "data": {
        "name": "Grewi",
        "names": {
            "last": "Григорьев",
            "first": "Евгений",
            "middle": "Викторович",
            "patronymic": "",
            "full": "",
            "short": ""
        },
        "image": "/data/image.jpg",
        "gallery": [
            {
                "link": "/media/1.jpg",
                "type": "image",
                "size": "6Kb",
                "desc": ""
            },
            {
                "link": "/media/1.mp3",
                "type": "audio",
                "size": "1Mb",
                "desc": ""
            },

        ],
        "country": {
            "iso": "643",
            "name": "Россия",
        },
        "desc": "Короткое описание на странице",
        "text": "Подробное описание"
    },
}
```

### **1-2-2** Пример ответа по авторизованному запросу

>Пример ответа с авторизацией 
Присутствует заголовок alias 
тело запроса шифруется

1. api - Номер версии api 
2. number - номер запроса 
3. host - от кого пришёл ответ 
4. data - Поля стандартного ответа 

```
POST / HTTP/1.1
Host: com2.example.com
alias: 6543210
Content-Length: 136
Connection: close

{
    "api":"1.0.0",
    "number":"1-2-2"
    "host":"com.exemple.com",
    "data": {
        "name": "Grewi",
        "names": {
            "last": "Григорьев",
            "first": "Евгений",
            "middle": "Викторович",
            "patronymic": "",
            "full": "",
            "short": ""
        },
        "image": "/data/image.jpg",
        "gallery": [
            {
                "link": "/media/1.jpg",
                "type": "image",
                "size": "6Kb",
                "desc": ""
            },
            {
                "link": "/media/1.mp3",
                "type": "audio",
                "size": "1Mb",
                "desc": ""
            },
        ],
        "country": {
            "iso": "643",
            "name": "Россия",
        },
        "desc": "Короткое описание на странице",
        "text": "Подробное описание"
    },
}
```

## 3 Запрос от клиента к своему серверу на получение списка создания контактов 

### **1-3-1** Запрос от клиента к серверу на получение списка hello запросов 

>По умолчанию сервер не отправляет запросы от других серверов даже с пометкой на создания контакта. 
Пользователь сам должен сам запросить список таких запросов. Запросы на создание контактов имеют не 
продолжительный срок жизни, по этому отдаются запросы за последние несколько минут.

```
POST / HTTP/1.1
Host: com.example.com
alias: 123456789
Content-Length: 136
Connection: close

{
    "api":"1.0.0",
    "number":"1-3-1"
}
```

### **1-3-2** Ответ от сервера со списком контактов 

```
POST / HTTP/1.1
Host: com.example.com
alias: 123456789
Content-Length: 136
Connection: close

{
    "api":"1.0.0",
    "number":"1-3-2"
    "list": [
        {
            "host": "exemle.ru",
            "datetime": 12456789,
            "text": "Сообщение"
        },
        {
            "host": "exemle.ru",
            "datetime": 12456789,
            "text": "Сообщение"
        },
    ]
}
```


