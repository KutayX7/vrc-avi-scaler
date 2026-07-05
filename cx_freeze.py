import sys
import subprocess
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [],
    'zip_exclude_packages': [],
    'excludes': [],
}

base = 'console'

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", "0.0.1", None, "Scale your avatar over OSC", "IconId", None),
    ],
    "Icon": [
        ("IconId", "icon_windows.ico"),
    ],
    "Shortcut": [
        ("DesktopShortcut", "DesktopFolder", "VRChat Avatar Scaler",
         "TARGETDIR", "[TARGETDIR]vrchat_avatar_scaler.exe",
         None, None, None, None, None, None, "TARGETDIR"),
        ("StartMenuShortcut", "MyProgramMenu", "VRChat Avatar Scaler",
         "TARGETDIR", "[TARGETDIR]vrchat_avatar_scaler.exe",
         None, None, None, None, None, None, "TARGETDIR"),
    ],
}

bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data,
    "upgrade_code": "{1e24271f-7f5a-4075-a957-5eab6e44b451}",
    "output_name": "vrc-avi-scaler.msi",
}
bdist_appimage_options = {
    "target_name": "vrc-avi-scaler.AppImage",
}

# Pick the right icon per platform
if sys.platform == "win32":
    icon = 'icon_windows.ico'
else:
    icon = 'icon_128x128.png'

executables = [
    Executable(
        'main.py',
        base=base,
        icon=icon,
    ),
]

setup(name='vrc-avi-scaler',
      version = '0.0.1',
      description = "Change your avatar's scale over osc",
      license = "MIT License",
      options = {
      'build_exe': build_options,
      'bdist_msi': bdist_msi_options,
      'bdist_appimage': bdist_appimage_options,
      },
      executables = executables)
