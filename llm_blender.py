import os
import subprocess  # docker run을 위해.
import textwrap    # 긴 문자열에서 들여쓰기 제거.
from pathlib import Path

import ollama      # 로컬 LLM(ollama) 호출용

# 블렌더 도커 이미지 이름
IMAGE_NAME = "nytimes/blender"

# 스크립트 파일 저장 폴더
SAVE_DIR = Path("./saves")


def generate_blender_script(user_prompt: str) -> str:
    """
    Ollama(qwen3-coder:30b)를 사용해서
    사용자의 자연어 프롬프트 → Blender용 Python 스크립트로 변환
    """
    system_prompt = textwrap.dedent("""
    You are an expert Blender Python scripter.
    
    [TASK]
    Generate Python code (bpy) to create 3D objects based on the user's prompt.

    [VALID PRIMITIVES (Use ONLY these)]
    - bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
    - bpy.ops.mesh.primitive_uv_sphere_add(location=(x,y,z))
    - bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(x,y,z))
    - bpy.ops.mesh.primitive_cylinder_add(location=(x,y,z))
    - bpy.ops.mesh.primitive_cone_add(location=(x,y,z))
    - bpy.ops.mesh.primitive_torus_add(location=(x,y,z))
    - bpy.ops.mesh.primitive_monkey_add(location=(x,y,z))

    [CRITICAL RULES]
    1. Output ONLY valid Python code. NO markdown, NO text explanations.
    2. Always start with: import bpy; import math
    3. Always clear scene: bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    4. IF the user asks for a shape NOT in the list (like Dodecahedron, Hexagon):
       -> Use 'primitive_ico_sphere_add(subdivisions=1)' or 'primitive_cylinder_add(vertices=6)' to approximate it.
       -> Do NOT try to create complex meshes manually.
    5. IF the user asks for a complex object (Tree, Car):
       -> Combine multiple primitives (Cylinders, Cubes) to build it.

    [RESPONSE FORMAT]
    import bpy
    import math
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    # Your generated code here...
    """)

    # ollama에게 보낼 메세지 구성.
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # ollama 호출
    response = ollama.chat(
        model="qwen3-coder:30b",  
        messages=messages
    )

    script_code = response["message"]["content"]

    return script_code


def save_script(script_code: str, job_name: str) -> Path:
    """
    LLM이 생성한 스크립트를 ./saves 폴더에 저장
    """
    SAVE_DIR.mkdir(exist_ok=True)  # saves 폴더 없으면 생성

    script_path = SAVE_DIR / f"{job_name}.py"

    # 문자열 기반 코드 검사. 해당 문자열이 있으면 예외 처리. 실행 X
    forbidden = ["import os", "import sys", "subprocess", "socket", "requests"]
    for bad in forbidden:
        if bad in script_code:
            raise ValueError("스크립트에 허용되지 않는 코드 존재: " + bad)

    script_path.write_text(script_code, encoding="utf-8")

    return script_path


def run_blender_in_docker(script_path: Path):
    """
    Docker 컨테이너 안에서 Blender를 실행해서
    save_script로 저장한 파이썬 스크립트를 -P 옵션으로 돌린다.
    """

    # 현재 작업 디렉토리
    project_root = Path.cwd()

    # 로컬 세이브 파일 경로.
    local_saves_dir = project_root / "saves"

    # 컨테이너 내부에서 볼 스크립트 경로.
    container_script_path = f"/saves/{script_path.name}"

    cmd = [
        "docker", "run", "--rm",            # 컨테이너 종료 시 삭제.
        "-v", f"{local_saves_dir}:/saves",  # ← 컨테이너 안에서 /saves 로 마운트
        IMAGE_NAME,
        "blender", "-b", "-P", container_script_path
    ]

    print("\n[Docker] 다음 명령을 실행합니다:")
    print(" ", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True  # bytes 대신 문자열로 출력.
    )

    print("\n=== Blender Docker STDOUT ===")
    print(result.stdout)

    print("=== Blender Docker STDERR ===")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Blender Docker 실행 실패 (return code {result.returncode})")


def main():
    user_prompt = input("원하는 ３Ｄ 모델 : ")

    print("\n[1] LLM에게 Blender 스크립트 생성 요청 중...")
    script_code = generate_blender_script(user_prompt)

    print("\n[2] 생성된 스크립트 일부 미리보기:\n")
    print(script_code[:500], "...\n")

    print("[3] 스크립트 저장 중...")
    script_path = save_script(script_code, job_name="test_job")
    print(f" → {script_path} 에 저장 완료")

    print("\n[4] Docker에서 Blender 실행 중...")
    run_blender_in_docker(script_path)

    print("\n[완료] 모든 작업이 끝났습니다.")


if __name__ == "__main__":
    main()
