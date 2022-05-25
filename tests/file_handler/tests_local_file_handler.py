import re
import os
import pytest
from cakeslicer.src.core.errors import (
    LocalFileHandlerErrorMessages as messages,
    ValueError,
    FileReadingError,
    CopyError,
)
from cakeslicer.src.file_handler import local_file_handler as file_handler
from cakeslicer.tests.file_handler.conftest import (
    temp_dir_path,
    create_directory,
    create_file,
    remove_directory,
)


def test_get_caller_base_dir_correctly_gets_the_first_caller_outside_the_file_handler_directory():
    current_dir = os.path.dirname(__file__)

    caller_dir = file_handler._get_caller_base_dir()

    assert caller_dir == current_dir


def test_get_full_path_correctly_for_same_directory():
    current_dir = os.path.dirname(__file__) + "/"

    path = "somedir/somefile.txt"
    relative_path = f"./{path}"

    expected_path = current_dir + path

    full_path = file_handler._get_full_path(relative_path)

    assert full_path == expected_path


def test_get_full_path_correctly_for_a_directory_above_the_current_one():
    current_file_path = os.path.abspath(__file__ + "/../../../")
    current_dir = os.path.dirname(current_file_path) + "/"

    path = "somedir/somefile.txt"
    relative_path = f"../../../{path}"

    expected_path = current_dir + path

    full_path = file_handler._get_full_path(relative_path)

    assert full_path == expected_path


def test_get_full_path_ignores_directory_up_syntax_in_the_middle_of_the_string():
    current_file_path = os.path.abspath(__file__ + "/../../../")
    current_dir = os.path.dirname(current_file_path) + "/"

    path = "somedir/../somefile.txt/../"
    relative_path = f"../../../{path}"

    expected_path = current_dir + path

    full_path = file_handler._get_full_path(relative_path)

    assert full_path == expected_path
    assert full_path[-3:] == "../"
    assert len(re.findall(r"\.\.\/", full_path)) == 2


def test_is_path_returns_false_when_the_file_doesnt_exist():
    inexistent_file_path = "./idontexist.txt"

    is_path = file_handler.is_path(inexistent_file_path)

    assert not is_path


def test_is_path_returns_false_when_the_directory_doesnt_exist():
    inexistent_dir_path = "./idontexist/"

    is_path = file_handler.is_path(inexistent_dir_path)

    assert not is_path


def test_is_path_returns_false_when_the_value_passed_doesnt_correspond_to_a_path():
    is_path = file_handler.is_path(["abacaxi", 123])

    assert not is_path


def test_is_path_returns_true_when_the_directory_exists(use_temp_dir):
    dirname = "somedir"
    existent_dir_path = f"{temp_dir_path}/{dirname}"

    create_directory(dirname)

    is_path = file_handler.is_path(existent_dir_path)

    remove_directory(dirname)

    assert is_path


def test_is_path_returns_true_when_the_file_exists(use_temp_dir):
    dirname = "somedir"
    existent_file_path = f"{temp_dir_path}/somedir/somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, "somefile.txt")

    is_path = file_handler.is_path(existent_file_path)

    remove_directory(dirname)

    assert is_path


def test_validate_existing_path_does_nothing_when_the_path_exists():
    dirname = "somedir"
    existent_dir_path = f"{temp_dir_path}/{dirname}"

    create_directory(dirname)

    try:
        file_handler._validate_existing_path(existent_dir_path)
    except Exception:
        assert False, "An exception was raised"

    remove_directory(dirname)


def test_validate_existing_path_raises_an_error_when_the_path_does_not_exist_on_the_document_tree():
    inexistent_dir_path = f"{temp_dir_path}/somedir"

    with pytest.raises(ValueError) as error:
        file_handler._validate_existing_path(inexistent_dir_path)

    assert str(error.value) == messages.invalid_path


