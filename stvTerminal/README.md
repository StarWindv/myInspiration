# stvTerminal - 自定义交互式终端工具

`stvTerminal` 是一个功能丰富的自定义交互式终端工具，支持内置命令、命令别名和插件扩展。它提供了友好的用户界面和强大的功能，适合开发者和系统管理员使用。

## 功能特点

- 支持丰富的内置命令，如 `cd`, `ra`, `rc` 等
- 命令别名系统，可自定义命令缩写
- 插件扩展机制，支持动态加载自定义命令
- 命令历史记录和日志记录
- 
## 环境与使用

### 环境

你需要`filetype`和`stv_pytree`这个两个库
```bash
pip install filetype stv_pytree
```

### 启动终端

```bash
python main.py
```

### 基本命令

```
cd [path] : 切换当前工作目录
exit: 退出此终端
clear/cls: 清屏
ori [command] : 使用系统Shell执行目标command,
tree args : 使用pytree生成目录树
alias [alias_name] [command_name] : 为目标命令创建别名
ac : 查看当前环境支持的命令(包括自定义扩展命令)
ra [alias_name] : 删除目标别名(空参数代表完全重置)
rc [command_name] : 删除目标命令(空参数代表完全重置)
```

## 自定义插件

`stvTerminal` 支持通过插件扩展功能。要创建自定义命令，只需在 `commands` 目录下创建一个 Python 文件，并定义 `main` 函数：

```python
# commands/hello.py
def main(*args, **kwargs):
    print("Hello, Custom Function!")
```
文件名就是新的命令名

无论你的main函数需不需要参数，我都建议你在里面加入 *args, **kwargs 以吸收参数，因为终端会传递一个列表给你的main函数


## 贡献

欢迎贡献代码、报告issue或pr。

## 许可证

本项目采用 MIT 许可证，详情请见 LICENSE 文件。
