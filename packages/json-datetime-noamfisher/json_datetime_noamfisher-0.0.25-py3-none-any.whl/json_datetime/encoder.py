import json
from typing import Union, Any

from json_datetime.consts import (DATE_TYPES, VALUE_KEY, TYPE_KEY)


class JsonDatetimeEncoder(json.JSONEncoder):
    def default(self, o: Union[Any, DATE_TYPES]):
        if isinstance(o, DATE_TYPES.__args__):
            return {
                TYPE_KEY: type(o).__name__,
                VALUE_KEY: o.isoformat()
            }
        return super(JsonDatetimeEncoder, self).default(o)
