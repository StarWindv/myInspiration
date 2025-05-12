def find_executables(
        path: Union[str, Path],
        recursion: bool = False,
        include_symlinks: bool = False
) -> List[Path]:

    path_obj = Path(path).resolve()
    if not path_obj.is_dir():
        raise NotADirectoryError(f"|> {path} 不是有效的目录")

    executables = []
    walker = path_obj.rglob("*") if recursion \
        else path_obj.iterdir()

    for entry in walker:
        try:
            if not entry.is_file():
                continue
            if not include_symlinks and entry.is_symlink():
                continue

            if _is_executable(entry):
                executables.append(entry.absolute())
        except PermissionError:
            continue

    return executables

def _is_executable(path: Path) -> bool:
    if os.name == 'nt':
        valid_suffixes = {'.ps1', '.bat', '.cmd', '.exe'}
        return path.suffix.lower() in valid_suffixes
    else:
        return (
                os.access(path, os.X_OK) and
                filetype.guess(str(path)) in {'elf', 'shellscript'}
        )

def _gepd(arr: List)->Dict :
    """
    generate executable path dict
    :param arr: 可执行文件的路径列表
    :return: dict
    """
    name_path_dict = defaultdict(list)
    for path in arr:
        name = os.path.basename(path)
        name_path_dict[name].append(path)
    return name_path_dict