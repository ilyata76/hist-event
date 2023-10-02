from pathlib import Path
import yaml
import pyparsing
from io import BytesIO
from ftplib import FTP
from loguru import logger
from config import ftp_host, ftp_port, ftp_password, ftp_username,\
                    parse_keyword_special_symbols, parse_name_special_symbols
from datetime import datetime
############################

def dictFromYaml(path : Path, 
                 ftp : FTP = FTP(), 
                 repeated : int = 0) -> dict | list[dict] | None:
    """
        Открыть файл .yaml по пути path внутри FTP-сервера, 
            вернуть результат в виде словаря
    """
    if repeated > 1 :
        raise Exception("Не удалось подключиться к FTP-серверу и прочитать yaml-файлы!")

    try : 
        logger.info("Чтение {yaml} файла в {ftp}", yaml=path, ftp=f"{ftp_host}:{ftp_port}")
        
        file_bytes : bytes = b""
                
        def save_bytes(byts : bytes) :
            nonlocal file_bytes
            file_bytes = byts
            logger.debug("Размер file_bytes {w}", w=file_bytes.__len__())
            return file_bytes

        try : 
            ftp.retrbinary(f"RETR {path}", save_bytes)
        except Exception as exc:
            logger.debug("Переподключение в dictFromYaml к FTP")
            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_username, ftp_password)
            return dictFromYaml(path, ftp, repeated + 1)

        return yaml.load(file_bytes, Loader=yaml.FullLoader)
    
    except ConnectionRefusedError as exc:
        raise Exception(f"Нет подключения к FTP-серверу! [{exc}]")
    except Exception as exc:
        raise Exception(f"Нет такого файла {path} [{exc}]")


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


#stdout_file_bytes : bytes = b""
# stdout_path = stdout_log_folder.joinpath('generate-sql.stdout').__str__()

# def save_bytes(byts : bytes) :
#     """
#         Частый вызов функции => глобальные функция и переменная
#     """
#     global stdout_file_bytes
#     stdout_file_bytes = byts
#     return stdout_file_bytes


def msgFormat(msg : str) :
    return "[" + datetime.now().__str__() + "][generate-sql] " + msg


# def lprint(string : str, ftp : FTP = FTP(), repeated : int = 0) -> None :
#     """
#         Переопределённая функция print сохраняет вывод в консоль.
#             А также сохраняет вывод в файл generate-sql.stdout
#     """
#     try : 
#         # if repeated > 3 :
#         #     raise Exception("Не удалось подключиться к FTP-серверу и выполнить запись в stdout-лог!")
#         global stdout_path
#         temp_string = msgFormat(string) + "\n"
#         print(temp_string, end="")
#         # try :
#         #     byts = bytes(temp_string, encoding="utf-8")
#         #     try : 
#         #         ftp.retrbinary(f"RETR {stdout_path}", save_bytes)
#         #     except Exception :
#         #         pass
#         #     ftp.storbinary(f"STOR {stdout_path}", BytesIO(stdout_file_bytes + byts))
#         # except Exception as exc:
#         #     if exc.args[0] == "550 No such file or directory." :
#         #         ftp.mkd(stdout_log_folder.__str__())
#         #     ftp.connect(ftp_host, ftp_port)
#         #     ftp.login(ftp_username, ftp_password)
#         #     return lprint(string, ftp, repeated + 1)
#     except Exception as exc :
#         raise Exception(f"Не смог выполнить логирование в stdout! [{exc}]")