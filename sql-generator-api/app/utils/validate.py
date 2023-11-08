"""
    Функции валидации полей
"""
import datetime

from utils.exception import ValidationException as VE, ValidationExceptionCode as VECode


def validateEntityOnDict(entity_identifier : str, dict_entity) :
    if type(dict_entity) != dict :
        raise VE(code=VECode.INVALID_FIELD_OR_ENTITY_TYPE,
                 detail=f"Сущность {entity_identifier} представлена неправильно")


def validateFieldOnExisting(field : str, entity_identifier : str, 
                            dict_entity : dict) :
    if field not in dict_entity.keys() :
        raise VE(code=VECode.INVALID_FIELD, 
                 detail=f"У сущности {entity_identifier} поле {field} является обязательным")


cast_to_message = {
    int : " должно быть целочисленным типом",
    float : " должно быть числом с плавающей точкой",
    datetime.date.fromisoformat : " должно быть даты формата ISO или ключевой фразой",
    datetime.time.fromisoformat : " должно быть времени формата ISO или ключевой фразой",
}


def validateFieldOnCasting(field : str, entity_identifier : str, 
                           dict_entity : dict, cast : object) :
    if field in dict_entity.keys() :
        try :
            cast(dict_entity[field])
        except :
            message = f"У сущности {entity_identifier} поле {field}"
            message += cast_to_message.get(cast,  " определено неверно")
            raise VE(code=VECode.INVALID_FIELD_CONTENT, detail=message)


def validateFieldOnOneOfExisting(fields : list[str], entity_identifier : str, 
                                 dict_entity : dict) :
    if not any([field in dict_entity.keys() for field in fields]) :
        raise VE(code=VECode.INVALID_FIELD, 
                detail=f"У сущности {entity_identifier} хотя бы одно поле из {fields} является обязательным")


def validateFieldOnHTTP(field : str, entity_identifier : str, dict_entity : dict) :
    if dict_entity[field][0:4] != "http" :
        raise VE(code=VECode.INVALID_FIELD_CONTENT,
                 detail=f"У сущности {entity_identifier} поле {field} должно представлять собой HTTP-ссылку")


def validateFieldOnCrossExcluding(fields : list[str], entity_identifier : str, dict_entity : dict) :
    if [field in dict_entity.keys() for field in fields].count(True) > 1 :
        raise VE(code=VECode.CROSS_EXCLUDING_FIELDS,
                 detail=f"У сущности {entity_identifier} поля {fields} являются взаимоисключающими")


def validateFieldOnListInt(field : str, entity_identifier : str, dict_entity : dict) :
    if not all(isinstance(i, int) for i in dict_entity[field]) :
        raise VE(code=VECode.INVALID_FIELD_CONTENT,
                 detail=f"У сущности {entity_identifier} поле {field} должно представлять собой массив целых чисел")