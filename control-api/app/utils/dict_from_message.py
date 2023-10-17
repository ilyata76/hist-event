from google.protobuf import message

def dict_from_message(message : message.Message) :
    """Вернуть человекочитаемый словарь"""
    return { x.name:y for x,y in message.ListFields() }