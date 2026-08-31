from pathlib import Path
from typing import Any

TRANSLATION_FILE_SUFFIX: str = ".txt"
DEPENDENCIES_KEY: str = "%%depends"

def _get_translations_path() -> Path:
    import os
    APPDIR: str = os.environ.get("APPDIR", "")
    XDG_CONFIG_HOME: str = os.environ.get("XDG_CONFIG_HOME", "")
    config_dir_name = "vrc-avi-scaler"
    paths: list[Path] = [
        Path() / ".config" / config_dir_name / "translations",
    ]
    if XDG_CONFIG_HOME:
        paths.append(Path(XDG_CONFIG_HOME) / config_dir_name / "translations")
    else:
        paths.append(Path.home() / ".config" / config_dir_name / "translations")
    if APPDIR:
        paths.append(Path(APPDIR) / ".config" / config_dir_name / "translations")
        paths.append(Path(APPDIR) / "data" / "translations")
        paths.append(Path(APPDIR) / "translations")
    paths.append(Path() / "data" / "translations")
    paths.append(Path() / "translations")
    resolved_paths = [path.resolve() for path in paths]
    for path in resolved_paths:
        if path.is_dir():
            return path
    raise Exception(f"Couldn't find the translations directory. Paths: {resolved_paths}")

TRANSLATIONS_PATH = _get_translations_path()

def _get_indent_level(line: str) -> int:
    count: int = 0
    for char in line:
        if char == "\t":
            count += 1
        else:
            break
    return count

