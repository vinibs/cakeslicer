from cakeslicer.src.core.enums import Actions, RuleTypes
from cakeslicer.src.main.setup import setup_properties
from cakeslicer.src.interaction import cli
from mocks.base_parameters import mocked_attributes, mocked_rules, mocked_inputs
import pytest


def test_setup_properties_successfully_generates_the_properties_structure(monkeypatch):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    properties = setup_properties(
        {},
        cli,
        rules=mocked_rules,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
    )

    assert properties == {
        "COMMENT_DELIMITERS": comment_delimiters,
        "TOOL_PREFIX": tool_prefix,
        "VARIABLES": {
            "project_slug": "project_name",
            "version": "1.0.0",
            "python_project": True,
            "node_project": False,
            "use_cache": False,
            "git": True,
            "license": 2,
        },
        "ACTIONS": {Actions.include: ["./somepyproject"], Actions.cmd: ["git init"]},
    }


def test_setup_properties_fails_if_an_action_that_is_not_a_tuple_is_passed(monkeypatch):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "node_project": {
            "message": "Use node project?",
            "type": RuleTypes.bool,
            "actions": "./somenodeproject",
        },
    }

    with pytest.raises(ValueError) as error:
        setup_properties(
            {},
            cli,
            attributes=mocked_attributes,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
            rules=rules,
        )

        assert (
            str(error)
            == "Invalid type for action definition. Each action definition should be a tuple, that may be inside a list or a dict"
        )


def test_setup_properties_fails_if_an_action_that_does_not_end_up_being_a_tuple_is_passed(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "node_project": {
            "message": "Use node project?",
            "type": RuleTypes.bool,
            "actions": {True: "__ignored_by_the_mock", False: "./somenodeproject"},
        },
    }

    with pytest.raises(ValueError) as error:
        setup_properties(
            {},
            cli,
            attributes=mocked_attributes,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
            rules=rules,
        )

        assert (
            str(error)
            == "Invalid type for action definition. Each action definition should be a tuple, that may be inside a list or a dict"
        )


def test_setup_properties_fails_if_an_action_that_has_more_than_3_levels_until_it_is_a_tuple_is_passed(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "node_project": {
            "message": "Use node project?",
            "type": RuleTypes.bool,
            "actions": {
                True: "__ignored_by_the_mock",
                False: [[(Actions.include, "./somenodeproject")]],
            },
        },
    }

    with pytest.raises(ValueError) as error:
        setup_properties(
            {},
            cli,
            attributes=mocked_attributes,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
            rules=rules,
        )

        assert (
            str(error)
            == "Invalid type for action definition. Each action definition should be a tuple, that may be inside a list or a dict"
        )


def test_setup_properties_fails_if_an_action_tuple_doesnt_start_with_an_action_type_value(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "node_project": {
            "message": "Use node project?",
            "type": RuleTypes.bool,
            "actions": {False: ("./someothernodeproject", "./somenodeproject")},
        },
    }

    with pytest.raises(ValueError) as error:
        setup_properties(
            {},
            cli,
            attributes=mocked_attributes,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
            rules=rules,
        )

        assert (
            str(error) == "The first value of an action's tuple must be of Actions type"
        )


def test_setup_properties_fails_if_an_action_doesnt_have_the_required_type_key(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "python_project": {
            "message": "Use python project?",
        },
    }

    with pytest.raises(Exception) as error:
        setup_properties(
            {},
            cli,
            attributes=mocked_attributes,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
            rules=rules,
        )

    assert (
        str(error.value) == 'Required key "type" not present on rule "python_project"'
    )


def test_setup_properties_fails_if_an_actions_type_is_not_of_ruletypes_type(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "python_project": {"message": "Use python project?", "type": "another_type"},
    }

    with pytest.raises(ValueError) as error:
        setup_properties(
            {},
            cli,
            attributes=mocked_attributes,
            comment_delimiters=comment_delimiters,
            tool_prefix=tool_prefix,
            rules=rules,
        )

    assert str(error.value) == 'Type of rule "python_project" must be of type RuleTypes'


