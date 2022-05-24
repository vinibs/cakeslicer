from cakeslicer.src.core.enums import RuleTypes
from cakeslicer.src.core.errors import CliErrorMessages as messages
from cakeslicer.src.interaction import cli
import pytest


positive_bool_strings = [
    "Yes",
    "yes",
    "YES",
    "y",
    "Y",
    "True",
    "true",
    "TRUE",
    "t",
    "T",
    "1",
]
negative_bool_strings = [
    "No",
    "no",
    "NO",
    "n",
    "N",
    "False",
    "false",
    "FALSE",
    "f",
    "F",
    "0",
]


def test_show_one_parameter_successfully(capsys):
    first_param = "somevalue"

    cli.show(first_param)
    out, _ = capsys.readouterr()

    assert out == f"{first_param}\n"


def test_show_many_parameters_with_a_space_between_them_successfully(capsys):
    first_param = "somevalue"
    second_param = "anothervalue"
    third_param = {"a_third": "value"}
    fourth_param = ["one", "more", "value"]

    cli.show(first_param, second_param, third_param, fourth_param)
    out, _ = capsys.readouterr()

    assert out == (
        f"{first_param} {second_param} {str(third_param)} {str(fourth_param)}\n"
    )


def test_ask_for_fails_without_default_value_and_no_input(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda _: "")

    attribute = "project_slug"

    with pytest.raises(ValueError) as error:
        answer = cli.ask_for(attribute, None)

    assert str(error.value) == messages.no_value_for_attribute(attribute)


def test_ask_for_successfully_with_passing_type_and_with_default_value_and_no_input(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda _: "")

    attribute = "project_slug"
    default = "SLUG"

    answer = cli.ask_for(attribute, default)

    assert answer == default


def test_ask_for_successfully_without_passing_type_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "another_slug"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "project_slug"
    default = "SLUG"

    answer = cli.ask_for(attribute, default)

    assert answer == typed_answer


def test_ask_for_successfully_without_passing_type_and_without_default_value_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "another_slug"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "project_slug"

    answer = cli.ask_for(attribute, None)

    assert answer == typed_answer


def test_ask_for_successfully_with_string_type_with_default_value_and_no_input(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda _: "")

    attribute = "project_slug"
    default = "SLUG"

    answer = cli.ask_for(attribute, default, RuleTypes.string)

    assert answer == default


def test_ask_for_successfully_with_string_type_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "another_slug"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "project_slug"
    default = "SLUG"

    answer = cli.ask_for(attribute, default, RuleTypes.string)

    assert answer == typed_answer


def test_ask_for_successfully_with_string_type_and_without_default_value_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "another_slug"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "project_slug"

    answer = cli.ask_for(attribute, None, RuleTypes.string)

    assert answer == typed_answer


def test_ask_for_successfully_with_int_type_with_default_value_and_no_input(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda _: "")

    attribute = "someattr"
    default = "3"

    answer = cli.ask_for(attribute, default, RuleTypes.integer)

    assert answer == default


def test_ask_for_successfully_with_int_type_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "42"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "someattr"
    default = "3"

    answer = cli.ask_for(attribute, default, RuleTypes.integer)

    assert answer == typed_answer


def test_ask_for_successfully_with_int_type_and_without_default_value_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "42"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "someattr"

    answer = cli.ask_for(attribute, None, RuleTypes.integer)

    assert answer == typed_answer


def test_ask_for_fails_with_int_type_and_with_invalid_inputted_value(
    monkeypatch,
):
    typed_answer = "notanint"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "someattr"

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, None, RuleTypes.integer)

    assert str(error.value) == messages.inappropriate_value_for_type("integer")


def test_ask_for_successfully_with_float_type_with_default_value_and_no_input(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda _: "")

    attribute = "someattr"
    default = "1.2"

    answer = cli.ask_for(attribute, default, RuleTypes.float)

    assert answer == default


