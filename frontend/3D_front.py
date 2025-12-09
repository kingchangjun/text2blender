import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import base64

#api 주소.
BACKEND_GENTATE = ""
BACKEND_ASK = ""
BACKEND_HISTORY =""
BACKEND_LOAD_IMAGE = "" 
BACKEND_NEW_SESSION = ""

#세션 확인
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

if "current_image" not in st.session_state:
    st.session_state.current_image = None

if "current_script" not in st.session_state:
    st.session_state.current_script = None

if "llm_answer" not in st.session_state:
    st.session_state.llm_answer = ""


#사이드바 디자인
if st.sidebar.button("새 이미지 만들기"):
    res = requests.post(BACKEND_NEW_SESSION)
    data = res.json()

    st.session_state.current_session_id = data["session_id"]
    st.session_state.current_image = data["image_base64"]
    st.session_state.current_script = data["script"]
    st.session_state.llm_answer = "새 세션을 시작했습니다."

st.sidebar.title("3D 모델 생성")
st.sidebar.collapsed = False

# 프롬프트 입력, 이미지 생성.
prompt = st.sidebar.text_area("만들 모델을 자세히 설명해 주세요.",height = 100)
if st.sidebar.button("Create",type = "primary",width = "stretch"):
    if not st.session_state.current_session_id:
        st.warning("먼저 '새 이미지 만들기'를 클릭해서 새 세션을 시작하세요.")
    else:
        with st.spinner("이미지 생성 중입니다..."):
            res = requests.post(BACKEND_ASK, json={
                "session_id": st.session_state.current_session_id,
                "prompt": prompt
        })

        data = res.json()

        st.session_state.llm_answer = data.get("llm_answer", "")
        st.session_state.current_image = data.get("image_base64", "")
        st.session_state.current_script = data.get("script", "")

st.sidebar.subheader("📜 히스토리")
history = requests.get(BACKEND_HISTORY).json()

for item in history:
    if st.sidebar.button(f"{item['id']} - {item['prompt'][:20]}"):
        img_res = requests.get(f"{BACKEND_LOAD_IMAGE}/{item['id']}")
        img_data = img_res.json()

        st.session_state.current_image = img_data["image_base64"]
        st.session_state.current_script = img_data["script"]
        st.session_state.llm_answer = img_data["llm_answer"]
        st.session_state.current_session_id = img_data["session_id"]




#메인 디자인
st.title("3D 모델링 생성")

if st.session_state.current_image:
    img_bytes = base64.b64decode(st.session_state.current_image)
    img = Image.open(BytesIO)
    st.image(img, caption = "현재 렌더링 이미지", use_column_width = True)





st.info("생성된 이미지가 마음에 들지 않으시다면 질문을 더 자세히 해 주세요.")
