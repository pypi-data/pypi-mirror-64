"""
Primitive types and transformations
"""

from datetime import date, datetime, time, timezone

from random import randint
from faker import Faker

_faker = Faker()

PRIMITIVE_TYPES = {
    "int": ["int", "number"],
    "float": ["float", "decimal"],
    "str": ["str", "string", "text"],
    "bool": ["bool", "boolean"],
    "date": ["date"],
    "datetime": ["datetime"],
    "time": ["time"]
}

PRIMITIVE_TYPES_CLASSES = {
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "date": date,
    "datetime": datetime,
    "time": time,
    "None": None
}

DEFAULT_VALUES_STR = {
    "int": "0",
    "float": "0.0",
    "str": "None",
    "bool": "False",
    "date": "None",
    "datetime": "None",
    "time": "None",
    "None": "None"
}

DEFAULT_VALUES = {
    "int": 0,
    "float": 0.0,
    "str": None,
    "bool": False,
    "date": None,
    "datetime": None,
    "time": None,
    "None": None
}

PRIMITIVE_TYPES_FAKES = {
    "int": lambda: randint(0, 1000),
    "float": lambda: randint(0, 1000000)/100,
    "bool": lambda: bool(randint(0, 1)),
    "str": lambda: _faker.text(30),
    "date": lambda: _faker.date_time().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=timezone.utc),
    "datetime": lambda: _faker.date_time().replace(tzinfo=timezone.utc),
    "time": lambda: randint(0, 86400000),
    "None": lambda: None
}

PRIMITIVE_PROMAX_TYPES_FAKES = {
    "int": lambda: randint(0, 1000),
    "float": lambda: randint(0, 1000000)/100,
    "bool": lambda: bool(randint(0, 1)),
    "str": lambda: _faker.text(30),
    "date": lambda: _faker.date_time().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=timezone.utc).strftime('%Y%m%d'),
    "datetime": lambda: _faker.date_time().replace(tzinfo=timezone.utc).strftime('%Y%m%d%H%M%S'),
    "time": lambda: _faker.time().replace(':', ''),
    "None": lambda: None
}


def get_type_from_str(type_str: str) -> str:
    """
    Normalize type from type string read from csv/xlsx file

    Valid only primitive types. Another types returns "None"
    """
    query = [x
             for x in PRIMITIVE_TYPES
             if type_str.lower() in PRIMITIVE_TYPES[x]]
    return query[0] if len(query) > 0 else 'None'


def is_primitive_type(type_str: str) -> bool:
    return get_type_from_str(type_str) != 'None'


def get_type_class_from_str(type_str: str):
    normal_type = get_type_from_str(type_str)
    return PRIMITIVE_TYPES_CLASSES[normal_type]


def get_default_primitive_type_as_str(type_str: str) -> str:
    normal_type = get_type_from_str(type_str)
    return DEFAULT_VALUES_STR[normal_type]


def get_fake_primitive_type(type_str: str, promax_type: bool = True):
    normal_type = get_type_from_str(type_str)
    if promax_type:
        fake = PRIMITIVE_PROMAX_TYPES_FAKES[normal_type]()
    else:
        fake = PRIMITIVE_TYPES_FAKES[normal_type]()
    return fake
