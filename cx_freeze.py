import os
import sys
from cx_Freeze import setup, Executable

gitRelease=os.environ['RELEASEVERSION']

#linux zsync update data
if sys.platform == "linux":
	gitRepo=os.environ['GITHUB_REPOSITORY_CLEAN']
	zsyncUpdateType="gh-releases-zsync|"
	zsyncFileName="|kvas-*.AppImage"
	zsyncUpdateValue= zsyncUpdateType + gitRepo + zsyncFileName

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [],
    'zip_exclude_packages': [],
    'excludes': [],
    'include_files': [
        #('translations', 'translations'),
    ],
}

base = 'gui'

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", "gitRelease", None, "Scale your avatar over OSC", "IconId", None),
    ],
    "Icon": [
        ("IconId", "icon_windows.ico"),
    ],
    "Shortcut": [
        ("DesktopShortcut", "DesktopFolder", "KVAS",
         "TARGETDIR", "[TARGETDIR]main.exe",
         None, None, None, None, None, None, "TARGETDIR"),
        ("StartMenuShortcut", "MyProgramMenu", "KVAS",
         "TARGETDIR", "[TARGETDIR]main.exe",
         None, None, None, None, None, None, "TARGETDIR"),
    ],
}

bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data,
    "upgrade_code": "{1e24271f-7f5a-4075-a957-5eab6e44b451}",
    "output_name": "kvas-installer",
}
bdist_appimage_options = {
    "target_name": "kvas",
    #i need to escape it from quotes
    "updateinformation": zsyncUpdateValue
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

setup(name='kvas',
      version = gitRelease,
      description = "Change your avatar's scale over osc",
      license = "MIT License",
      options = {
      'build_exe': build_options,
      'bdist_msi': bdist_msi_options,
      'bdist_appimage': bdist_appimage_options,
      },
      executables = executables)
