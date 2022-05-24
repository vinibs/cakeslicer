from cakeslicer.src.core.enums import RuleTypes, Actions


mocked_attributes = {"project_slug": "ProjectName", "version": "0.0.1"}
mocked_rules = {
    "python_project": {
        "message": "Use python project?",
        "type": RuleTypes.bool,
        "actions": {
            True: (Actions.include, "./somepyproject"),
            False: [(Actions.cmd, "echo 'fail'"), (Actions.cmd, "echo 'fail again'")],
        },
    },
    "node_project": {
        "message": "Use node project?",
        "type": RuleTypes.bool,
        "actions": [
            (
                Actions.include,
                "./somenodeproject",
            ),
            (Actions.cmd, "cp /home"),
        ],
    },
    "use_cache": {
        "message": "Use cache?",
        "type": RuleTypes.bool,
    },
    "git": {
        "message": "Initialize git?",
        "type": RuleTypes.bool,
        "actions": (
            Actions.cmd,
            "git init",
        ),
    },
    "license": {
        "type": RuleTypes.choice,
        "options": ["MIT", "CC", "Apache"],
    },
}


def mocked_inputs(prompt_text: str) -> str:
    prompt_input_map = {
        "- project_slug [ProjectName]: ": "project_name",
        "- version [0.0.1]: ": "1.0.0",
        "- Use python project? (y/n): ": "y",
        "- Use python project?: ": "y",
        "- Use node project? (y/n): ": "n",
        "- Use cache? (y/n): ": "n",
        "- Initialize git? (y/n): ": "y",
        (
            "- Choose an option for license:\n"
            "    1 - MIT\n"
            "    2 - CC\n"
            "    3 - Apache\n"
            "  Type your choice's number or value: "
        ): "3",
        "- country: ": "brazil",
        "- children_count: ": "3",
        "- pi_value: ": "3.141592653589793",
        "- int_pi_value: ": "3",
    }

    return prompt_input_map[prompt_text]
