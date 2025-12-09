import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import base64

Backend_URL = ""
Rackend_Undo_URL = ""
Rackend_Redo_URL = ""



st.info("생성된 이미지가 마음에 들지 않으시다면 질문을 더 자세히 해 주세요.")

st.title("3D 모델 자동 생성")
#st.markdown('# 3D 모델 자동 생성','### 4inlab')




# 프롬프트 입력.
prompt = st.text_input("만들 모델을 자세히 설명해 주세요.")

col, col_empty, col2 = st.columns([1,13,1])
with col:
    st.button("<-",
              key="undo",
              help="이전 이미지로 되돌립니다.")

with col2:
    st.button("->",
              key = "redo",
              help = "다음 이미지로 되돌립니다.")


if st.button("생성하기", use_container_width = True):
    if prompt.strip() == "":
        st.error("질문을 입력해 주세요.")
    else:
        try:
            with st.spinner("생성 중 입니다...."):

                #백엔드 주소
                response = requests.post(Backend_URL,json={"prompt":prompt})

                if response.status_code != 200:
                    st.error(str(response.status_code)+"Error")
                else:
                    result = response.json()

                    if "image_base" in result:
                        img_bytes = img_bytes = base64.b64decode(result["image_base64"])
                        img = Image.open(BytesIO(img_bytes))
                        st.image(img, use_column_width=True)
                    else:
                        st.warning("이미지 데이터를 불러 올 수 없습니다.")
        except Exception as e:
            st.error()

