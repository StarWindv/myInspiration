#! D:\python\python.exe
# ./Lexer.py

import re
from typing import Tuple, Generator

from ShellInput import _get_line
from utils.const import TOKEN_PATTERNS, KEYWORDS

# 定义Token类型
Token = Tuple[str, str]

class SQLLexer:
    def __new__(cls, *args, **kwargs):
        print("|> Initialized SQL Lexer")
        return super().__new__(cls)

    def __del__(self):
        print("|> Exit SQL Lexer")

    def __init__(self):
        # 编译正则表达式模式
        self.keyword_regex = self._compile_keywords()
        self.token_regex = re.compile(
            '|'.join(f'({pattern})' for pattern, _ in TOKEN_PATTERNS),
            re.IGNORECASE | re.DOTALL
        )
        self.token_types = [name for _, name in TOKEN_PATTERNS]

    @staticmethod
    def _compile_keywords():
        compiled = []
        for pattern, name in KEYWORDS:
            compiled.append((
                re.compile(pattern, re.IGNORECASE),
                name
            ))
        return compiled

    def tokenize(self, input_str: str) -> Generator[Token, None, None]:
        # 先处理多词关键字
        # input_str = input_str.upper()
        for regex, name in self.keyword_regex:
            input_str = regex.sub(lambda m: f' {name} ', input_str)

        # Tokenize其他元素
        pos = 0
        while pos < len(input_str):
            match = self.token_regex.match(input_str, pos)
            if not match:
                pos += 1
                continue

            for i in range(len(TOKEN_PATTERNS)):
                group = match.group(i+1)

                if group is not None:
                    token_type = self.token_types[i]
                    if token_type == 'WHITESPACE':
                        pos = match.end()
                        break

                    if token_type == 'SHELL_COMMAND':
                        yield 'SHELL_COMMAND', group
                        return

                    if token_type in ('COMMENT', 'BLOCK_COMMENT'):
                        pos = match.end()
                        break
                    value = group.strip()
                    yield token_type, value
                    pos = match.end()
                    break

if __name__ == '__main__':
    lexer = SQLLexer()

    generator = _get_line(name='dbname>')

    for statement in generator:
        print("完整语句:", repr(statement))

        for token in lexer.tokenize(statement):
            print(token)
