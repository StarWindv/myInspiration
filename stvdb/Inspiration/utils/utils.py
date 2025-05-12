from unicodedata import east_asian_width
from re import match as re_match, escape as re_escape # 进行重命名，防止隐藏名称警告
from typing import List, Optional, Union

def _process_prompt(name):
    if name is not None:
        name = name.strip()
        if not name.startswith('|'):
            name = '|' + name
        if not name.endswith('|') and not name.endswith(">"):
            name = name + '|'
        if not name[-1:-2] == '|' and name.endswith(">"):
            name = name[:-1] + '|'
        if not name.endswith(">"):
            name =  name + '>'
        name += ' '
    return name

def _gcw(char):
    """
    Get char width
    :param char: An character
    :return: int
    """
    width_category = east_asian_width(char)
    if width_category in ('F', 'W'):
        return 2
    else:
        return 1

def _process_len(dbname=''):
    return sum([_gcw(c) for c in dbname])

def _gwp(dbname=None):
    """
    Generate wait prompt
    :param dbname:
    :return: str
    """
    return (_process_len(dbname) - 2) * ' ' +'> '

def _swa(s: str, array: Optional[List[Union[str, int]]] = None) -> bool:
    """
    starts with any prefix
    :param s: your string
    :param array: target prefix list
    :return: bool
    """
    array = ['`', '.', '//', '~'] if not array else array
    array = [str(item) for item in array]
    pattern = '^(?:' + '|'.join(re_escape(prefix) for prefix in array) + ')'
    return bool(re_match(pattern, s))