def test_setup_properties_runs_an_action_defined_in_a_simple_tuple_if_the_rule_is_boolean_and_its_value_is_true(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "python_project": {
            "message": "Use python project?",
            "type": RuleTypes.bool,
            "actions": (Actions.include, "./somepyproject"),
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert properties["ACTIONS"] == {
        Actions.include: ["./somepyproject"],
        Actions.cmd: [],
    }


def test_setup_properties_doesnt_run_an_action_defined_in_a_simple_tuple_if_the_rule_is_not_boolean(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "python_project": {
            "message": "Use python project?",
            "type": RuleTypes.string,
            "actions": (Actions.include, "./somepyproject"),
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert properties["ACTIONS"] == {
        Actions.include: [],
        Actions.cmd: [],
    }


def test_setup_properties_doesnt_run_an_action_defined_in_a_simple_tuple_if_the_rule_is_boolean_and_its_value_is_not_true(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    rules = {
        "node_project": {
            "message": "Use node project?",
            "type": RuleTypes.bool,
            "actions": (Actions.include, "./somenodeproject"),
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert properties["ACTIONS"] == {
        Actions.include: [],
        Actions.cmd: [],
    }


def test_setup_properties_runs_a_string_action_defined_in_a_dict_if_its_key_matches_the_attributes_value(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    brazil_action_str = "echo 'Brazil!'"
    usa_action_str = "echo 'USA!'"

    rules = {
        "country": {
            "type": RuleTypes.string,
            "actions": {
                "brazil": (Actions.cmd, brazil_action_str),
                "usa": (Actions.cmd, usa_action_str),
            },
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert usa_action_str not in properties["ACTIONS"][Actions.cmd]
    assert brazil_action_str in properties["ACTIONS"][Actions.cmd]


def test_setup_properties_runs_an_integer_action_defined_in_a_dict_if_its_key_matches_the_attributes_value(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    children_2_action_str = "echo '2 children!'"
    children_3_action_str = "echo '3 children!'"

    rules = {
        "children_count": {
            "type": RuleTypes.integer,
            "actions": {
                "2": (Actions.include, children_2_action_str),
                "3": (Actions.include, children_3_action_str),
            },
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert children_2_action_str not in properties["ACTIONS"][Actions.include]
    assert children_3_action_str in properties["ACTIONS"][Actions.include]


def test_setup_properties_runs_an_float_action_defined_in_a_dict_if_its_key_matches_the_attributes_value(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    short_pi_action_str = "echo 'Short Pi!'"
    long_pi_action_str = "echo 'Long Pi!'"

    rules = {
        "pi_value": {
            "type": RuleTypes.float,
            "actions": {
                "3.1415": (Actions.cmd, short_pi_action_str),
                "3.141592653589793": (Actions.include, long_pi_action_str),
            },
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert short_pi_action_str not in properties["ACTIONS"][Actions.cmd]
    assert long_pi_action_str in properties["ACTIONS"][Actions.include]


def test_setup_properties_runs_a_boolean_action_defined_in_a_dict_if_its_key_matches_the_attributes_value(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    true_action_str = "./somenodeproject"
    false_action_str = "echo 'dont load node'"

    rules = {
        "node_project": {
            "message": "Use node project?",
            "type": RuleTypes.bool,
            "actions": {
                True: (Actions.include, true_action_str),
                False: (Actions.cmd, false_action_str),
            },
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert true_action_str not in properties["ACTIONS"][Actions.include]
    assert false_action_str in properties["ACTIONS"][Actions.cmd]


def test_setup_properties_runs_a_choice_action_defined_in_a_dict_if_its_key_matches_the_option_index_on_the_list(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    mit_action_str = "MIT action string"
    cc_action_str = "CC action string"
    apache_action_str = "Apache action string"

    rules = {
        "license": {
            "type": RuleTypes.choice,
            "options": ["MIT", "CC", "Apache"],
            "actions": {
                0: (Actions.cmd, mit_action_str),
                1: (Actions.cmd, cc_action_str),
                2: (Actions.cmd, apache_action_str),
            },
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert mit_action_str not in properties["ACTIONS"][Actions.cmd]
    assert cc_action_str not in properties["ACTIONS"][Actions.cmd]
    assert apache_action_str in properties["ACTIONS"][Actions.cmd]


def test_setup_properties_doesnt_run_any_action_defined_in_a_dict_if_the_attributes_value_doesnt_match_any_dict_key(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    germany_action_str = "echo 'Germany!'"
    usa_action_str = "echo 'USA!'"

    rules = {
        "country": {
            "type": RuleTypes.string,
            "actions": {
                "germany": (Actions.cmd, germany_action_str),
                "usa": (Actions.cmd, usa_action_str),
            },
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert usa_action_str not in properties["ACTIONS"][Actions.cmd]
    assert germany_action_str not in properties["ACTIONS"][Actions.cmd]
    assert properties["ACTIONS"][Actions.cmd] == []


def test_setup_properties_runs_all_actions_defined_in_a_list_from_a_dict_when_its_key_matches_the_attributes_value(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    true_action_str = "./somenodeproject"
    first_false_action_str = "echo 'fail'"
    second_false_action_str = "echo 'fail again'"

    rules = {
        "node_project": {
            "message": "Use node project?",
            "type": RuleTypes.bool,
            "actions": {
                True: (Actions.include, true_action_str),
                False: [
                    (Actions.cmd, first_false_action_str),
                    (Actions.cmd, second_false_action_str),
                ],
            },
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert true_action_str not in properties["ACTIONS"][Actions.include]
    assert properties["ACTIONS"][Actions.cmd] == [
        first_false_action_str,
        second_false_action_str,
    ]


def test_setup_properties_runs_all_actions_defined_in_a_list_for_the_true_value_of_a_boolean_rule(
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", mocked_inputs)

    comment_delimiters = ["//", "#"]
    tool_prefix = "cakeslicer"

    first_true_action_str = "./somepyproject"
    second_true_action_str = "echo 'Didnt fail'"
    third_true_action_str = "echo 'Didnt fail again'"

    rules = {
        "python_project": {
            "message": "Use python project?",
            "type": RuleTypes.bool,
            "actions": [
                (Actions.include, first_true_action_str),
                (Actions.cmd, second_true_action_str),
                (Actions.cmd, third_true_action_str),
            ],
        },
    }

    properties = setup_properties(
        {},
        cli,
        attributes=mocked_attributes,
        comment_delimiters=comment_delimiters,
        tool_prefix=tool_prefix,
        rules=rules,
    )

    assert properties["ACTIONS"][Actions.include] == [first_true_action_str]
    assert properties["ACTIONS"][Actions.cmd] == [
        second_true_action_str,
        third_true_action_str,
    ]
