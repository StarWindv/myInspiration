from handler import (handle_available_commands, handle_alias,
                     handle_exit, handle_cd, handle_clear,
                     handle_tree)
from Register import CommandRegistry
from thisutils import helper

def register_builtin_commands(inner = False):
    """注册常用内置命令"""
    print("|> 注册常用命令")
    cmd_array = ['cd', 'exit', 'clear', 'tree', 'alias',
                 'ac', 'ra', 'help']
    func_array = [handle_cd, handle_exit, handle_clear,
                  handle_tree, handle_alias, handle_available_commands,
                  reset_alias, helper]
    if not inner:
        cmd_array.append('rc')
        func_array.append(reset_commands)
    for cmd, func in zip(cmd_array, func_array):
        CommandRegistry.register(cmd, func, inner=True)

    print("|> 注册常用命令别名")
    CommandRegistry.add_alias('cls', 'clear')
    CommandRegistry.add_alias('logout', 'exit')
    CommandRegistry.add_alias('/?', 'help')

def reset_commands(keys = None):
    CommandRegistry.clean_commands(keys = ' '.join(keys))
    register_builtin_commands(inner=True)

def reset_alias(keys = None):
    CommandRegistry.clean_alias(keys = ' '.join(keys))