def test_ask_for_successfully_with_float_type_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "3.141592653689793"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "someattr"
    default = "1.2"

    answer = cli.ask_for(attribute, default, RuleTypes.float)

    assert answer == typed_answer


def test_ask_for_successfully_with_float_type_and_without_default_value_and_with_inputted_value(
    monkeypatch,
):
    typed_answer = "3.141592653689793"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "someattr"

    answer = cli.ask_for(attribute, None, RuleTypes.float)

    assert answer == typed_answer


def test_ask_for_fails_with_float_type_and_with_invalid_inputted_value(
    monkeypatch,
):
    typed_answer = "notafloat"
    monkeypatch.setattr("builtins.input", lambda _: typed_answer)

    attribute = "someattr"

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, None, RuleTypes.float)

    assert str(error.value) == messages.inappropriate_value_for_type("float")


@pytest.mark.parametrize(
    "boolean_str",
    [*positive_bool_strings, *negative_bool_strings],
)
def test_ask_for_successfully_with_boolean_type_without_default_value_and_with_inputted_value(
    boolean_str,
    monkeypatch,
):
    attribute = "use_python"

    boolean_answer = boolean_str
    monkeypatch.setattr("builtins.input", lambda _: boolean_answer)

    answer = cli.ask_for(attribute, None, RuleTypes.bool)

    assert answer == boolean_answer


def test_ask_for_successfully_with_boolean_type_with_default_value_and_no_input(
    monkeypatch,
):
    attribute = "use_python"

    boolean_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: boolean_answer)

    default = "true"
    answer = cli.ask_for(attribute, default, RuleTypes.bool)

    assert answer == default


@pytest.mark.parametrize(
    "invalid_bool_str",
    [
        "yess",
        "ye",
        "yeah",
        "nno",
        "not",
        "dont",
        "tru",
        "fals",
        "somethingdifferent",
    ],
)
def test_ask_for_fails_with_boolean_type_and_invalid_inputted_value(
    invalid_bool_str,
    monkeypatch,
):
    attribute = "use_python"

    invalid_answer = invalid_bool_str
    monkeypatch.setattr("builtins.input", lambda _: invalid_answer)

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, None, RuleTypes.bool)

    assert str(error.value) == messages.inappropriate_value_for_type("bool")


@pytest.mark.parametrize(
    "choice_option",
    [
        "mit",
        "MIT",
        "Mit",
        "1",
        "cc",
        "CC",
        "Cc",
        "2",
        "apache",
        "APACHE",
        "apachE",
        "3",
    ],
)
def test_ask_for_successfully_with_choice_type_without_default_value_and_with_inputted_value(
    choice_option,
    monkeypatch,
):
    attribute = "license"

    option_answer = choice_option
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    answer = cli.ask_for(attribute, None, RuleTypes.choice, ["MIT", "CC", "Apache"])

    assert answer == option_answer


@pytest.mark.parametrize(
    "choice_option",
    [
        "mit",
        "MIT",
        "Mit",
        "1",
    ],
)
def test_ask_for_successfully_with_choice_with_inputted_value_being_name_case_insensitive_or_list_index_starting_from_1(
    choice_option,
    monkeypatch,
):
    attribute = "license"

    option_answer = choice_option
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    answer = cli.ask_for(attribute, None, RuleTypes.choice, ["MIT", "CC", "Apache"])

    assert answer == option_answer


def test_ask_for_successfully_with_choice_type_with_default_value_matching_option_case_and_no_input(
    monkeypatch,
):
    attribute = "license"

    option_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    default = "MIT"
    answer = cli.ask_for(attribute, default, RuleTypes.choice, ["MIT", "CC", "Apache"])

    assert answer == default


def test_ask_for_successfully_with_choice_type_with_default_option_containing_spaces(
    monkeypatch,
):
    attribute = "license"

    option_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    default = "Another license"
    answer = cli.ask_for(
        attribute, default, RuleTypes.choice, ["MIT", "CC", "Apache", "Another license"]
    )

    assert answer == default


