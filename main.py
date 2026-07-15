import os
import sys
import globals
import client
import server
import oscquery
from pathlib import Path
from config import ConfigLoadResult, reset_config_file, save_config, read_config
from simple_types import ParameterValue, Height, Any
from scaling_utils import get_base_eyeheight, parse_to_meters, is_valid_float
from translator import translator, printl
from command import Command
from task import Task, task_manager

FEEDBACK_URL = "https://github.com/KutayX7/vrc-avi-scaler/issues"

translator.set_locale("auto")
_ = translator.translate
globals.translator = translator

def shutdown() -> None:
    printl("main.shutting_down")
    if globals.save_config_on_exit:
        save_config()
    printl("main.can_close_terminal")
    os._exit(0)

def check_float(value: float) -> None:
    if not is_valid_float(value):
        raise Exception("Not a valid float.")

def command_quit(*_: list[Any]) -> None:
    shutdown()

def command_help(c: Command, args: list[Any]) -> None:
    if len(args) > 1:
        name = args[1]
        for command in globals.commands:
            if command.matches(name):
                print(command.helptext)
                return
        printl("main.unknown_command", command=name)
    else:
        for command in globals.commands:
            if command.available():
                helptext = command.helptext
                print(helptext)
                longest = 1
                for line in helptext.split("\n"):
                    longest = max(longest, len(line))
                print("-" * longest)

def command_clear(*_: list[Any]) -> None:
    print("\033[3J\033[H\033[2J", end="")

def set_eyeheight(eyeheight: float) -> None:
    if not globals.world_scaling_allowed:
        printl("main.scaling.not_available")
    if eyeheight > globals.MAX_EYEHEIGHT:
        printl("main.too_tall", max=globals.MAX_EYEHEIGHT)
        return
    if eyeheight < globals.MIN_EYEHEIGHT:
        printl("main.too_short", min=globals.MIN_EYEHEIGHT)
        return
    client = globals.client
    printl("main.set_eyeheight", height=eyeheight)
    client.set_eyeheight(eyeheight, globals.smooth_scaling_duration)

def command_minimum(*_: list[Any]) -> None:
    set_eyeheight(globals.world_min_eyeheight)

def command_maximum(*_: list[Any]) -> None:
    set_eyeheight(globals.world_max_eyeheight)

def command_normal(*_: list[Any]) -> None:
    set_eyeheight(get_base_eyeheight())

def command_vrmode(*_: list[Any]) -> None:
    server.set_vrmode(True, True)

def command_desktopmode(*_: list[Any]) -> None:
    server.set_vrmode(False, True)

def command_lock_vrmode(*_: list[Any]) -> None:
    globals.vrmode_lock = True
    printl("main.vrmode_locked_to", vrmode=int(globals.VRMode))

def command_nocompat(*_: list[Any]) -> None:
    globals.compat_killswitch = True

def command_fix_osc_client(*_: list[Any]) -> None:
    client = globals.client
    detected_ip: str = globals.osc_detected_VRChat_ip
    current_ip: str = client.ip
    if detected_ip and detected_ip != current_ip:
        client.reconnect(detected_ip, client.port)

def command_osc_debug(*_: list[Any]) -> None:
    globals.osc_debug_log = not globals.osc_debug_log
    if globals.osc_debug_log:
        printl("main.osc_debugging.enabled")
    else:
        printl("main.osc_debugging.disabled")

def command_osc_send(c: Command, args: list[Any]) -> None:
    address: str = args[1]
    list_to_send: list[ParameterValue] = []
    for token in args[2:]:
        if (not token) or not isinstance(token, str):
            printl("main.osc_send.malformed_message")
            return
        token_type = token[0:1]
        match token_type:
            case 'i':
                list_to_send.append(int(token[1:]))
            case 'f':
                list_to_send.append(float(token[1:]))
            case 'T':
                list_to_send.append(True)
            case 'F':
                list_to_send.append(False)
            case 's':
                printl("main.osc_send.cant_parse_strings")
                return
    printl("main.sending_osc_message", message=f"{address} {list_to_send}")
    globals.client.send_message(address, list_to_send)

