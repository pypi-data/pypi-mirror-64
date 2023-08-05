import json
from os.path import abspath, dirname, join

from jsonschema import Draft7Validator, RefResolver

base_path = dirname(dirname(abspath(__file__)))


def handle_schema_filename(filename):
    extension = filename.split(".")[-1]
    if extension != "json":
        if len(filename.split(".")) > 1:
            filename = filename[:-len(extension)] + ".json"
        else:
            filename = filename + ".json"
    return filename


def is_valid(data, schema_name):
    if not isinstance(data, dict):
        raise TypeError(
            "Data to be validated must be a dict, got {} instead".format(
                type(data)))
    filename = handle_schema_filename(schema_name)
    with open(join(base_path, "schemas", "base.json"), "r") as bf:
        base_schema = json.load(bf)
        with open(join(base_path, "schemas", filename), "r") as sf:
            object_schema = json.load(sf)
            resolver = RefResolver.from_schema(base_schema)
            validator = Draft7Validator(
                object_schema, resolver=resolver)
            validator.validate(data)
            return True
