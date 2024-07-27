import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

include_files = ["icon.ico"]

packages = [
    "json",
    "os",
    "sys",
    "datetime",
    "serial.tools.list_ports",
    "PyQt5.QtWidgets",
    "PyQt5.QtGui",
    "PyQt5.QtCore",
    "logging",
    "servo",
]

executables = [
    cx_Freeze.Executable(
        script="main.py",
        base=base,
        icon="icon.ico"
    )
]

cx_Freeze_options = {
    "packages": packages,
    "include_files": include_files,
    "excludes": [],
    "optimize": 2
}

cx_Freeze.setup(
    name="三星堆舵机控制",
    version="1.0.1",
    description="正式",
    options={"build_exe": cx_Freeze_options},
    executables=executables
)
