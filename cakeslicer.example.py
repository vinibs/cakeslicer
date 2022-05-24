from cakeslicer import cakeslicer, RuleTypes, Actions

ATTRIBUTES = {"project_slug": "ProjectName", "version": "0.0.1"}
RULES = {
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
        ),  # default for "true" value in a *boolean* rule
    },
    "license": {
        "type": RuleTypes.choice,
        "options": ["MIT", "CC", "Apache"],
    },
}


cakeslicer.run(attributes=ATTRIBUTES, rules=RULES)
