from collections.abc import Iterable

from google.protobuf import message
from pydantic import BaseModel

from config import config


def dictFromGoogleMessage(message : message.Message) -> dict :
    """Вернуть человекочитаемый словарь"""
    return { x.name:y for x,y in message.ListFields() }


def __formateStr(string : str) :
    return string.__str__().replace("\n", " ")

def __cutStr(string) :
    return string if len(str(string)) < config.LOG_CUT_LEN else string[:config.LOG_CUT_LEN] + "........."

def cutLogStr(string : str | None = None) -> str :
    if not string : return "NONE"
    string = __formateStr(string)
    return __cutStr(string)

# взаимная рекурсия между cutLog и VVV

def cutLogArgs(args : list | None = None) -> str :
    if not args : return "WITHOUT ARGS"
    string_array = []
    for arg in args :
        arg = __formateStr(arg)
        string_array.append(cutLog(arg))
    return "(" + ", ".join(string_array) + ")"

def cutLogKwargs(kwargs : dict | None = None) -> str :
    if not kwargs : return "WITHOUT KWARGS"
    string_array = []
    for key, value in kwargs.items() :
        key = __formateStr(key)
        value = __formateStr(value)
        string_array.append(key + "=" + cutLog(value))
    return "{" + ", ".join(string_array) + "}"

def cutLogGoogleMessage(message : message.Message) -> str :
    result_dict = {}
    for key, value in message.ListFields() :
        # if isinstance(value, Iterable)  : #     value = cutLogArgs(value) # else : #     value = cutLogStr(value)
        value = cutLog(value)
        result_dict.update({key.name:value})
    return result_dict

def cutLog(arg : str | Iterable | message.Message) :
    if isinstance(arg, bytes) :
        return "*BYTES*"
    if isinstance(arg, dict) :
        return cutLogKwargs(arg)
    if isinstance(arg, message.Message) :
        return cutLogGoogleMessage(arg)
    if isinstance(arg, str) or isinstance(arg, BaseModel):
        return cutLogStr(arg)
    if isinstance(arg, Iterable) :
        return cutLogArgs(arg)
    return cutLogStr(arg.__str__())


from .exception import *