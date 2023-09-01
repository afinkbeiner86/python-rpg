import sys
from pathlib import Path
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"include_files": "assets"}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="TerraMythica",
    version="1.0.0",
    description="Tiny RPG in Python.",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("terramythica.py", base=base, target_name="TerraMythica", icon=Path("./assets/graphics/icon/icon.ico"))
    ],
)
