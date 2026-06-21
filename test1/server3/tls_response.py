#!/usr/bin/env python3

import db_commynicator

def communicator():
    key = db_commynicator.db("localhost:8002")
    return {
        "key": key
    }