class Translator:
    def __init__(self) -> None:
        self._current_locale: str = ""
        self._loaded_locales: set[str] = set()
        self._entries: dict[str, str] = {}
        self.preferred_length_unit: str = "metre"
        self.shorten_length_unit: bool = True

    @staticmethod
    def get_system_locale() -> str|None:
        import locale
        lang, _ = locale.getlocale()
        return lang

    @property
    def system_locale(self) -> str:
        return Translator.get_system_locale() or "en"

    @staticmethod
    def get_available_locales() -> list[str]:
        locales: list[str] = []
        for translation_file_path in TRANSLATIONS_PATH.iterdir():
            if translation_file_path.suffix == TRANSLATION_FILE_SUFFIX:
                locales.append(translation_file_path.stem)
        return locales

    def add_translation_entry(self, key: str, template: str, replace: bool = False) -> None:
        if (not replace) and (key in self._entries):
            return
        self._entries[key] = template

    def has_key(self, key: str) -> bool:
        return key in self._entries

    def extend_from_file_path(self, file_path: Path, replace: bool = False) -> bool:
        try:
            temp_cache: dict[str, str] = {}
            with file_path.open(encoding="utf-8") as f:
                mode: int = 0
                line_num: int = 0
                parents: list[str] = []
                for line in f:
                    line_num += 1
                    if line.startswith("#"):
                        continue
                    if line.endswith("\n"):
                        line = line[:-1]
                    if not line:
                        continue
                    if line.startswith("\t"):
                        if not parents:
                            raise Exception(f"Parsing error. Invalid indent. Line {line_num}.")
                    space_index: int = line.find(" ")
                    indent_level: int = _get_indent_level(line)
                    if space_index >= 0:
                        if space_index <= indent_level:
                            raise Exception(f"Parsing error. Keys can't contain spaces. Line {line_num}.")
                        key: str = line[indent_level:space_index]
                        template: str = line[space_index+1:]
                        key = "".join(parents[:indent_level]) + key
                        temp_cache[key] = template
                    else:
                        if indent_level > len(parents):
                            raise Exception(f"Parsing error. Too much indent. Line {line_num}.")
                        if indent_level == len(parents):
                            parents.append(line[indent_level:])
                        else:
                            parents[indent_level] = line[indent_level:]
            for key, template in temp_cache.items():
                self.add_translation_entry(key, template, replace)
            return True
        except Exception as e:
            # I know these are not translated but that's an important compromise
            print(f"[ERROR] Failed to read translation file {file_path} - {e}")
            print(f"Current locale: {self._current_locale}")
            return False

    def _load_locale(self, locale: str, replace: bool) -> bool:
        if locale in self._loaded_locales:
            return True
        translation_file = TRANSLATIONS_PATH / f"{locale}{TRANSLATION_FILE_SUFFIX}"
        success = self.extend_from_file_path(translation_file, replace)
        if success:
            self._loaded_locales.add(locale)
            if self.has_key(DEPENDENCIES_KEY):
                locales = self.get_template(DEPENDENCIES_KEY, "").split(",")
                for locale_2 in locales:
                    if locale_2:
                        success = success and self._load_locale(locale_2, False)
        return success

    def set_locale(self, new_locale: str) -> bool:
        self._entries = {}
        self._loaded_locales = set()
        if new_locale.lower() == "auto" or new_locale.lower() == "system":
            locales = Translator.get_available_locales()
            system_locale = self.get_system_locale()
            if system_locale in locales:
                new_locale = system_locale
            else:
                new_locale = "en"
        success = self._load_locale(new_locale, True)
        if success:
            self._current_locale = new_locale
        return success

    @property
    def locale(self) -> str:
        return self._current_locale

    def has_key(self, key: str) -> bool:
        return True if key in self._entries else False

    def get_template(self, key: str, default: str|None = None) -> str:
        return self._entries.get(key, default if default != None else key)

    def localise_integer(self, value: int) -> str:
        if value < 0:
            return "-" + self.localise_integer(-value)
        group_size: int = 3
        group_separator: str = ","
        if self.has_key(".number.grouping.separator"):
            group_separator = self.translate(".number.grouping.separator")
        if self.has_key(".number.grouping.size"):
            group_size = int(self.translate(".number.grouping.size"))
        output: str = ""
        index: int = 0
        for digit in str(value)[::-1]:
            if index % group_size == 0:
                output += group_separator
            index += 1
            output += digit
        return output[:len(group_separator)-1:-1]

    def localise_rational_number(self, value: float) -> str:
        if value.is_integer():
            return self.localise_integer(int(value))
        if value < 0:
            return "-" + self.localise_rational_number(-value)
        decimal_separator: int = "."
        if self.has_key(".number.decimal_separator"):
            decimal_separator = self.translate(".number.decimal_separator")
        int_part = int(value)
        frac_part = value % 1
        int_str = self.localise_integer(int_part)
        return int_str + decimal_separator + str(frac_part)[2:]

    def localise_length(self, length: float, unit: str = "") -> str:
        if not unit:
            unit = self.preferred_length_unit
        min_value: float = 0.0
        max_value: float = 0.0
        multiplier: float = 1.0
        overflow: str = ""
        underflow: str = ""
        if self.has_key(f".length.unit.{unit}.max"):
            max_value = float(self.translate(f".length.unit.{unit}.max"))
        if self.has_key(f".length.unit.{unit}.min"):
            min_value = float(self.translate(f".length.unit.{unit}.min"))
        if self.has_key(f".length.unit.{unit}.multiplier"):
            multiplier = float(self.translate(f".length.unit.{unit}.multiplier"))
        if self.has_key(f".length.unit.{unit}.overflow"):
            overflow = self.translate(f".length.unit.{unit}.overflow")
        if self.has_key(f".length.unit.{unit}.underflow"):
            underflow = self.translate(f".length.unit.{unit}.underflow")
        multiplied_length = length * multiplier
        if max_value and overflow and multiplied_length > max_value:
            return self.localise_length(length, overflow)
        if min_value and underflow and multiplied_length < min_value:
            return self.localise_length(length, underflow)
        if self.shorten_length_unit:
            if multiplied_length == 1.0 and self.has_key(f".length.unit.{unit}.short.=1"):
                return self.translate(f".length.unit.{unit}.short.=1")
            return self.translate(
                f".length.unit.{unit}.short.any",
                value=multiplied_length
            )
        else:
            if multiplied_length == 1.0 and self.has_key(f".length.unit.{unit}.long.=1"):
                return self.translate(f".length.unit.{unit}.long.=1")
            return self.translate(
                f".length.unit.{unit}.long.any",
                value=multiplied_length
            )

    def interpret(self, template: str, *args: Any, **kwargs: Any) -> str:
        tape: list[str] = list(template)
        char_index: int = 0
        arg_index: int = 0
        mode: int = 0
        key: str = ""
        kwarg_name: str = ""
        kwarg_type: str = ""
        arg_value: Any = None
        hex_str: str = ""
        def insert_str_into_tape(string: str, index: int|None = None) -> None:
            index = index if index != None else char_index
            for char in reversed(string):
                tape.insert(index, char)
        def insert_str_into_tape_and_skip(string: str) -> None:
            nonlocal char_index
            insert_str_into_tape(string)
            char_index += len(string)
        while char_index < len(tape):
            char: str = tape[char_index]
            match mode:
                case 0:
                    if char == "%":
                        mode = 1
                        tape.pop(char_index)
                    else:
                        char_index += 1
                case 1:
                    # determine special mode
                    tape.pop(char_index)
                    match char:
                        case "%": # % literal
                            tape.insert(char_index, "%")
                            char_index += 1
                        case ".": # recursive reference
                            mode = 2
                            key = ""
                        case ":": # keyword argument
                            mode = 3
                            kwarg_name = ""
                        case "\\": # \n or \<hex>
                            mode = 5
                            hex_str = ""
                        case _:
                            mode = 0
                case 2:
                    tape.pop(char_index)
                    if char == "%":
                        mode = 0
                        template_2 = self.get_template(key, "")
                        insert_str_into_tape(template_2)
                    else:
                        key = key + char
                case 3:
                    tape.pop(char_index)
                    if char == "%":
                        mode = 4
                        arg_value = kwargs[kwarg_name]
                    else:
                        kwarg_name += char
                case 4:
                    # %:<kwarg_name>%(s|i|I|r|R|x)
                    tape.pop(char_index)
                    arg_type = char
                    value = arg_value
                    match arg_type:
                        case "s":
                            assert isinstance(value, str)
                            insert_str_into_tape_and_skip(value)
                        case "i":
                            assert isinstance(value, int)
                            insert_str_into_tape_and_skip(self.localise_integer(value))
                        case "I":
                            assert isinstance(value, int)
                            insert_str_into_tape_and_skip(str(value))
                        case "r":
                            assert isinstance(value, float)
                            insert_str_into_tape_and_skip(self.localise_rational_number(value))
                        case "R":
                            assert isinstance(value, float)
                            insert_str_into_tape_and_skip(str(value))
                        case "x":
                            assert isinstance(value, int)
                            insert_str_into_tape_and_skip(hex(value))
                        case "l":
                            assert isinstance(value, float)
                            insert_str_into_tape_and_skip(self.localise_length(value))
                        case _:
                            raise Exception(f"Not implemented kwarg type: {kwarg_type}.")
                    mode = 0
                case 5:
                    # %\
                    tape.pop(char_index)
                    if char == "n":
                        tape.insert(char_index, "\n")
                        char_index += 1
                        mode = 0
                    else:
                        hex_str += char
                        mode = 6
                case 6:
                    # hex number
                    tape.pop(char_index)
                    if char == "%":
                        insert_str_into_tape_and_skip(chr(int(hex_str.lower(), 16)))
                        mode = 0
                    else:
                        hex_str += char
                case _:
                    raise Exception(f"Invalid state: {mode}")
        return "".join(tape)

    def get_translated_text(self, key: str, *args: Any, **kwargs: Any) -> str:
        if key not in self._entries:
            return key
        template: str = self._entries[key]
        return self.interpret(template, *args, **kwargs)

    def translate(self, key: str, *args: Any, **kwargs: Any) -> str:
        return self.get_translated_text(key, *args, **kwargs)

translator: Translator = Translator()

def printl(key: str, *args: Any, **kwargs: Any) -> None:
    print(translator.translate(key, *args, **kwargs))
