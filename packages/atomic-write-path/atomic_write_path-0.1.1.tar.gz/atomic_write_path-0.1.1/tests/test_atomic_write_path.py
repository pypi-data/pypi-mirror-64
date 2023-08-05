from pathlib import Path
from stat import S_IRUSR
from stat import S_IRWXG
from stat import S_IRWXO
from stat import S_IRWXU
from stat import S_IWUSR
from stat import S_IXUSR

from pytest import raises

from atomic_write_path import atomic_write_path


def test_basic_usage(tmp_path: Path) -> None:
    path = tmp_path.joinpath("file")
    with atomic_write_path(path) as temp:
        with open(temp, mode="w") as fh:
            fh.write("contents")
    with open(path) as fh:
        assert fh.read() == "contents"


def test_file_exists_error(tmp_path: Path) -> None:
    path = tmp_path.joinpath("file")
    with atomic_write_path(path) as temp:
        with open(temp, mode="w") as fh:
            fh.write("contents")
    with raises(FileExistsError, match=str(path)):
        with atomic_write_path(path) as temp:
            with open(temp, mode="w") as fh:
                fh.write("new contents")


def test_dir_perms(tmp_path: Path) -> None:
    path = tmp_path.joinpath("dir1/dir2/dir3/file")
    with atomic_write_path(path, dir_perms=S_IRWXU) as temp:
        with open(temp, mode="w") as fh:
            fh.write("contents")
    parts = path.relative_to(tmp_path).parent.parts
    for i in range(len(parts)):
        path_parent = tmp_path.joinpath(*parts[: (i + 1)])
        assert path_parent.is_dir()
        assert path_parent.stat().st_mode & S_IRWXU & (~S_IRWXG) & (~S_IRWXO)


def test_overwrite(tmp_path: Path) -> None:
    path = tmp_path.joinpath("file")
    with atomic_write_path(path) as temp:
        with open(temp, mode="w") as fh:
            fh.write("contents")
    with atomic_write_path(path, overwrite=True) as temp:
        with open(temp, mode="w") as fh:
            fh.write("new contents")
    with open(path) as fh:
        assert fh.read() == "new contents"


def test_file_perms(tmp_path: Path) -> None:
    path = tmp_path.joinpath("file")
    with atomic_write_path(path, file_perms=S_IRUSR) as temp:
        with open(temp, mode="w") as fh:
            fh.write("contents")
    assert (
        path.stat().st_mode
        & S_IRUSR
        & (~S_IWUSR)
        & (~S_IXUSR)
        & (~S_IRWXG)
        & (~S_IRWXO)
    )