@pytest.mark.parametrize(
    "path",
    [
        "/Users/someuser/bin",
        "/Users/someuser/bin/",
        "/Users/someuser/bin/executable.sh",
        "C:/Users/someuser/bin",
        "C:/Users/someuser/bin/executable.exe",
        "./bin/",
        "./music/somemusic.mp3",
        "../../pictures/somepicture.jpeg",
        "bin/",
        "bin/executable.sh",
        "/.hiddendir",
        "/.hiddendir/somefile.wma",
        "./.hiddendir/.hiddenfile.docx",
        "../../../.hiddendir/.hiddenfile.docx",
    ],
)
def test_validate_path_format_does_nothing_when_the_path_is_a_valid_path(path):
    try:
        file_handler._validate_path_format(path)
    except Exception:
        assert False, "An exception was raised"


@pytest.mark.parametrize(
    "path",
    ["//bin/", "/bin//", "/somefolder/1nv@l1dn@m3$/"],
)
def test_validate_path_format_raises_an_error_when_the_path_has_an_incorrect_format(
    path,
):
    with pytest.raises(ValueError) as error:
        file_handler._validate_path_format(path)

    assert str(error.value) == messages.invalid_path


def test_read_file_gets_the_content_of_a_file():
    dirname = "somedir"
    content = "I need to read this text.\nIs this a new line?"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, "somefile.txt", content)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    file_contents = file_handler.read_file(file_path)

    remove_directory(dirname)

    assert file_contents == content


def test_read_file_raises_a_file_reading_error_if_it_fails_opening_the_file(
    monkeypatch,
):
    dirname = "somedir"
    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, "somefile.txt")

    monkeypatch.setattr("builtins.open", None, raising=True)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(FileReadingError) as error:
        file_handler.read_file(file_path)

    assert str(error.value) == messages.couldnt_read_file


@pytest.mark.parametrize(
    "search_subject, expected_result",
    [
        ("this text", ["this text"]),
        ("this", ["this", "this"]),
        ("not present string", []),
        ("(t|T)[a-z]+", ["to", "this", "text", "this"]),
        ("", []),
    ],
)
def test_search_gets_the_list_of_the_matching_substrings_inside_the_file(
    search_subject, expected_result
):
    dirname = "somedir"
    content = "I need to read this text.\nIs this a new line?"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, "somefile.txt", content)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    search_result = file_handler.search(search_subject, file_path)

    remove_directory(dirname)

    assert search_result == expected_result


def test_search_raises_a_file_reading_error_if_it_fails_opening_the_file(monkeypatch):
    dirname = "somedir"
    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, "somefile.txt")

    monkeypatch.setattr("builtins.open", None, raising=True)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(FileReadingError) as error:
        file_handler.search("any search subject", file_path)

    remove_directory(dirname)

    assert str(error.value) == messages.couldnt_read_file


def test_search_raises_a_value_error_if_the_subject_is_not_a_string():
    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(ValueError) as error:
        file_handler.search(True, file_path)

    assert str(error.value) == messages.invalid_type_for_parameter("subject")


def test_search_raises_a_value_error_if_the_path_is_invalid():
    dirname = "somedir"
    remove_directory(dirname)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(ValueError) as error:
        file_handler.search("subject", file_path)

    assert str(error.value) == messages.invalid_path


@pytest.mark.parametrize(
    "search_subject, replacement, expected_result",
    [
        (
            "a new",
            "an old",
            "I need to read this text.\nIs this an old line?\n\n// Some comment: start\nSomething not in a comment\n// Some comment: end",
        ),
        (
            "// Some comment: start\n",
            "",
            "I need to read this text.\nIs this a new line?\n\nSomething not in a comment\n// Some comment: end",
        ),
        (
            "\n// Some comment: (start|end)",
            "",
            "I need to read this text.\nIs this a new line?\n\nSomething not in a comment",
        ),
        (
            "\n// Some comment: start(.|\n)*// Some comment: end",
            "",
            "I need to read this text.\nIs this a new line?\n",
        ),
    ],
)
def test_replace_content_updates_the_files_content(
    search_subject, replacement, expected_result
):
    dirname = "somedir"
    file_name = "somefile.txt"
    content = "I need to read this text.\nIs this a new line?\n\n// Some comment: start\nSomething not in a comment\n// Some comment: end"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name, content)

    file_path = f"./{temp_dir_path}/somedir/{file_name}"

    new_content_file = file_handler.replace_content(
        search_subject, replacement, file_path
    )

    assert new_content_file == expected_result

    with open(f"{new_dir_path}/{file_name}", "r") as file:
        assert file.read() == new_content_file

    remove_directory(dirname)


