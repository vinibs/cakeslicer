# Setting up rules

Rules can be set in some ways so you are able to define what cakeslicer needs to do when some property has some value.

Currently, a rule, which is defined by a variable and may have an action associated with its value, can be of 5 different types, which are defined for the `RuleTypes` enum, accessible from the `core` module:

- `string`
- `integer`
- `float`
- `bool`
- `choice`

They can be defined inside a general rules `dict` that is passed in so they can be processed.

## Rule format

A rule is set based on a dict key from the rules `dict` you set. Each rule is also a `dict` and can accept a few properties:

- `type` (required): The type of the rule. It must be a [`RuleTypes` value](#rules-types).
- `message` (optional): By default, when prompting the user for the rule's value the rule name is used (its key on the main dict). If this `message` attribute is set, it'll replace the rule name when prompting the user. On `choice` rules, though, it'll only replace the reference to the rule, not all the message.
- `actions` (optional): Defines what need to be done based on the rule's value. More details about the actions can be found [here](#actions). A rule without any action can be used in [a conditional (TODO)](#) while copying files to the new project.
- `options` (required only for a `choice` rule): When setting a `choice` rule, you need to specify between what the user needs to choose. This attribute must be a list containing the values that will be shown to the user so it can choose one to be the rule's value.

## Rules dict example

```python
{
    "node_project": {
        "message": "Use node project?",
        "type": RuleTypes.bool,
        "actions": (Actions.include, "./somenodeproject"),
    },
    "license": {
        "type": RuleTypes.choice,
        "options": ["MIT", "CC", "Apache"],
    },
}
```

## Rules types

### `RuleTypes.string`

This type means that the rule's variable can receive any string as a value. It's the mos simple type.

#### Declaration example

```python
"project_name": {
    "type": RuleTypes.string,
},
```

### `RuleTypes.integer`

This type means that the rule's variable can receive any integer as a value. If a value that cannot be converted to an integer is passed when the user is prompted, it'll raise an error.

#### Declaration example

```python
"subprojects_count": {
    "type": RuleTypes.integer,
},
```

### `RuleTypes.float`

Almost the same as for the `integer` type, except that this type expects a **float number**, like an integer or a decimal number.

#### Declaration example

```python
"pi_value": {
    "type": RuleTypes.float,
},
```

### `RuleTypes.bool`

This type means that the rule's variable can receive a boolean value. When prompted, the user may enter one of the following values:

- `Yes` (case insensitive)
- `No` (case insensitive)
- `Y` (case insensitive)
- `N` (case insensitive)
- `True` (case insensitive)
- `False` (case insensitive)
- `T` (case insensitive)
- `F` (case insensitive)
- `1`
- `0`

After being parsed, a boolean rule will always have a python's default `True` or `False` boolean value.

A `bool` rule will have its prompt automatically changed, adding `(y/n)` at the end of the prompt text to guide the user about the available answers, even though it can accept more valid responses than just `y` and `n`. You can see an example as follows:

> For a given `bool` rule with a `message` property declared with the following code:
>
> ```python
>  "node_project": {
>       "message": "Use node project?",
>       "type": RuleTypes.bool,
>       "actions": (Actions.include, "./somenodeproject"),
>   },
> ```
>
> Then the resulting output when prompting the user will be:
>
> ```
> - Use node project? (y/n):
> ```

#### Declaration example

```python
"node_project": {
    "message": "Use node project?",
    "type": RuleTypes.bool,
},
```

### `RuleTypes.choice`

This type means that the rule's variable can receive a choice of a set of options. This requires the rule to have a `options` attribute (that must be a list) so they can be displayed to the user.

A `choice` rule, when prompting the user, format the text so it has a number (sequential, starting from 1) and the value set on the options list. Take this options list a an example:

```python
"options": ["MIT", "CC", "Apache"]
```

This will generate the following prompt for the user, considering they are set to a rule called `license`:

```
- Choose an option for license:
    1 - MIT
    2 - CC
    3 - Apache
  Type your choice's number or value:
```

As you can see by the text, the prompt lets the user ask using both the option's text (case insensitive) or its correlated number (in this case, from 1 to 3).

The final value of a `choice` type will be the index of the selected options in the `options` list. So, for example, if the user selects, in this prompt above, the `Apache` option, the resulting value for this rule will be `2` - its index on the original list.

#### Declaration example

```python
"license": {
    "type": RuleTypes.choice,
    "options": ["MIT", "CC", "Apache"],
},
```

## Actions

A rule can also have one or more actions associated with it. This means that, depending on the value of this rule, one or more action can de executed.

### Action format

An action is defined by a tuple, started by a reference of what needs to be done, based on the `Actions` enum (available from the `core` module), followed by its params.

#### Available actions

Currently, there are two kinds of actions that can be set:

- `Actions.include`
- `Actions.cmd`

The first of them, `include`, means that it will consider all the following items on the tuple as relative paths and will try to add them to the new project. This is the action that make it possible to add a subfolder if the user asks that wants some specific resource.

Se second one, `cmd`, means that it will try to run the following items on the tuple as bash commands. This can be useful, for example, to run git commands.

All the commands (`cmd`) will be executed after processing the `include` rules, at this moment.

### Setting up actions

Once that a single action must be a tuple, there are also a few ways to set actions - the `actions` attribute of the rule:

- **A single tuple for a boolean value** will run the specified action if the rule's value is `True` and won't do anything otherwise. This format of a single tuple **is only valid for boolean values**.
  ```python
  "actions": (Actions.cmd, "git init")
  ```
- **A list of tuples for a boolean value** will behave mostly like the single tuple, except that, using this option, it'l be able to run multiple actions (for example, some `include`s and some `cmd`s) if the boolean rule's value is set to `True`. Again, **it only works this way for boolean rules**.
  ```python
  "actions": [
      (Actions.include, "./somenodeproject"),
      (Actions.cmd, "cp /home"),
  ]
  ```
- **A dictionary relationing the possible rule's values with their desired actions** is the base and default way of setting rule's actions, since it works for any type of rule. This way, you can set each possible value that needs to trigger an action and associate it with an action tuple or a list of action tuples.
  ```python
  "actions": {
        "3.1415": (Actions.cmd, "echo 'Short Pi!'"),
        "3.141592653589793": (Actions.include, echo "'Long Pi!'"),
    }
  ```
