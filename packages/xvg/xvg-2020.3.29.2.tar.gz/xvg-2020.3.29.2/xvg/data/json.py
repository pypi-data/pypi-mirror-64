from json import loads, dumps
from .object import Object


def toJSON(data):
    return dumps(data, default=lambda o: o.__dict__)


def fromJSON(data):
    return loads(data, object_hook=lambda d: Object(d))