def test_replace_content_does_nothing_when_the_search_subject_is_empty():
    dirname = "somedir"
    file_name = "somefile.txt"
    content = "I need to read this text.\nIs this a new line?\n\n// Some comment: start\nSomething not in a comment\n// Some comment: end"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name, content)

    file_path = f"./{temp_dir_path}/somedir/{file_name}"

    new_content_file = file_handler.replace_content("", "replacement", file_path)

    assert new_content_file == None

    with open(f"{new_dir_path}/{file_name}", "r") as file:
        assert file.read() == content

    remove_directory(dirname)


def test_replace_content_a_file_reading_error_if_it_fails_opening_the_file(monkeypatch):
    dirname = "somedir"
    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, "somefile.txt")

    monkeypatch.setattr("builtins.open", None, raising=True)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(FileReadingError) as error:
        file_handler.replace_content("any search subject", "any replacement", file_path)

    remove_directory(dirname)

    assert str(error.value) == messages.couldnt_read_file


def test_replace_content_a_value_error_if_the_subject_is_not_a_string():
    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(ValueError) as error:
        file_handler.replace_content(True, "", file_path)

    assert str(error.value) == messages.invalid_type_for_parameter("subject")


def test_replace_content_a_value_error_if_the_replacement_is_not_a_string():
    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(ValueError) as error:
        file_handler.replace_content("some string", True, file_path)

    assert str(error.value) == messages.invalid_type_for_parameter("replacement")


def test_replace_content_a_value_error_if_the_path_is_invalid():
    dirname = "somedir"
    remove_directory(dirname)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(ValueError) as error:
        file_handler.replace_content("subject", "", file_path)

    assert str(error.value) == messages.invalid_path


def test_copy_copies_a_single_file():
    dirname = "somedir"
    copied_dir_name = "copieddir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    file_path = f"./{temp_dir_path}/{dirname}/{file_name}"
    copy_file_path = f"{temp_dir_path}/{copied_dir_name}/{file_name}"

    file_handler.copy(file_path, copy_file_path)

    assert os.path.exists(os.path.dirname(__file__) + f"/{copy_file_path}")

    remove_directory(dirname)
    remove_directory(copied_dir_name)


def test_copy_copies_a_whole_directory_with_its_contents():
    dirname = "somedir"
    copied_dir_name = "copieddir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    file_path = f"./{temp_dir_path}/{dirname}/{file_name}"
    copy_dir_path = f"{temp_dir_path}/{copied_dir_name}"
    full_copy_dir_path = os.path.dirname(__file__) + f"/{copy_dir_path}"

    file_handler.copy(file_path, copy_dir_path)

    assert os.path.exists(full_copy_dir_path)
    assert os.path.exists(f"{full_copy_dir_path}/{file_name}")

    remove_directory(dirname)
    remove_directory(copied_dir_name)


def test_copy_raises_a_value_error_if_the_original_path_is_invalid():
    dirname = "somedir"
    remove_directory(dirname)

    file_path = f"./{temp_dir_path}/somedir/somefile.txt"

    with pytest.raises(ValueError) as error:
        file_handler.copy(file_path, "./destination_path/")

    assert str(error.value) == messages.invalid_path


def test_copy_raises_a_values_error_if_the_destination_path_has_an_invalid_format():
    dirname = "somedir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    file_path = f"./{temp_dir_path}/{dirname}/{file_name}"

    with pytest.raises(ValueError) as error:
        file_handler.copy(file_path, "/usr/d&s71n@710n_p@7h")

    assert str(error.value) == messages.invalid_path

    remove_directory(dirname)


