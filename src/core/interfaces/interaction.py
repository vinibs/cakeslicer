from abc import ABC, abstractmethod
from ..enums import RuleTypes


from abc import ABC


class Interaction(ABC):
    @abstractmethod
    def ask_for(
        self,
        attribute: str,
        default_value: any,
        type: RuleTypes = RuleTypes.string,
        options: list = None,
        message: str = None,
    ) -> any:
        raise NotImplemented

    @abstractmethod
    def _validate_input(self, value: str, type: RuleTypes) -> str:
        raise NotImplemented

    @abstractmethod
    def show(self, *args) -> None:
        raise NotImplemented
