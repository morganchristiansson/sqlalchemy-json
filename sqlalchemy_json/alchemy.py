# Third-party modules
try:
  import simplejson as json
except ImportError:
  import json

import sqlalchemy
from sqlalchemy.ext import mutable
from sqlalchemy_utils.types.json import JSONType

# Custom modules
from . import track


class NestedMutableDict(mutable.Mutable, track.TrackedDict):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(value)
        return super().coerce(key, value)


class NestedMutableList(mutable.Mutable, track.TrackedList):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, list):
            return cls(value)
        return super().coerce(key, value)


class NestedMutable(mutable.Mutable):
    """SQLAlchemy `mutable` extension with nested change tracking."""
    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionary to NestedMutable."""
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return NestedMutableDict.coerce(key, value)
        if isinstance(value, list):
            return NestedMutableList.coerce(key, value)
        return super().coerce(key, value)


class JsonObject():
  """JSON object type for SQLAlchemy with change tracking as base level."""


class NestedJsonObject(JSONType):
  """JSON object type for SQLAlchemy with nested change tracking."""


mutable.MutableDict.associate_with(JsonObject)
NestedMutable.associate_with(NestedJsonObject)
