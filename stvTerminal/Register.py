import os
import sys
import importlib

from thisutils import _generate_dict

from typing import Callable, List, Dict

CommandHandler = Callable[[List[str]], None]

class _CommandRegistry:
    def __new__(cls, *args, **kwargs):
        print("|> 初始化命令注册表")
        return super().__new__(cls)

    def __del__(self):
        print("|> 清除命令注册表")
        print("|> 清除别名注册表")

    def __init__(self):
        self.commands: Dict[str, CommandHandler] = {}
        self.aliases: Dict[str, str] = {}

    def register(self, name: str, handler: CommandHandler, inner: bool = False):
        if not inner:
            print(f"|> 注册命令: {name}")
        self.commands[name] = handler

    def add_alias(self, alias: str, command: str):
        if alias.startswith('.'):
            print(f"|> [Ban 001] The beginning of an alias cannot be '.'", file=sys.stderr)
            return
        self.aliases[alias] = command

    def _resolve_alias(self, name: str) -> str:
        original_name = name
        visited = set()
        while name in self.aliases:
            if name in visited:
                print(f"|> [Warn 002] Loop Alias'{original_name}'", file=sys.stderr)
                return original_name
            visited.add(name)
            name = self.aliases[name]
        return name

    def clean_commands(self, keys=None):
        if keys is None:
            self.commands: Dict[str, CommandHandler] = {}
        else:
            self.commands.pop(keys, None)
        print(f"|> [INFO] 重置命令表")

    def clean_alias(self, keys=None):
        if keys is None:
            self.aliases: Dict[str, CommandHandler] = {}
        else:
            self.aliases.pop(keys, None)
        print(f"|> [INFO] 重置别名表")

    def execute(self, name: str, args: List[str]):
        if name == 'ori':
            if self._execute_external_command('', args):
                return True

        if name.startswith("."):
            real_name = name.split('.')[-1]
        else:
            real_name = self._resolve_alias(name)

        # print(f"|> [INFO] true command: {real_name}")
        # print(f"|> [INFO] args: {' '.join(args)}")

        if real_name in self.commands:
            print(f"|> [INFO] 使用当前Shell执行命令: {real_name} {' '.join(args)}")
            self.commands[real_name](args)
            return True

        handler = self._load_code_command(real_name)
        if handler:
            CommandRegistry.register(real_name, handler)
            handler(args)
            return True

        if self._execute_external_command(real_name, args):
            return True

        print(f"|> [Err 000] Command Not Found: '{name}'", file=sys.stderr)
        return False

    @staticmethod
    def _load_code_command(command: str, path = None) -> CommandHandler:
        try:
            tar_dir = os.path.abspath(os.path.dirname(__file__) + "./commands")
            path = _generate_dict(tar_dir) if path is None else path
            # 生成一个py文件名与绝对路径对应的字典，名为键
            if command in path:
                module_name = command
                module_path = path[command]
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'main'):
                    return getattr(module, 'main')
        except Exception as e:
            print(f"|> [Err -01] Generalization error (PlaceHolder)")
            print(f"|> [ErrInfo] {e}", file=sys.stderr)

    @staticmethod
    def _execute_external_command(command: str, args: List[str]) -> bool:
        full_cmd = [command] + args
        full_cmd = " ".join(full_cmd)
        print("|> [INFO] 使用原生Shell执行命令: ", full_cmd)
        try:
            os.system(full_cmd)
            return True

        except Exception as e:
            print(f"|> [Err 003] Failed to execute external command")
            print(f"|> [ErrInfo] {str(e)}", file=sys.stderr)

        return False

CommandRegistry = _CommandRegistry()