import streamlit as st
import requests

st.title("Family Sound Records 聲音藝術實驗室")

# 安全讀取 Key
try:
    api_key = st.secrets["STABILITY_KEY"].strip()
except:
    st.error("❌ Secrets 中找不到 STABILITY_KEY")
    st.stop()

uploaded_file = st.file_uploader("上傳一段語音自述...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("✨ 點擊生成：轉化為『破碎莊嚴』音樂"):
        with st.spinner("正在連線 Stability AI..."):
            
            # 修正後的穩定路徑 (Stable Audio 1.0)
            url = "https://api.stability.ai/v1/generation/stable-audio-1-0/text-to-audio"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "audio/mpeg"
            }

            payload = {
                "prompt": "Broken majesty, cinematic industrial ambient, emotional piano, solemn atmosphere",
                "steps": 50,
                "seconds_total": 30
            }

            response = requests.post(url, headers=headers, data=payload)

            if response.status_code == 200:
                st.success("✅ 生成成功！")
                st.audio(response.content)
            else:
                st.error(f"生成失敗 (Status: {response.status_code})")
                st.json(response.json())
