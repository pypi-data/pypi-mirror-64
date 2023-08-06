import datetime
from typing import Union, Type

DATETIME_TYPE = datetime.datetime
DATE_TYPE = datetime.date
DATE_TYPES = Union[DATETIME_TYPE, DATE_TYPE]
DATE_CLS_TYPES = Union[Type[DATE_TYPE], Type[DATETIME_TYPE]]
TYPE_KEY = '__type__'
VALUE_KEY = '__value__'
