import streamlit as st

st.title("3D 모델 자동 생성")

prompt = st.text_input("만들 모델을 자세히 설명해 주세요.")

if st.botton("생성하기"):
    with st.spinner("생성 중 입니다...."):
              #백엔드 주소
        re = requests.post("",json={"prompt"=prompt})
        result = res.json()

    st.success("생성 완료!")

    st.image(result["image"])

    
        