def test_ask_for_successfully_with_choice_type_with_option_containing_spaces_selected_by_its_text(
    monkeypatch,
):
    attribute = "license"

    option_answer = "Another license"
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    answer = cli.ask_for(
        attribute, None, RuleTypes.choice, ["MIT", "CC", "Apache", "Another license"]
    )

    assert answer == option_answer


def test_ask_for_successfully_with_choice_type_with_default_option_containing_special_chars(
    monkeypatch,
):
    attribute = "license"

    option_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    default = "Sp&c1al Ch@ar 0pt!ion"
    answer = cli.ask_for(
        attribute,
        default,
        RuleTypes.choice,
        ["MIT", "CC", "Apache", "Sp&c1al Ch@ar 0pt!ion"],
    )

    assert answer == default


def test_ask_for_successfully_with_choice_type_with_option_containing_spaces_selected_by_its_text(
    monkeypatch,
):
    attribute = "license"

    option_answer = "Sp&c1al Ch@ar 0pt!ion"
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    answer = cli.ask_for(
        attribute,
        None,
        RuleTypes.choice,
        ["MIT", "CC", "Apache", "Sp&c1al Ch@ar 0pt!ion"],
    )

    assert answer == option_answer


def test_ask_for_fails_with_choice_type_with_default_value_not_matching_option_case_and_no_input(
    monkeypatch,
):
    attribute = "license"

    option_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    default = "mit"

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, default, RuleTypes.choice, ["MIT", "CC", "Apache"])

    assert str(error.value) == messages.default_value_not_present_among_the_options(
        default
    )


def test_ask_for_fails_with_choice_type_with_default_value_not_present_among_options_and_no_input(
    monkeypatch,
):
    attribute = "license"

    option_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    default = "copyright"

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, default, RuleTypes.choice, ["MIT", "CC", "Apache"])

    assert str(error.value) == messages.default_value_not_present_among_the_options(
        default
    )


def test_ask_for_fails_with_choice_type_with_empty_set_of_options(
    monkeypatch,
):
    attribute = "license"

    option_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, "1", RuleTypes.choice, [])

    assert str(error.value) == messages.no_available_options


def test_ask_for_fails_with_choice_type_with_options_set_to_none(
    monkeypatch,
):
    attribute = "license"

    option_answer = ""
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, "1", RuleTypes.choice, None)

    assert str(error.value) == messages.no_available_options


def test_ask_for_fails_with_choice_type_with_inputted_value_not_among_the_options(
    monkeypatch,
):
    attribute = "license"

    option_answer = "copyright"
    monkeypatch.setattr("builtins.input", lambda _: option_answer)

    with pytest.raises(ValueError) as error:
        cli.ask_for(attribute, None, RuleTypes.choice, ["MIT", "CC", "Apache"])

    assert str(error.value) == messages.inappropriate_value_for_type("choice")


@pytest.mark.parametrize(
    "attribute_type",
    [RuleTypes.string, RuleTypes.integer, RuleTypes.float],
)
def test_generate_input_message_with_basic_format_for_basic_attributes_without_a_default_value(
    attribute_type,
):
    attribute = "someattribute"
    message = cli._generate_input_message(attribute, None, attribute_type)

    assert message == f"- {attribute}: "


@pytest.mark.parametrize(
    "attribute_type",
    [RuleTypes.string, RuleTypes.integer, RuleTypes.float],
)
def test_generate_input_message_with_the_default_value_for_basic_attributes(
    attribute_type,
):
    attribute = "someattribute"
    default_value_map = {
        RuleTypes.string: "somestringvalue",
        RuleTypes.integer: "3",
        RuleTypes.float: "3.141592653589793",
    }

    default_value = default_value_map[attribute_type]
    message = cli._generate_input_message(attribute, default_value, attribute_type)

    assert message == f"- {attribute} [{default_value}]: "


def test_generate_input_message_with_basic_format_and_possible_answers_indicator_for_boolean_attribute_without_a_default_value():
    attribute = "someattribute"
    message = cli._generate_input_message(attribute, None, RuleTypes.bool)

    assert message == f"- {attribute} (y/n): "


