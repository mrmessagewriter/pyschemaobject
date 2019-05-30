"""
    pyschemagen

    This is an object generator which uses JSON Schema as the input, and generates
    python code.
"""


import json
import jsonschema
import requests


def generate_from_schema(path=None, text=None, url=None, validate = False):
    if path is None and text is None and url is None:
        raise ValueError("Require either a path or the json text as input.")

    jsonobj = None
    if path:
        f = open(path,"r")
        jsondata = f.read()
        f.close()
        jsonobj = json.loads(jsondata)

    if text:
        jsonobj = json.loads(text)

    if url:
        response = requests.get(url)
        if response.status_code == 200:
            jsonobj = response.json()
        else:
            raise ValueError(f"got error {response.status_code}")

    if validate:
        response = requests.get("http://json-schema.org/draft-07/schema")
        jsonschema.validate(jsonobj, response.json())

    check = jsonschema.Draft7Validator()
    if not check:
        raise ValueError("Error validating the schema")