def command_info(c: Command, args: list[Any]) -> None:
    printl("main.info.avatar")
    if globals.current_eyeheight > 0:
        if globals.VRMode:
            if globals.vrmode_lock:
                printl("main.info.mode.vr_manual")
            else:
                printl("main.info.mode.vr")
            printl("main.info.tracking_type", tracking_type=globals.tracking_type)
        else:
            if globals.vrmode_lock:
                printl("main.info.mode.desktop_manual")
            else:
                printl("main.info.mode.desktop")
        printl("main.info.calculated_base_eyeheight", height=get_base_eyeheight())
        printl("main.info.current_eyeheight", height=globals.current_eyeheight)
        printl("main.info.current_scale_factor", factor=globals.current_scale_factor)
    else:
        printl("main.info.not_available")
        printl("main.info.reload_avatar")
    if globals.smooth_scaling_duration > 0:
        printl("main.info.smooth_scaling.enabled")
        printl("main.info.smooth_scaling.duration", duration=globals.smooth_scaling_duration)
        printl("main.info.smooth_scaling.frequency", frequency=globals.smooth_scaling_step_frequency)
    else:
        printl("main.info.smooth_scaling.disabled")
    if globals.world_scaling_allowed:
        printl("main.info.world_limits")
        if (globals.world_min_eyeheight == 0 and
            globals.world_max_eyeheight == 0):
            printl("main.info.not_available")
            printl("main.info.reload_avatar")
        else:
            printl("main.info.world_eyeheight.min", height=globals.world_min_eyeheight)
            printl("main.info.world_eyeheight.max", height=globals.world_max_eyeheight)
            printl("main.info.world_eyeheight.notice")
    else:
        printl("main.info.scaling_disabled")

def command_override(*_: list[Any]) -> None:
    globals.world_min_eyeheight = globals.MIN_EYEHEIGHT
    globals.world_max_eyeheight = globals.MAX_EYEHEIGHT
    globals.world_scaling_allowed = True
    printl("main.override.forgot")
    printl("main.override.warning")

def command_instant(*_: list[Any]) -> None:
    globals.smooth_scaling_duration = 0
    print("main.instant_scaling")

def command_smooth(_: Command, args: list[Any]) -> None:
    length: float = globals.smooth_scaling_default_duration
    try:
        length = abs(float(args[1]))
        check_float(length)
    except:
        printl("main.smooth_scaling.invalid_duration")
    finally:
        if globals.smooth_scaling_duration <= 0:
            printl("main.smooth_scaling.enabled")
        globals.smooth_scaling_duration = length
        printl("main.smooth_scaling.duration", duration=length)
        if globals.current_eyeheight == 0:
            printl("main.smooth_scaling.reload_avatar")

def command_framerate(_: Command, args: list[Any]) -> None:
    try:
        fps = abs(float(args[1]))
        check_float(fps)
        globals.FPS = fps
        globals.config.set("fps", fps)
        globals.smooth_scaling_step_frequency = fps * 4
        printl("main.framerate.set_to", fps=fps)
    except:
        printl("main.invalid_argument")

def command_frequency(_: Command, args: list[Any]) -> None:
    try:
        if len(args) == 1:
            pass
        elif args[1] == "reset":
            globals.smooth_scaling_step_frequency = globals.FPS * 4
        else:
            frequency = abs(float(args[1]))
            check_float(frequency)
            globals.smooth_scaling_step_frequency = frequency
    except:
        printl("main.invalid_argument")
    finally:
        printl("main.frequency.set_to", frequency=globals.smooth_scaling_step_frequency)

def command_save(*_: list[Any]) -> None:
    save_config()

