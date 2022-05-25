import shutil
import pytest
import os


temp_dir_path = "tmpdir"


@pytest.fixture(scope="module")
def use_temp_dir():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)

    tmp_dir = current_dir + f"/{temp_dir_path}"

    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
        assert os.path.exists(tmp_dir)
        print(os.path.abspath(tmp_dir))

    yield

    shutil.rmtree(tmp_dir)
    assert not os.path.exists(tmp_dir)


def create_directory(dirname: str) -> str:
    base_path = os.path.dirname(__file__)
    new_dir_path = os.path.join(base_path, temp_dir_path, dirname)

    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path, exist_ok=True)

    return new_dir_path


def remove_directory(dirname: str):
    base_path = os.path.dirname(__file__)
    dir_path = os.path.join(base_path, temp_dir_path, dirname)

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


def create_file(dir_path: str, filename: str, content: str = "Some new text file"):
    with open(os.path.join(dir_path, filename), "w") as f:
        f.write(content)
