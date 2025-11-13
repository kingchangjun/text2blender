import subprocess
import os
import sys


def run_blender_script(script_path: str) -> str:
    output_file = script_path.replace(".py", ".png")
    BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"
    cmd = [
       BLENDER_PATH, "-b", "-P", script_path,
       "--", output_file
	]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Blender Error:", result.stderr)
        raise RuntimeError("Blender script failed")
    return f"/{output_file}"