def command_autosave(*_: list[Any]) -> None:
    globals.save_config_on_exit = True
    globals.config.set("autosave", True)
    printl("main.autosave.on")
    printl("main.autosave.info")

def command_manuelsave(*_: list[Any]) -> None:
    globals.save_config_on_exit = False
    globals.config.set("autosave", False)
    printl("main.autosave.off")

def command_configure(*_: list[Any]) -> None:
    termux_properties = Path.home() / ".termux" / "termux-properties"
    if (termux_properties.exists() and
            "\nallow-external-apps = true" not in termux_properties.read_text()):
        printl("main.termux.allow_external_apps", config_path=str(globals.config.path))
    else:
        printl("main.opening_config")
        globals.config.show_in_file_explorer()

def command_delay(_: Command, args: list[Any]) -> None:
    if len(args) < 3:
        printl("main.invalid_argument")
        return
    delay: float = args[1]
    if isinstance(delay, int):
        delay = float(delay)
    if not isinstance(delay, float):
        printl("main.invalid_argument")
        return
    str_args: list[str] = [str(args[2])]
    for arg in args[3:]:
        if isinstance(arg, str):
            str_args.append(f'"{arg.replace("\\", "\\\\").replace("\"", "\\\"")}"')
        else:
            str_args.append(str(arg))
    full_command = " ".join(str_args)
    task = (Task("delayed_command")
        .attach_callback(process_command)
        .add_arg(full_command)
    )
    task_manager.add_task(task, delay)

# TODO: Move command implementations to a different file

globals.commands = {
    Command("quit", {"exit"}).bind(command_quit),
    Command("help", set()).bind(command_help),
    Command("clear", {"cls"}).bind(command_clear),
    Command("minimum", {"min"}).bind(command_minimum),
    Command("maximum", {"max"}).bind(command_maximum),
    Command("normal", {"reset", "norm", "base"}).bind(command_normal),
    Command("vrmode", {"vr"}).bind(command_vrmode),
    Command("desktopmode", {"desktop", "nonvr", "novr", "nvr"}).bind(command_desktopmode),
    Command("lock_vrmode", {"lockvrmode", "lvrm", "lvm", "lm"}).bind(command_lock_vrmode),
    Command("nocompat", {"pure"}).bind(command_nocompat),
    Command("fix_osc_client", set()).bind(command_fix_osc_client),
    Command("osc_debug", set()).bind(command_osc_debug),
    Command("osc_send", set()).bind(command_osc_send),
    Command("info", {"i"}).bind(command_info),
    Command("override", {"o"}).bind(command_override),
    Command("instant", set()).bind(command_instant),
    Command("smooth", {"s"}).bind(command_smooth),
    Command("framerate", {"fps"}).bind(command_framerate),
    Command("frequency", {"freq"}).bind(command_frequency),
    Command("save", set()).bind(command_save),
    Command("autosave", set()).bind(command_autosave),
    Command("manuelsave", {"manualsave", "noautosave"}).bind(command_manuelsave),
    Command("configure", {"config", "conf", "cfg"}).bind(command_configure),
    Command("delay", {"d"}).bind(command_delay),
}

def process_command(full_command: str) -> None:
    for command in globals.commands:
        if command.matches(full_command):
            command.run(full_command)
            return
    # check if it's a height value
    try:
        eyeheight = parse_to_meters(full_command, globals.current_eyeheight)
        if eyeheight:
            set_eyeheight(eyeheight)
    except:
        printl("main.unknown_command", command=full_command)

def get_available_terminal_emulator() -> str|None:
    from shutil import which
    terminal: str = (
        which("konsole") or
        which("gnome-terminal") or
        which("xfce4-terminal") or
        which("alacritty") or
        which("lxterminal") or
        which("kitty") or
        which("wezterm") or
        which("terminator") or
        which("urxvt") or
        which("xterm") or
        ""
    )
    return which(os.environ.get("TERMINAL", terminal))