def test_copy_raises_a_copy_error_if_the_file_copy_process_goes_wrong(monkeypatch):
    dirname = "somedir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    monkeypatch.setattr("shutil.copy", None, raising=True)

    file_path = f"./{temp_dir_path}/{dirname}/{file_name}"
    new_file_path = f"./{temp_dir_path}/otherdir/{file_name}"

    with pytest.raises(CopyError) as error:
        file_handler.copy(file_path, new_file_path)

    assert str(error.value) == messages.failed_to_copy("file")

    remove_directory(dirname)


def test_copy_raises_a_copy_error_if_the_directory_copy_process_goes_wrong(monkeypatch):
    dirname = "somedir"
    copied_dir_name = "copieddir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    monkeypatch.setattr("shutil.copytree", None, raising=True)

    file_path = f"./{temp_dir_path}/{dirname}"
    new_file_path = f"./{temp_dir_path}/{copied_dir_name}"

    with pytest.raises(CopyError) as error:
        file_handler.copy(file_path, new_file_path)

    assert str(error.value) == messages.failed_to_copy("directory")

    remove_directory(dirname)


def test_copy_file_copies_a_single_file():
    dirname = "somedir"
    copied_dir_name = "copieddir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    full_file_path = (
        os.path.dirname(__file__) + f"/{temp_dir_path}/{dirname}/{file_name}"
    )
    full_copy_file_path = (
        os.path.dirname(__file__) + f"/{temp_dir_path}/{copied_dir_name}/{file_name}"
    )

    file_handler._copy_file(full_file_path, full_copy_file_path)

    assert os.path.exists(full_copy_file_path)

    remove_directory(dirname)
    remove_directory(copied_dir_name)


def test_copy_file_raises_a_copy_error_if_the_file_copy_process_goes_wrong(monkeypatch):
    dirname = "somedir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    monkeypatch.setattr("shutil.copy", None, raising=True)

    full_file_path = (
        os.path.dirname(__file__) + f"/{temp_dir_path}/{dirname}/{file_name}"
    )
    full_copy_file_path = (
        os.path.dirname(__file__) + f"/{temp_dir_path}/otherdir/{file_name}"
    )
    with pytest.raises(CopyError) as error:
        file_handler._copy_file(full_file_path, full_copy_file_path)

    assert str(error.value) == messages.failed_to_copy("file")

    remove_directory(dirname)


def test_copy_directory_copies_a_whole_directory_with_its_contents():
    dirname = "somedir"
    copied_dir_name = "copieddir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    full_dir_path = os.path.dirname(__file__) + f"/{temp_dir_path}/{dirname}"
    full_copy_dir_path = (
        os.path.dirname(__file__) + f"/{temp_dir_path}/{copied_dir_name}"
    )

    file_handler._copy_directory(full_dir_path, full_copy_dir_path)

    assert os.path.exists(full_copy_dir_path)
    assert os.path.exists(f"{full_copy_dir_path}/{file_name}")

    remove_directory(dirname)
    remove_directory(copied_dir_name)


def test_copy_raises_a_copy_error_if_the_directory_copy_process_goes_wrong(monkeypatch):
    dirname = "somedir"
    copied_dir_name = "copieddir"
    file_name = "somefile.txt"

    new_dir_path = create_directory(dirname)
    create_file(new_dir_path, file_name)

    monkeypatch.setattr("shutil.copytree", None, raising=True)

    full_dir_path = os.path.dirname(__file__) + f"/{temp_dir_path}/{dirname}"
    full_copy_dir_path = (
        os.path.dirname(__file__) + f"/{temp_dir_path}/{copied_dir_name}"
    )

    with pytest.raises(CopyError) as error:
        file_handler._copy_directory(full_dir_path, full_copy_dir_path)

    assert str(error.value) == messages.failed_to_copy("directory")

    remove_directory(dirname)
