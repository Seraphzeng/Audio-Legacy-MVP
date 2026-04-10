import streamlit as st
import librosa
import numpy as np

st.set_page_config(page_title="Family Sound Art", page_icon="🎙️")
st.title("Family Sound Records 聲音藝術實驗室")
st.markdown("---")

st.write("作為一名藝術家創業者，我致力於將家人的語音轉化為具有『破碎莊嚴感』的數字資產。")

uploaded_file = st.file_uploader("上傳一段語音...", type=["wav", "mp3"])

if uploaded_file:
    # 進行情感模式識別
    y, sr = librosa.load(uploaded_file)
    energy = np.mean(librosa.feature.rms(y=y))
    
    st.subheader("核心模式識別結果：")
    if energy > 0.05:
        st.success("能量特徵：激昂/宏大。推薦配樂：沈穩的工業低音。")
    else:
        st.info("能量特徵：空靈/沈思。推薦配樂：破碎的鋼琴旋律。")
    
    st.warning("下一步將串接 AI 接口，生成專屬音樂。")