def get_terminal_exec_args(terminal: str) -> list[str]:
    if "/" in terminal:
        terminal = terminal[terminal.rindex("/")+1:]
    match terminal:
        case "konsole" | "xterm" | "lxterminal" | "urxvt" | "terminator":
            return ["-e"]
        case "wezterm":
            return ["start", "--"]
        case _:
            return ["--"]

def relaunch_in_new_terminal() -> None:
    import subprocess
    terminal = get_available_terminal_emulator()
    if not terminal:
        return
    exec_args = get_terminal_exec_args(terminal)
    main_path = Path(__file__).resolve()
    dir_path = main_path.parent
    if os.environ.get("APPIMAGE"):
        main_path = Path(os.environ["APPIMAGE"]).resolve()
        dir_path = main_path.parent
        launch_command = f"cd {dir_path} && {main_path}"
    else:
        if __file__.endswith(".py"):
            launch_command = f"cd {dir_path} && {sys.executable} {main_path}"
        else:
            launch_command = f"cd {dir_path} && {main_path}"
    subprocess.Popen([terminal] + exec_args + ["bash", "-c"] + [launch_command])
    os._exit(0)

def should_relaunch_in_new_terminal() -> bool:
    if os.name != "posix":
        return False
    if sys.stdout.isatty():
        return False
    if sys.stdin.isatty():
        return False
    if sys.stderr.isatty():
        return False
    return True

def main() -> None:
    print("\033[0;33m[ KutayX7's VRChat Avi Scaler ]\033[0m")
    globals.config.load()
    (
        globals.config
        .register("fps", 90.0)
        .register("autosave", False)
        .register("osc.client.ip", '127.0.0.1')
        .register("osc.client.port", 9000)
        .register("osc.server.ip", '127.0.0.1')
        .register("osc.server.port", 9001)
        .register("oscquery.enable", True)
        .register("localisation.locale", "auto")
        .register("compat.Mag's Scale Adjuster", True)
        .register("compat.Jackal Scaling System", True)
        .register("compat.OpenVRCScaler", True)
    )
    config_read_result = read_config()
    printl("main.feedback", link = FEEDBACK_URL)
    match config_read_result:
        case ConfigLoadResult.SUCCESS:
            pass
        case ConfigLoadResult.NOT_FOUND:
            printl("main.init.config.not_found")
            reset_config_file()
        case ConfigLoadResult.ACCESS_DENIED:
            printl("main.init.config.access_denied")
            sys.exit(-1)
        case ConfigLoadResult.CORRUPTED:
            printl("main.init.config.corrupted")
            choice = input(_("prompt.options.yes_NO"))
            if choice in _("%choice.yes"):
                reset_config_file()
            else:
                printl("main.init.config.continue")
                choice = input(_("prompt.options.yes_NO"))
                if choice in _("%choice.yes"):
                    pass
                else:
                    shutdown()

    print( "--------------------------------")
    printl("main.to.get_help")
    printl("main.to.quit")
    print( "--------------------------------")

    osc_server_ip = globals.osc_server_ip
    osc_server_port = globals.osc_server_port
    globals.client = client.start_client(globals.osc_client_ip, globals.osc_client_port)
    if globals.oscquery_enabled:
        osc_server_ip = ''
        oscquery.start_service()
        osc_server_port = globals.oscquery_service_port
    globals.server = server.start_server(osc_server_ip, osc_server_port)
    if globals.oscquery_enabled:
        oscquery.start_listener()

    while True:
        try:
            user_input = input("")
            commands = Command.separate_commands(user_input)
            for command in commands:
                if command:
                    process_command(command)
        except EOFError:
            # not running in a terminal
            break
    # continue to run as a background service
    while True:
        pass

if __name__ == "__main__":
    if should_relaunch_in_new_terminal():
        relaunch_in_new_terminal()
    main()
