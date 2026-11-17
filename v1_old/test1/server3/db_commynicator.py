#!/usr/bin/env python3

# Типа база данных которая по хосту отдаёт на ключ

def db(host):
    if host == "localhost:8002":
        return "key 8002"
    elif host == "localhost:8003":
        return "key 8003"
    else:
        return ""