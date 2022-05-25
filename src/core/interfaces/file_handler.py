from abc import ABC, abstractmethod


class FileHandler(ABC):
    @abstractmethod
    def is_path(self, path: str):
        raise NotImplemented

    @abstractmethod
    def read_file(self, file_path: str):
        raise NotImplemented

    @abstractmethod
    def search(self, subject: str, file_path: str):
        raise NotImplemented

    @abstractmethod
    def replace_content(self, search_subject: str, new_content: str, file_path: str):
        raise NotImplemented

    @abstractmethod
    def copy(self, original_path: str, destination_path: str):
        raise NotImplemented
