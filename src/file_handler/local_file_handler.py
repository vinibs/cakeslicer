import re
import os
import inspect
import shutil
from typing import List
from ..core.interfaces import FileHandler
from ..core.errors import (
    LocalFileHandlerErrorMessages as messages,
    ValueError,
    FileReadingError,
    CopyError,
)


class LocalFileHandler(FileHandler):
    def is_path(self, path: str) -> bool:
        if not isinstance(path, str):
            return False

        try:
            full_path = self._get_full_path(path)

            return os.path.exists(full_path)

        except Exception:
            return False

    def read_file(self, file_path: str) -> str:
        self._validate_existing_path(file_path)

        try:
            file_path = self._get_full_path(file_path)

            with open(file_path, "r") as file:
                file_contents = file.read()

                return file_contents
        except Exception:
            raise FileReadingError(messages.couldnt_read_file)

    def search(self, subject: str, file_path: str) -> List[str]:
        if not isinstance(subject, str):
            raise ValueError(messages.invalid_type_for_parameter("subject"))

        if subject == "":
            return []

        self._validate_existing_path(file_path)

        file_content = self.read_file(file_path)

        matches = re.finditer(subject, file_content, re.MULTILINE)
        search_results = [match.group() for match in matches]

        return search_results

    def replace_content(
        self, search_subject: str, replacement: str, file_path: str
    ) -> str:
        if not isinstance(replacement, str):
            raise ValueError(messages.invalid_type_for_parameter("replacement"))

        if not len(self.search(search_subject, file_path)):
            return None

        file_contents = self.read_file(file_path)
        full_path = self._get_full_path(file_path)

        print(file_path, full_path)
        try:
            with open(full_path, "w") as file:
                new_content = re.sub(search_subject, replacement, file_contents)

                file.write(new_content)

            return new_content
        except Exception:
            raise FileReadingError(messages.couldnt_write_file)

    def copy(self, original_path: str, destination_path: str) -> None:
        self._validate_existing_path(original_path)
        self._validate_path_format(destination_path)

        full_original_path = self._get_full_path(original_path)
        full_destination_path = self._get_full_path(destination_path)

        if os.path.isfile(full_original_path):
            self._copy_file(full_original_path, full_destination_path)

        else:
            self._copy_directory(full_original_path, full_destination_path)

    def createDirectory(self, directory_path: str) -> None:
        # TODO
        raise NotImplemented

    def _validate_existing_path(self, path: str) -> None:
        if not self.is_path(path):
            raise ValueError(messages.invalid_path)

    def _validate_path_format(self, path: str) -> None:
        pattern = r"^(\/|\.\/|(\.\.\/)+|[A-z]\:\/)?([A-z0-9_\-\(\)\[\]\.]+\/)*[A-z0-9_\-\(\)\[\]\.]+(\.[A-z0-9]+)?\/?$"

        if not re.match(pattern, path):
            raise ValueError(messages.invalid_path)

    def _get_caller_base_dir(self) -> str:
        current_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_path)

        stack = inspect.stack()

        for item in stack:
            caller = item
            abs_path = os.path.abspath(caller.filename)
            dirname = os.path.dirname(abs_path)

            if dirname != current_dir:
                return dirname

    def _get_full_path(self, path: str) -> str:
        path_separator = os.path.sep
        base_path = self._get_caller_base_dir() + path_separator

        same_dir = "." + path_separator
        dir_up = ".." + path_separator

        if path[0:2] == same_dir:
            path = path[2:]

        elif path[0:3] == dir_up:
            base_path_parts = base_path.split(path_separator)

            if base_path_parts[-1] == "":
                base_path_parts.pop(-1)

            dir_up_count = 1
            start_index = 3
            step_size = 3
            for i in range(start_index, len(path), step_size):
                if path[i : i + step_size] == dir_up:
                    dir_up_count += 1
                else:
                    break

            base_path_parts = base_path_parts[0:-dir_up_count]
            base_path = path_separator.join(base_path_parts) + path_separator
            path = path[dir_up_count * step_size :]

        return os.path.join(base_path, path)

    def _copy_file(self, full_original_path: str, full_destination_path: str) -> None:
        try:
            destination_dir_path = full_destination_path

            if re.match(
                r"[A-z0-9_\-\(\)\[\]\.\/]*\.[A-z0-9]+\/?", full_destination_path
            ):
                last_slash = full_destination_path[:-1].rfind(os.path.sep)
                destination_dir_path = full_destination_path[:last_slash]

            if not os.path.isdir(destination_dir_path):
                os.makedirs(destination_dir_path)

            shutil.copy(full_original_path, full_destination_path)
        except Exception:
            raise CopyError(messages.failed_to_copy("file"))

    def _copy_directory(
        self, full_original_path: str, full_destination_path: str
    ) -> None:
        try:
            shutil.copytree(full_original_path, full_destination_path)
        except Exception as error:
            print(error)
            raise CopyError(messages.failed_to_copy("directory"))
