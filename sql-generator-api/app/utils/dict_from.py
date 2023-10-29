from google.protobuf import message
import yaml


def dictFromMessage(message : message.Message) -> dict :
    """Вернуть человекочитаемый словарь"""
    return { x.name:y for x,y in message.ListFields() }


def dictFromYaml(file : bytes, keyword : str | None = None) -> list[dict] :
    """
        Открыть .yaml файл, вернуть список словай с сущностями
    """
    result = yaml.load(file, Loader=yaml.FullLoader)
    
    if keyword :
        result = result[keyword]

    if not result :
        return []
    elif type(result) is dict or type(result) == dict :
        return [result]
    else :
        return result