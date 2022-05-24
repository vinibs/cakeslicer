from ...src.core.interfaces import Interaction
from ...src.core.enums import RuleTypes, Actions, BooleanStrValues
from ...src.core.errors import SetupErrorMessages as messages


def setup_properties(
    properties: dict,
    interaction: Interaction,
    *args,
    rules: dict = {},
    comment_delimiters: list = [],
    tool_prefix: str = "",
    attributes: dict = {},
) -> dict:
    attr_variables = _get_attributes(interaction, attributes)
    rules_variables, actions_to_perform = _parse_rules(interaction, rules)

    properties["COMMENT_DELIMITERS"] = comment_delimiters
    properties["TOOL_PREFIX"] = tool_prefix
    properties["VARIABLES"] = {**attr_variables, **rules_variables}
    properties["ACTIONS"] = actions_to_perform

    return properties


def _get_attributes(interaction: Interaction, default_attributes: dict) -> dict:
    attributes = {}

    interaction.show("ATTRIBUTES:")

    for (attr, default_value) in default_attributes.items():
        attr_value = interaction.ask_for(attr, default_value) or default_value
        attributes[attr] = attr_value

    return attributes


def _parse_rules(interaction: Interaction, rules: dict) -> dict:
    rules_vars = {}
    actions_to_perform = {Actions.include: [], Actions.cmd: []}

    interaction.show("\nPROJECT SETTINGS:")

    for (var_name, properties) in rules.items():
        if not "type" in properties:
            raise Exception(messages.required_key_not_present_on_rule("type", var_name))

        elif not isinstance(properties["type"], RuleTypes):
            raise ValueError(messages.type_of_rule_must_be_rule_types(var_name))

        type = properties["type"]
        options = properties["options"] if "options" in properties else None

        rule_value = _process_rule_value(
            interaction.ask_for(
                var_name,
                None,
                type,
                options,
                properties["message"] if "message" in properties else None,
            ),
            type,
            options,
        )

        rules_vars[var_name] = rule_value

        if "actions" in properties:
            actions_to_perform = _process_actions(
                actions_to_perform, properties["actions"], type, rule_value
            )

    return (rules_vars, actions_to_perform)


def _process_rule_value(rule_value: str, type: RuleTypes, options: list = None) -> any:
    if type == RuleTypes.bool:
        rule_value = True if rule_value in BooleanStrValues["positive"] else False

    elif type == RuleTypes.choice:
        lowercase_options = [option.lower() for option in options]

        rule_value = (
            int(rule_value) - 1
            if rule_value.isnumeric()
            else lowercase_options.index(rule_value)
        )

    return rule_value


def _process_actions(
    actions_to_perform: dict,
    property_actions: any,
    rule_type: RuleTypes,
    rule_value: any,
) -> dict:
    error = ValueError(messages.invalid_type_for_action_definition)

    if isinstance(property_actions, dict):
        for value, action in property_actions.items():
            if not (isinstance(action, tuple) or isinstance(action, list)):
                raise error

            if value == rule_value:
                if isinstance(action, list):
                    actions = action
                    for action in actions:
                        if not isinstance(action, tuple):
                            raise error

                        actions_to_perform = _handle_action(actions_to_perform, action)
                else:
                    actions_to_perform = _handle_action(actions_to_perform, action)

    elif isinstance(property_actions, tuple):
        if rule_type == RuleTypes.bool and rule_value == True:
            action = property_actions

            actions_to_perform = _handle_action(actions_to_perform, action)

    elif isinstance(property_actions, list):
        if rule_type == RuleTypes.bool and rule_value == True:
            for action in property_actions:
                if not isinstance(action, tuple):
                    raise error

                actions_to_perform = _handle_action(actions_to_perform, action)

    else:
        raise error

    return actions_to_perform


def _handle_action(actions_to_perform: dict, action: tuple):
    if not isinstance(action[0], Actions):
        raise ValueError(messages.first_tuple_value_must_be_an_action)

    for index, item in enumerate(action):
        if index == 0:
            continue

        actions_to_perform[action[0]].append(item)

    return actions_to_perform
