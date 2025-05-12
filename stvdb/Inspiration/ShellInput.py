#!D:\Python\python.exe
# ./ShellInput.py

from sys import stdin, stdout
from utils.utils import _process_prompt, _gwp, _swa

def _get_line(name=None):
    """
    Interactive Input Processor

    交互式获取 SQL 语句，支持多行输入直到分号结尾
    返回一个生成器，每次 yield 一个完整语句

    :param name: your database name, string
    :return: yield return
    """
    # 1 进行判断，如果没有进行注释，则检测最后一个字符是否为分号
    # 2 如果是分号，则代表语句结束
    # 3 如果不是分号，则输入相应的继续提示，比如 "...>" 以代表延续行

    # 如果进行了单行注释，忽略注释符号后续的内容
    # 检测注释符号之前的内容，进入 2、3

    # 延续行时，如果是单行注释，则继续分析下一行内容
    # 如果是多行注释，从注释尾开始继续分析，
    # 直到遇到分号结尾为止

    # 当延续行时，每一行尾自动添加空格

    # 返回处理结果

    # 状态机
    single_quote = False     # 单引号模式
    double_quote = False     # 双引号模式
    block_note = False       # 块注释模式
    line_note = False        # 单行注释模式
    escape = False           # 转义状态
    buffer = []              # 当前语句缓冲区

    dbname = _process_prompt(name)

    prompt = "SQL > " if dbname is None else dbname # 初始提示符
    # 这里是用的三元表达式，格式大概是
    # 主语句 语句A if 条件 else 语句B
    # 如果条件成立，执行主语句+语句A，否则执行主语句+语句B

    wait_prompt = _gwp(prompt) # 重写一下...>的格式，长度要和dbname匹配

    interrupt_count = 0

    print("|> Initialize SQL Shell")

    while True:
        try:
            # 根据状态显示不同的提示符
            if prompt != wait_prompt:
                stdout.write('\n')
            stdout.write(prompt)
            stdout.flush()
            line = stdin.readline().rstrip('\n')  # 读取输入并去除换行符
        except EOFError:
            # 输入结束（如 Ctrl+D），强制终止
            print()  # 为了输出美观
            break

        except KeyboardInterrupt:
            # 清空缓冲区并重置所有状态
            single_quote = double_quote = block_note = line_note = escape = False
            buffer = []
            interrupt_count += 1
            if interrupt_count >= 2:
                break
            prompt = "SQL > " if dbname is None else dbname  # 重置提示符
            stdout.write("\n^C\n")  # 显示中断符号
            continue  # 直接进入下一轮循环

        interrupt_count = 0 # 重置中断计数器，只有连续按下两次中断才会彻底停止

        if (prompt != wait_prompt
                and not any([block_note, line_note, single_quote, double_quote, escape])
                and _swa(line)):
            # 我们用这种方式定义了，以某种特殊前缀开头的字符串为命令
            # 直接将对应开头的行视为完整行
            yield line
            continue

        if prompt == wait_prompt and not any([block_note, line_note, single_quote, double_quote, escape]):
            buffer.append(' ')  # 在缓冲区添加分隔空格

        i = 0
        while i < len(line):
            char = line[i]

            if escape:
                # 处理转义字符：直接写入缓冲区，取消特殊符号作用
                buffer.append(char)
                escape = False
                i += 1
                continue

            if char == '\\':
                # 转义符：标记下一个字符为普通字符
                escape = True
                i += 1
                continue

            # ┌──────────────── 优先级：引号 > 注释 > 分号 ────────────────┐
            if block_note:
                # 块注释中，寻找 */ 退出
                if char == '*' and i+1 < len(line) and line[i+1] == '/':
                    block_note = False
                    i += 2  # 跳过 */
                else:
                    i += 1
                continue

            if line_note:
                # 单行注释中，忽略剩余字符
                break

            if single_quote or double_quote:
                # 引号模式中，直接写入字符
                buffer.append(char)
                if (char == "'" and single_quote) or (char == '"' and double_quote):
                    single_quote = double_quote = False
                i += 1
                continue
            # └──────────────────────────────────────────────────────────┘

            # 检测特殊符号（不在引号/注释中）
            if char == '-' and i+1 < len(line) and line[i+1] == '-':
                # 单行注释：忽略本行剩余内容
                line_note = True
                break

            if char == '/' and i+1 < len(line) and line[i+1] == '*':
                # 块注释开始
                block_note = True
                i += 2
                continue

            if char in ("'", '"'):
                # 进入引号模式
                buffer.append(char)
                single_quote = (char == "'")
                double_quote = (char == '"')
                i += 1
                continue

            if char == ';':
                # 分号结束语句
                buffer.append(';')
                yield ''.join(buffer)
                buffer = []
                prompt = "SQL > " if dbname is None else dbname
                i += 1
                continue

            # 普通字符直接写入缓冲区
            buffer.append(char)
            i += 1

        # 在行尾重置单行注释模式状态
        line_note = False

        # 更新提示符：如果存在未闭合状态，则显示延续提示符
        if block_note or single_quote or double_quote or escape:
            prompt = wait_prompt
        elif buffer:  # 缓冲区有内容但未闭合（如未以分号结尾）
            prompt = wait_prompt
        else:
            prompt = "SQL > " if dbname is None else dbname

    print(f"\n\n|> Exit Interactive Input Processor")
    return True # 进行一次return，说不定后续有用

if __name__ == '__main__':
    # 通过生成器逐条获取完整语句
    generator = _get_line(name='dbname>')
    for statement in generator:
        print("完整语句:", repr(statement))
