import os
import shlex
from getpass import getuser

from thisutils import log
from initialize import register_builtin_commands
from Register import CommandRegistry

import os

def injection(name: str = None, value: str = None, show = False):
    name = 'stv-terminal-depth' if name is None else name
    value = '0' if value is None else value
    name, value = str(name), str(value)
    os.environ[name] = str(value)
    if show:
        print("|> [INFO] Set Environment Variable: " + name + " = " + value)

def depth_check():
    if not 'stv-terminal-depth' in os.environ:
        injection()
        return 1, True
    depth = int(os.environ['stv-terminal-depth'])
    injection(value=depth+1)
    return depth+1, True

def main():
    """启动终端循环"""
    register_builtin_commands()
    print("|> 初始化终端变量")
    log_path = os.path.join(os.path.expanduser("~"), "log/log.txt")
    username = getuser()
    print("|> 启动终端循环")

    depth = depth_check()
    if depth[-1]:
        if depth[0] >= 2:
            print(f"|> [Warn 004] Multi layer terminal nesting")

    while True:
        try:
            cwd = os.getcwd()
            if cwd == os.path.expanduser("~"):
                cwd = "~"
            prompt = f"\n{username}:{cwd} $ "
            line = input(prompt).strip()
            if not line:
                continue

            log(log_path, line)
            parts = shlex.split(line)
            command = parts[0] if parts else ""
            args = parts[1:]
            if not CommandRegistry.execute(command, args):
                continue

        except PermissionError:
            print("|> [Err 001] Permission Denied")
            continue
        except KeyboardInterrupt:
            print("\n|> 已中断当前操作")
            continue
        except EOFError:
            print("\n|> 退出终端循环")
            break
        except Exception as e:
            print(f"|> [Err -02] Inner Error")
            print(f"|> [ErrInfo] {e}")

if __name__ == "__main__":
    main()