import streamlit as st
import openai
import requests
from io import BytesIO

st.title("GPT-4o 이미지 생성기")

import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI API KEY ---
openai_api_key = os.getenv("OPENAI_API_KEY")
prompt = st.text_input("이미지 프롬프트를 입력하세요:")

img_bytes = None
img_url = None

if st.button("이미지 생성"):
    if not openai_api_key:
        st.warning("API Key를 입력하세요.")
    elif not prompt:
        st.warning("프롬프트를 입력하세요.")
    else:
        with st.spinner("이미지 생성 중..."):
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                img_url = response.data[0].url
                img_bytes = requests.get(img_url).content
                st.image(img_url, caption="생성된 이미지")
            except Exception as e:
                st.error(f"이미지 생성 실패: {e}")

if img_bytes:
    st.download_button(
        label="이미지 다운로드",
        data=img_bytes,
        file_name="generated_image.png",
        mime="image/png"
    )