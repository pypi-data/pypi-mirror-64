"""Context manager for atomically writing data to a file path"""
from contextlib import contextmanager
from pathlib import Path
from stat import S_IRUSR
from stat import S_IRWXG
from stat import S_IRWXU
from stat import S_IWUSR
from tempfile import TemporaryDirectory
from typing import Generator
from typing import Union

from atomicwrites import move_atomic
from atomicwrites import replace_atomic


__version__ = "1.0.0"


@contextmanager
def atomic_write_path(
    destination: Union[Path, str],
    *,
    dir_perms: int = S_IRWXU | S_IRWXG,
    overwrite: bool = False,
    file_perms: int = S_IRUSR | S_IWUSR,
) -> Generator[Path, None, None]:
    destination = Path(destination)
    parent = destination.parent
    parts = parent.parts
    for i in range(len(parts)):
        path_parent = Path(*parts[: (i + 1)])
        try:
            path_parent.mkdir(mode=dir_perms)
        except FileExistsError:
            pass
    name = destination.name
    with TemporaryDirectory(suffix=".tmp", prefix=name, dir=parent) as temp_dir:
        source = Path(temp_dir).joinpath(name)
        yield source
        if overwrite:
            replace_atomic(str(source), str(destination))
        else:
            move_atomic(str(source), str(destination))
        destination.chmod(file_perms)
