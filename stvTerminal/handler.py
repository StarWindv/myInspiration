import sys
from typing import List
import os
from pathlib import Path
from Register import CommandRegistry

def handle_available_commands(*args):
    for i in CommandRegistry.commands.keys():
        print(f"|> {i}")

def handle_cd(args: List[str], default: str = None):
    """处理cd命令"""
    if default is None:
        default = Path.home()

    if not args:
        args.append(default)

    target_dir = args[0]
    try:
        os.chdir(target_dir)
        print(f"|> [INFO] 当前目录: {os.getcwd()}")
    except OSError as e:
        print(f"|> [Err cd] 无法切换到目录 '{target_dir}' - {str(e)}", file=sys.stderr)

def handle_exit(*args):
    print("\n|> 退出终端循环")
    sys.exit(0)

def handle_clear(*args):
    sys.stdout.write("\033[2J\033[H")

def handle_tree(args):
    os.system("pytree " + " ".join(args))

def handle_alias(args: List[str]):
    if len(args) < 2:
        print("|> [Err 002] Parameter quantity not aligned")
        print("|> [Usage] alias <alias> <command>")
        return
    elif len(args) > 2:
        print("|> [Warn 001] Currently only supports aliases without parameters")
        return
    CommandRegistry.add_alias(args[0], args[1])