from .setup import setup_properties
from ..interaction import cli
from ...settings import COMMENT_DELIMITERS, TOOL_PREFIX, ATTRIBUTES


class Main:
    _properties = {}

    def run(
        self,
        *args,
        rules: dict,
        attributes: dict = ATTRIBUTES,
        comment_delimiters: list = COMMENT_DELIMITERS,
        tool_prefix: str = TOOL_PREFIX,
    ):
        self._prepare(
            rules=rules,
            attributes=attributes,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
        )

    def _prepare(
        self,
        *args,
        rules: dict,
        attributes: dict,
        comment_delimiters: list,
        tool_prefix: str,
    ):
        self._properties = setup_properties(
            self._properties,
            cli,
            rules=rules,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
            attributes=attributes,
        )

        cli.show(self._properties)
