class AttributeDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(name)


class CliErrorMessages(AttributeDict):
    inappropriate_value_for_type = lambda type: f'Inappropriate value for "{type}" type'
    default_value_not_present_among_the_options = (
        lambda default_value: f'Default value "{default_value}" not present among the options'
    )
    no_available_options = "No available options to ask for"
    no_value_for_attribute = lambda attribute: f'No value for attribute "{attribute}"'


class SetupErrorMessages(AttributeDict):
    first_tuple_value_must_be_an_action = (
        "The first value of an action's tuple must be of Actions type"
    )
    type_of_rule_must_be_rule_types = (
        lambda rule_name: f'Type of rule "{rule_name}" must be of type RuleTypes'
    )
    required_key_not_present_on_rule = (
        lambda key, rule_name: f'Required key "{key}" not present on rule "{rule_name}"'
    )
    invalid_type_for_action_definition = "Invalid type for action definition. Each action definition should be a tuple, that may be inside a list or a dict"
