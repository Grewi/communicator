# База данных

Структура базы

users
    id 
    user
    host
    port
    public_key
    tor
    i2p
    rules
    last_connect
    date_create

groups
    id
    name
    rules

users_groups
    user_id
    group_id

chats
    id
    name
    image
    description
    date_create

chats_user_rules
    chat_id
    user_id
    rule

chat_user_messages
    id
    type_id
    

cannals

messages

comments

