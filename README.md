# text2blender

text2blender는 사용자가 입력한 자연어 명령을 해석하여 자동으로 Blender Python 스크립트를 생성하고 실행하는 AI 기반 3D 모델링 자동화 도구입니다.

## 프로젝트 개요

**구성 요약**
- **Frontend (index.html)**: 사용자가 텍스트로 명령 입력  
- **Backend (app.py)**: 명령을 LLM API로 전송하여 Blender Python 코드 생성  
- **Blender Script (generated_script.py)**: Blender 내부에서 실행되어 실제 3D 오브젝트 생성

---

## 실행 방법

1. 가상환경 생성 및 활성화
2. 의존성 설치
   pip install -r requirements.txt
3. 서버 실행
   python backend/app.py
4. 클라이언트 실행
