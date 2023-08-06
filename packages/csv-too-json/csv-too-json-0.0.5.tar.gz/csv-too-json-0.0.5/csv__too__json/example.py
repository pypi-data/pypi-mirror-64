# !/usr/bin/env python3
#Example Code
import csv__too__json
import json

def change(csv):
    try:
        response = json.loads(csv__too__json.change(csv))
        return response
    except Exception as e:
        exception_error = str(e)
        return exception_error

print(change('fredrick_test.csv'))
