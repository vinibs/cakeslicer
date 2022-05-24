# The bootstrap file

The file that starts the execution is the one where the desired attributes and rules are set and calls the `cakeslicer.run()` method, passing to it the custom values.

An example of this file can be found on the root directory of this repository under the name `cakeslicer.example.py`.

## What does it do?

Basically, this is the file that lives outside the cakeslicer folder, on your starter project. This file is responsible to be of easy access to you so you can set your rules to manage your starter's project creation and execute it from its root (not from this respository's root).

By default, it's called `cakeslicer.py` to be easy to understand who this file is. It's thought to be one level above this repository's code, so it directly imports `cakeslicer` at the top of it, which means it's importing this repository's root.

## What can I set in this file?

There are currently 4 different properties that can be set or overriden by this files contents:

- [`ATTRIBUTES`](#attributes)
- [`RULES`](#rules)
- [`TOOL_PREFIX`](#tool-prefix)
- [`COMMENT_DELIMITERS`](#comment-delimiters)

### Attributes

These are the attributes of the project that will be replaced within the copied directories, like `project_slug`, `version` etc.

These are always strings and can be overriden by the user when running this tool, since it'll be prompted for setting it up.

When an attribute is set, it is defined with a name and a default value. Based on this, when the user is prompted for this attribute's value, the default is also shown and is used if it's left empty.

### Rules

[Rules](./setting-up-rules.md) are the definitions of what need to be stored in memory and what need to be done by the tool based on these stored values.

The rules are used to define which directories need to be included or what command needs to run after creating the new project from the template ones.

### Tool prefix

By default set to `cakeslicer`, the `TOOL_PREFIX` property defines the start point for searching [what needs to be replaced (TODO)](#) among the template project's files.

This way the tool will know that a file that contains, for example, the string `cakeslicer_project_slug` needs to be replaced with the value of the `project_slug` attribute.

### Comment delimiters

Thinking of how to define [conditionals (TODO)](#) without breaking the template code, they can be defined inside comments. To do so, the `COMMENT_DELIMITERS` property can be set overriding the list of comment markers so the tool can identify them correctly. Initially set as `["//", "#"]`.

> **Note:** both `TOOL_PREFIX` and `COMMENT_DELIMITERS` default values are set under the `settings.py` file and can be set there instead of in the `cakeslicer.py` file.
>
> Although the `ATTRIBUTES` is also present on the settings file as an empty list, it's not recommended to set it there, but keep it together the `RULES` definitions in the bootstrap file (`cakeslicer.py`).

## How to set properties?

To set properties in the bootstrap file you just need to set them as variables and pass them accordingly to the `cakeslicer.run()` method.

Take the following as an example:

```python
# Don't forget to import what you'll need.
from cakeslicer import cakeslicer, RuleTypes, Actions


# Set what you want to set as variables...
ATTRS = {"project_slug": "MyBeautyProject"}
rules = {
     "license": {
        "type": RuleTypes.choice,
        "options": ["MIT", "CC", "Apache"],
    },
}

my_own_prefix = "beautyProjectPrefix"
i_only_want_python_comment_delimiters = ["#"]

# ... and pass them to the runner as keyword arguments!
cakeslicer.run(attributes=ATTRS, rules=rules, tool_prefix=my_own_prefix, comment_delimiters=i_only_want_python_comment_delimiters)
```
