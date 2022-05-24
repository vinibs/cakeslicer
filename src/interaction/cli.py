from ..core.interfaces import Interaction
from ..core.enums import RuleTypes, BooleanStrValues
from ..core.errors import CliErrorMessages as messages


class Cli(Interaction):
    def ask_for(
        self,
        attribute: str,
        default_value: any,
        type: RuleTypes = RuleTypes.string,
        options: list = None,
        message: str = None,
    ) -> str:
        input_message = self._generate_input_message(
            attribute, default_value, type, options, message
        )

        value = input(input_message)

        if value == "" and not default_value:
            raise ValueError(messages.no_value_for_attribute(attribute))

        return self._validate_input(default_value, value, type, options)

    def _generate_input_message(
        self,
        attribute: str,
        default_value: any,
        type: RuleTypes,
        options: list = None,
        custom_message: str = None,
    ):
        base_message = custom_message if custom_message else attribute

        message = f"- {base_message}{f' [{default_value}]' if default_value else ''}"

        if type == RuleTypes.bool:
            message += " (y/n)"

        elif type == RuleTypes.choice:
            self._validate_choice_params(default_value, options)

            message = self._generate_choice_message(attribute, default_value, options)

        message += ": "

        return message

    def _validate_choice_params(self, default_value: any, options: list):
        if options is None or options == []:
            raise ValueError(messages.no_available_options)

        if default_value is not None and default_value not in options:
            raise ValueError(
                messages.default_value_not_present_among_the_options(default_value)
            )

    def _generate_choice_message(
        self, attribute: str, default_value: any, options: list
    ) -> str:
        message = f"- Choose an option for {attribute}{f' [{default_value}]' if default_value else ''}:"

        for (i, option) in enumerate(options):
            message += f"\n{' '*4}{i+1} - {option}"

        message += "\n  Type your choice's number or value"

        return message

    def _validate_input(
        self, default_value: str, value: str, type: RuleTypes, options: list = None
    ) -> str:
        if value == "":
            value = default_value

        if type == RuleTypes.string:
            return value

        validations = {
            RuleTypes.bool: lambda val: (
                val.lower()
                in [
                    *BooleanStrValues["positive"],
                    *BooleanStrValues["negative"],
                ]
            ),
            RuleTypes.choice: lambda val: (
                val.lower() in [option.lower() for option in options]
                or (int(val) > 0 and int(val) <= len(options))
            ),
            RuleTypes.integer: lambda val: int(val),
            RuleTypes.float: lambda val: float(val),
        }

        try:
            if not validations[type](value):
                raise Exception
        except Exception:
            desired_type = str(type).replace("RuleTypes.", "")
            raise ValueError(
                messages.inappropriate_value_for_type(desired_type)
            ) from None

        return value

    def show(self, *args) -> None:
        print(*args)
