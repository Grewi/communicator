# 1 hello

## 1 request 

### 1 
Пример не авторизованного запроса
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

Пример авторизованного запроса
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
    "number":"1-1-1"
    "host":"com2.exemple.com",
    "lang": "ru"
}
```
## 2 response - ответ 

Пример ответа без авторизации

```
POST / HTTP/1.1
Host: com2.example.com
Accept: application/json
Content-Type: application/json; charset=utf-8
Content-Length: 136
Connection: close

{
    "api":"1.0.0",
    "number":"1-1-2"
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

