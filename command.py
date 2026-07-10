from typing import Any, Self
from collections.abc import Callable

type CommandValueType = bool|int|float|range|str
type CommandTemplate = list[
    type|
    CommandValueType|
    set[CommandValueType]|
    list[CommandValueType]
]

type Callback = Callable[..., None]
type Predicate = Callable[[], bool]

def always_true() -> bool:
    return True

class Command:
    def __init__(self, name: str, aliases: set[str]):
        assert " " not in name
        assert "%" not in name
        self._name = name
        self._aliases = aliases.copy()
        self._aliases.add(name)
        self._callback: Callback|None = None
        self._templates: list[CommandTemplate] = [] # parameter type info for validation and completion
        self._use_templates = False
        self._predicate: Predicate = always_true

    @property
    def name(self) -> str:
        return self._name

    @property
    def helptext_translation_key(self) -> str:
        return f"command.helptext.{self.name}"

    @property
    def helptext(self) -> str:
        import globals
        aliases = list(self._aliases)
        aliases.sort(reverse=True)
        name_index = aliases.index(self._name)
        aliases[name_index], aliases[0] = aliases[0], aliases[name_index]
        helptext: str = " | ".join(aliases) + "\n"
        helptext += globals.translator.translate(self.helptext_translation_key)
        return helptext

    def add_template(self, types: CommandTemplate) -> None:
        template: CommandTemplate = []
        self._templates.append(template)
        for arg_type in types:
            if isinstance(arg_type, type):
                template.append(arg_type)
            else:
                arg_type_type = type(arg_type)
                match arg_type_type:
                    case bool():
                        template.append(arg_type)
                    case int():
                        template.append(arg_type)
                    case float():
                        template.append(arg_type)
                    case str():
                        template.append(arg_type)
                    case set(): # set of choices
                        template.append(arg_type.copy())
                    case list(): # variadic arguments (type cycle)
                        temp = []
                        for cyclic_arg_type in arg_type:
                            match type(cyclic_arg_type):
                                case set():
                                    temp.append(cyclic_arg_type.copy())
                                case list():
                                    raise Exception("Variadic arguments are not allowed in variadic arguments!")
                                case _:
                                    temp.append(cyclic_arg_type)
                        template.append(temp)
                        return # don't allow arguments after this
                    case range():
                        template.append(arg_type)

    def complete(self, text: str) -> list[str]:
        # TODO: Implement command completion
        return []

    def alias(self, alias: str) -> Self:
        self._aliases.add(alias)
        return self

    def bind(self, callback: Callback) -> Self:
        self._callback = callback
        return self

    def available_when(self, predicate: Any) -> Self:
        self._predicate = predicate
        return self

    def available(self) -> bool:
        available: bool = self._predicate()
        return available

    def matches(self, command: str) -> bool:
        if not command:
            return False
        args = command.split()
        return args[0] in self._aliases

    # NOT IMPLEMENTED + EXPERIMENTAL
    def use_templates(self) -> None:
        self._use_templates = True

    def parse(self, command: str) -> list[CommandValueType]:
        args: list[CommandValueType] = []
        mode: int = 0
        for char in command:
            match mode:
                case 0:
                    if char == " ":
                        pass
                    elif char == "-":
                        args.append(char)
                        mode = 5
                    elif char in ".0123456789":
                        args.append(char)
                        mode = 1
                    elif char == '"':
                        args.append("")
                        mode = 3
                    else:
                        args.append(char)
                        mode = 2
                case 1:
                    assert isinstance(args[-1], str)
                    if char == " ":
                        mode = 0
                        try:
                            number: str = args[-1]
                            if "." in number:
                                args[-1] = float(number)
                            else:
                                args[-1] = int(number)
                        except:
                            pass
                    else:
                        args[-1] += char
                case 2:
                    assert isinstance(args[-1], str)
                    if char == " ":
                        mode = 0
                    else:
                        args[-1] += char
                case 3:
                    assert isinstance(args[-1], str)
                    if char == "\\":
                        mode = 4
                    elif char == '"':
                        mode = 0
                    else:
                        args[-1] += char
                case 4:
                    assert isinstance(args[-1], str)
                    args[-1] += char
                    mode = 3
                case 5:
                    args.append(char)
                    if char in ".0123456789":
                        mode = 1
                    else:
                        mode = 2
        if self._use_templates:
            raise NotImplementedError()
        return args

    def run(self, command: str) -> None:
        # This does not check for match (intentional)
        args = self.parse(command)
        if self._callback:
            self._callback(self, args)
