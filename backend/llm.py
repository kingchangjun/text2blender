import subprocess
import json

def generate_script(prompt: str) -> str:
    """
    LLM을 사용해서 Blender Python 스크립트를 생성.
    Blender에서 GLTF로 export하도록 코드 생성.
    """
    full_prompt = (
        "You are a 3D modeling assistant. "
        "Generate a Blender Python script based on the following instruction:\n"
        f"{prompt}\n\n"
        "Only output pure Python code for Blender API, no explanations."
    )

    cmd = ["ollama", "run", "llama3:latest", full_prompt]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        raise RuntimeError("LLM script generation failed")
    return result.stdout.strip()

