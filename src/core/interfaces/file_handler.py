from abc import ABC, abstractmethod
from typing import List


class FileHandler(ABC):
    @abstractmethod
    def is_path(self, path: str) -> bool:
        raise NotImplemented

    @abstractmethod
    def read_file(self, file_path: str) -> str:
        raise NotImplemented

    @abstractmethod
    def search(self, subject: str, file_path: str) -> List[str]:
        raise NotImplemented

    @abstractmethod
    def replace_content(
        self, search_subject: str, replacement: str, file_path: str
    ) -> str:
        raise NotImplemented

    @abstractmethod
    def copy(self, original_path: str, destination_path: str) -> None:
        raise NotImplemented

    @abstractmethod
    def _validate_existing_path(self, path: str) -> None:
        raise NotImplemented

    @abstractmethod
    def _validate_path_format(self, path: str) -> None:
        raise NotImplemented

    @abstractmethod
    def _copy_file(self, full_original_path: str, full_destination_path: str) -> None:
        raise NotImplemented

    @abstractmethod
    def _copy_directory(
        self, full_original_path: str, full_destination_path: str
    ) -> None:
        raise NotImplemented
