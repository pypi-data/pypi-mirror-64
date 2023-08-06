import csv
import json
import sys


def csv_change(fp_in, delimiter=',', quotechar='"', remove_empty=False, 
        custom_headers=None, **kwargs):
    r = csv.DictReader(fp_in, delimiter=delimiter, quotechar=quotechar, 
            fieldnames=custom_headers)
    rows = [row_dct for row_dct in r]
    if remove_empty:
        rows = [dict([(k, item) for k, item in row.items() if item]) for row in rows]
    return rows


def return_json(data, pretty_spaces=4, sort_keys=False, **kwargs):
    json_value= json.dumps(data, indent=pretty_spaces, sort_keys=sort_keys)
    return(json_value)

def change(csv,**kwargs):
    csv_local= None
    try:
        if csv == '-' or csv is None:
            csv = sys.stdin
        elif isinstance(csv, str):
            csv = csv_local = open(csv, 'r')

        data = csv_change(csv, **kwargs)
        return return_json(data)
    finally:
        if csv_local is not None:
            csv_local.close()
