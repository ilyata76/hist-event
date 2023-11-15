"""
    Класс, связанный с парсингом и поиском вставок в текстах
"""
import pyparsing

from config import config
from schemas import ParseResult


class InclusionParser :

    @staticmethod
    def __pattern() -> pyparsing.ParserElement :
        keyword = pyparsing.alphas + config.PARSE_KEYWORD_SPECIAL_SYMBOLS
        number = pyparsing.nums
        name = pyparsing.alphanums + config.PARSE_NAME_SPECIAL_SYMBOLS + pyparsing.ppu.Cyrillic.alphanums

        return pyparsing.Combine( pyparsing.Suppress("{") + 
                                pyparsing.ZeroOrMore(" ") + 
                                      pyparsing.Word(keyword) +     #' { abo'
             pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + 
                                                     ":" + 
             pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) +        #' : '
                                      pyparsing.Word(number) + 
             pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + 
                                  pyparsing.Suppress("}") +         #'1 }'
             pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) +        # и имя 
                                                     "[" + 
                                pyparsing.ZeroOrMore(" ") + 
                                      pyparsing.Word(name) +        #'[ NAME'
             pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + 
                                  pyparsing.Suppress("]") )         #' ]'


    @staticmethod
    def getEntitiesFromString(string : str) -> list[ParseResult] :
        parse_list : list = InclusionParser.__pattern().searchString(string).as_list()
        result : list[ParseResult] = []
        for x in parse_list :
            stroke : str = x[0]
            result.append( ParseResult(keyword=stroke.split(':')[0].strip(),
                                       number=stroke.split(':')[1].strip().split('[')[0].strip(),
                                       name=stroke.split('[')[1].strip()) )
        return result