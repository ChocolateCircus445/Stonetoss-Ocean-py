import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "requests", "PIL", "io", "pyperclip", "html", "sys", "tkinter"]
}

bdist_mac_options = {
    "iconfile": "icon.icns",
    "bundle_name": "Stonetoss Ocean",
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Stonetoss-Ocean",
        version = "1.1",
        description = "Stonetoss is a Nazi. Fetches Stonetoss comics so you don't have to!",
        options = {"build_exe": build_exe_options, "bdist_mac": bdist_mac_options},
        executables = [Executable("stogui.py", base=base, targetName="Stonetoss Ocean", icon="icon.ico")])
