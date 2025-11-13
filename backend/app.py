from flask import Flask, request, jsonify, send_from_directory
from llm import generate_script
from blender import run_blender_script
import os

app = Flask(__name__)
os.makedirs('generated_scripts', exist_ok=True)
os.makedirs('static/generated_models', exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        user_prompt = request.json.get('prompt')
        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # LLM으로 Blender 스크립트 생성
        script_code = generate_script(user_prompt)

        # 스크립트 파일 저장
        script_path = f"generated_scripts/{abs(hash(user_prompt))}.py"
        with open(script_path, 'w') as f:
            f.write(script_code)

        # Blender 실행 후 GLTF 모델 생성
        output_url = run_blender_script(script_path)

        return jsonify({"script": script_code, "output": output_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


