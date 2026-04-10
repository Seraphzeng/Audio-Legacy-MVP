import streamlit as st
import requests

st.title("Family Sound Records 聲音藝術實驗室")
st.write("作為一名藝術家創業者，我致力於將家人的語音轉化為具有『破碎莊嚴感』的數字資產。")

uploaded_file = st.file_uploader("上傳一段語音...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.info("音頻已接收，準備轉化情感...")
    
    # 從你剛才設定的 Secrets 裡讀取密鑰
    try:
        api_key = st.secrets["STABILITY_KEY"]
    except:
        st.error("❌ 找不到 API Key，請檢查 Streamlit Secrets 設定！")
        st.stop()

    if st.button("✨ 點擊生成：將情感轉化為『破碎莊嚴』音樂"):
        with st.spinner("正在連線 Stability AI 服務器，提取情感共振..."):
            # 調用 API 生成音樂
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-audio/generate",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "audio/mpeg"
                },
                data={
                    "prompt": "Broken majesty, cinematic industrial ambient, heavy low-end, emotional ripples",
                    "output_format": "mp3",
                    "seconds_total": 30
                }
            )

            if response.status_code == 200:
                st.balloons()
                st.success("✅ 音樂生成成功！")
                st.audio(response.content, format="audio/mpeg")
            else:
                st.error(f"生成失敗，錯誤碼：{response.status_code}")
                st.write(response.json())