def test_generate_input_message_with_the_default_value_and_possible_answers_indicator_for_boolean_attribute():
    attribute = "someattribute"
    default = "y"
    message = cli._generate_input_message(attribute, default, RuleTypes.bool)

    assert message == f"- {attribute} [{default}] (y/n): "


def test_generate_input_message_with_custom_format_for_choice_attribute_without_a_default_value():
    attribute = "someattribute"
    message = cli._generate_input_message(
        attribute,
        None,
        RuleTypes.choice,
        ["option A", "option B", "option C", "option D"],
    )

    assert message == (
        "- Choose an option for someattribute:\n"
        + "    1 - option A\n"
        + "    2 - option B\n"
        + "    3 - option C\n"
        + "    4 - option D\n"
        + "  Type your choice's number or value: "
    )


def test_generate_input_message_with_custom_format_for_choice_attribute_with_a_default_value():
    attribute = "someattribute"
    default = "option B"
    message = cli._generate_input_message(
        attribute,
        default,
        RuleTypes.choice,
        ["option A", "option B", "option C", "option D"],
    )

    assert message == (
        f"- Choose an option for someattribute [{default}]:\n"
        + "    1 - option A\n"
        + "    2 - option B\n"
        + "    3 - option C\n"
        + "    4 - option D\n"
        + "  Type your choice's number or value: "
    )


def test_generate_input_message_with_passed_custom_message_instead_of_attribute_name_without_a_default_value():
    attribute = "someattribute"
    custom_message = "Use some-attribute?"
    message = cli._generate_input_message(
        attribute, None, RuleTypes.string, custom_message=custom_message
    )

    assert message == f"- {custom_message}: "


def test_generate_input_message_with_passed_custom_message_instead_of_attribute_name_with_a_default_value():
    attribute = "someattribute"
    default = "3.141592653589793"
    custom_message = "Use some-attribute?"
    message = cli._generate_input_message(
        attribute, default, RuleTypes.float, custom_message=custom_message
    )

    assert message == f"- {custom_message} [{default}]: "


def test_validate_choice_params_fails_when_there_is_no_options():
    with pytest.raises(ValueError) as error:
        cli._validate_choice_params("default", None)

    assert str(error.value) == messages.no_available_options


def test_validate_choice_params_fails_when_the_default_value_is_not_among_the_options():
    with pytest.raises(ValueError) as error:
        cli._validate_choice_params("default", ["not the default", "some other option"])

    assert str(error.value) == messages.default_value_not_present_among_the_options(
        "default"
    )


def test_validate_choice_params_doesnt_fail_when_there_are_options_and_no_default_value():
    try:
        cli._validate_choice_params(None, ["not the default", "some other option"])
    except Exception:
        assert False, "An exception was raised."


def test_validate_choice_params_doesnt_fail_when_there_are_options_and_a_default_value_that_match_one_of_the_options():
    try:
        cli._validate_choice_params(
            "some other option", ["not the default", "some other option"]
        )
    except Exception:
        assert False, "An exception was raised."


def test_generate_choice_message_without_a_default_value():
    attribute = "someattribute"
    message = cli._generate_choice_message(
        attribute,
        None,
        ["option A", "option B", "option C", "option D"],
    )

    assert message == (
        "- Choose an option for someattribute:\n"
        + "    1 - option A\n"
        + "    2 - option B\n"
        + "    3 - option C\n"
        + "    4 - option D\n"
        + "  Type your choice's number or value"
    )


def test_generate_choice_message_with_a_default_value():
    attribute = "someattribute"
    default = "option B"
    message = cli._generate_choice_message(
        attribute,
        default,
        ["option A", "option B", "option C", "option D"],
    )

    assert message == (
        f"- Choose an option for someattribute [{default}]:\n"
        + "    1 - option A\n"
        + "    2 - option B\n"
        + "    3 - option C\n"
        + "    4 - option D\n"
        + "  Type your choice's number or value"
    )
