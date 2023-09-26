from pathlib import Path
import yaml
import pyparsing
from ftplib import FTP
from loguru import logger
from config import ftp_host, ftp_port, ftp_password, ftp_username,\
                    parse_keyword_special_symbols, parse_name_special_symbols


def dictFromYaml(path : Path, 
                 ftp : FTP = FTP()) -> dict | list[dict] | None:
    """
        Открыть файл .yaml по пути path внутри FTP-сервера, 
            вернуть результат в виде словаря
    """
    try : 
        logger.info("Чтение {yaml} файла в {ftp}", yaml=path, ftp=f"{ftp_host}:{ftp_port}")
        
        file_bytes : bytes = b""
                
        def save_bytes(byts : bytes) :
            nonlocal file_bytes
            file_bytes = byts
            return file_bytes

        try : 
            ftp.retrbinary(f"RETR {path}", save_bytes)
        except Exception as exc:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_username, ftp_password)
            return dictFromYaml(path, ftp)

        return yaml.load(file_bytes, Loader=yaml.FullLoader)
    
    except ConnectionRefusedError as exc:
        raise Exception(f"Нет подключения к FTP-серверу! exc={exc}")
    except Exception as exc:
        raise Exception(f"Нет такого файла {path} exc={exc}")


def patternTextInclusion() -> pyparsing.ParserElement :
    """
        Для поиска { таких : 1 } [ ИМЯ ] вставок шаблон
    """

    keyword = pyparsing.alphas + parse_keyword_special_symbols
    number = pyparsing.nums
    name = pyparsing.alphanums + parse_name_special_symbols + pyparsing.ppu.Cyrillic.alphanums

    return pyparsing.Combine( pyparsing.Suppress("{") + 
                              pyparsing.ZeroOrMore(" ") + 
                              pyparsing.Word(keyword) + #' { abo'
                              pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + 
                              ":" + 
                              pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + #' : '
                              pyparsing.Word(number) + 
                              pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + 
                              pyparsing.Suppress("}") + #'1 }'
                              pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + # и имя 
                              "[" + 
                              pyparsing.ZeroOrMore(" ") + 
                              pyparsing.Word(name) + #'[ NAME'
                              pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + 
                              pyparsing.Suppress("]") ) #' ]'


def nullOrValue(value) -> str:
    """
        Функция для создания SQL-параметров при генерации таблиц
    """
    return "null" if not value else str(f"'{value}'")


def NOV(value) -> str :
    """
        Экономия места!
    """
    return nullOrValue(value)