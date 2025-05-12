import os
from typing import IO

def _generate_dict(directory):
    file_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                abs_path = os.path.join(root, file)
                name_without_ext = os.path.splitext(file)[0]
                file_dict[name_without_ext] = abs_path
            continue
    return file_dict

def _get_length(file_path):
    count = 0
    block_size = 1024 * 1024
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                block = file.read(block_size)
                if not block:
                    break
                count += block.count('\n')
        return count
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        f.close()
    return 0

def rename_log(filepath):
    lines = _get_length(filepath)
    if lines > 1000:
        base, ext = os.path.splitext(filepath)
        i = 1
        while os.path.exists(f"{base}_{i}.bak{ext}"):
            i += 1
        new_filename = f"{base}_{i}.bak{ext}"
        os.rename(filepath, new_filename)
        return True, True # 打开文件成功，重命名成功
    return True, False # 打开文件成功，不需要重命名

def write(file: IO, content):
    file.write("|> "+content+"\n\n")
    file.flush()

def log(filepath, content):
    rename_log(filepath)
    with open(filepath, 'a', encoding='utf-8') as file:
        write(file, content)
        # print(filepath)

def helper(keys: str = None) -> None:
    content = {
        'cd': 'cd [path] : 切换当前工作目录',
        'exit': '退出此终端',
        'clear/cls': '清屏',
        'ori': 'ori [command] : 使用系统Shell执行目标command',
        'tree': 'tree args : 使用pytree生成目录树',
        'alias': 'alias [alias_name] [command_name] : 为目标命令创建别名',
        'ac': 'ac : 查看当前环境支持的命令(包括自定义扩展命令)',
        'ra': 'ra [alias_name] : 删除目标别名(空参数代表完全重置)',
        'rc': 'rc [command_name] : 删除目标命令(空参数代表完全重置)'
    }
    if keys:
        print(f"|> [HELP] {content[keys]}")
    else:
        for i, j in content.items():
            print(f"|> [HELP] {j}")