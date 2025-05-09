#! D:\python\python.exe
# ./utils/const.py

KEYWORDS = [
    (r'\bBEGIN\s+TRANSACTION\b', 'BEGIN_TRANSACTION'),
    (r'\bSTART\s+TRANSACTION\b', 'START_TRANSACTION'),
    (r'\bGROUP\s+BY\b', 'GROUP_BY'),
    (r'\bORDER\s+BY\b', 'ORDER_BY'),
    (r'\bCREATE\b', 'CREATE'), (r'\bSELECT\b', 'SELECT'),
    (r'\bINSERT\b', 'INSERT'), (r'\bUPDATE\b', 'UPDATE'),
    (r'\bDELETE\b', 'DELETE'), (r'\bALTER\b', 'ALTER'),
    (r'\bSET\b', 'SET'), (r'\bUNION\b', 'UNION'),
    (r'\bGROUP\b', 'GROUP'), (r'\bDROP\b', 'DROP'),
    (r'\bGRANT\b', 'GRANT'), (r'\bREVOKE\b', 'REVOKE'),
    (r'\bCOMMIT\b', 'COMMIT'), (r'\bROLLBACK\b', 'ROLLBACK'),
    (r'\bWHERE\b', 'WHERE'), (r'\bJOIN\b', 'JOIN'),
    (r'\bHAVING\b', 'HAVING'), (r'\bASC\b', 'ASC'),
    (r'\bDESC\b', 'DESC'), (r'\bINNER\b', 'INNER'),
    (r'\bLEFT\b', 'LEFT'), (r'\bRIGHT\b', 'RIGHT'),
    (r'\bFULL\b', 'FULL'), (r'\bOUTER\b', 'OUTER'),
    (r'\bJOIN\b', 'JOIN'), (r'\bAS\b', 'AS'),
    (r'\bON\b', 'ON'),
    (r'\bAND\b', 'AND'), (r'\bOR\b', 'OR'),
    (r'\bNOT\b', 'NOT'), (r'\bIS\b', 'IS'),
    (r'\bNULL\b', 'NULL'), (r'\bLIKE\b', 'LIKE'),
    (r'\bIN\b', 'IN'), (r'\bBETWEEN\b', 'BETWEEN'),
    (r'\bEXISTS\b', 'EXISTS'), (r'\bALL\b', 'ALL'), (r'\bANY\b', 'ANY'),
    (r'\bDISTINCT\b', 'DISTINCT'), (r'\bFROM\b', 'FROM'),
    (r'\bINTO\b', 'INTO'),
    (r'\bVALUES\b', 'VALUES'), (r'\bTABLE\b', 'TABLE'),
    (r'\bINDEX\b', 'INDEX'), (r'\bVIEW\b', 'VIEW'),
    (r'\bCASE\b', 'CASE'), (r'\bWHEN\b', 'WHEN'),
    (r'\bTHEN\b', 'THEN'), (r'\bELSE\b', 'ELSE'),
    (r'\bEND\b', 'END')
]


TOKEN_PATTERNS = [
    *KEYWORDS,
    (r'`.*', 'SHELL_COMMAND'),        # Shell命令
    (r'\..*', 'SHELL_COMMAND'),      # Shell命令
    (r'~.*', 'SHELL_COMMAND'),       # Shell命令
    (r'//.*', 'SHELL_COMMAND'),       # Shell命令
    (r'--.*', 'COMMENT'),             # 单行注释
    (r'\/\*.*?\*\/', 'BLOCK_COMMENT'),# 块注释
    (r';', 'SEMICOLON'),
    (r',', 'COMMA'),
    (r'\*', 'ASTERISK'),
    (r'=', 'EQUALS'),
    (r'!=', 'NOT_EQUAL'),
    (r'<', 'LESS_THAN'),
    (r'>', 'GREATER_THAN'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\d+', 'NUMBER'),
    (r"'[^']*'", 'STRING'),           # 单引号字符串
    (r'"[^"]*"', 'STRING'),           # 双引号字符串
    # (r'\b\w+\b', 'IDENTIFIER'),       # 标识符
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
    (r'\s+', 'WHITESPACE')            # 空白字符
]