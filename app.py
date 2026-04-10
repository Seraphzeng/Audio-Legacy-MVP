import streamlit as st
import requests
import re

st.set_page_config(page_title="Family Sound Records", page_icon="🎙️")
st.title("Family Sound Records 聲音藝術實驗室")

# 1. 強力清洗 Key (解決 latin-1 編碼錯誤)
def clean_api_key(raw_key):
    return re.sub(r'[^A-Za-z0-9\-_]', '', raw_key).strip()

try:
    # 從 Secrets 讀取
    raw_key = st.secrets["STABILITY_KEY"]
    api_key = clean_api_key(raw_key)
except:
    st.error("❌ 請在 Streamlit Secrets 設置 STABILITY_KEY")
    st.stop()

uploaded_file = st.file_uploader("上傳語音...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("✨ 點擊生成：構建『破碎莊嚴』音景"):
        with st.spinner("正在嘗試連線 Stability AI 最新音頻端點..."):
            
            # --- 核心修正點：使用正式的 Stable Audio 1.0 端點 ---
            url = "https://api.stability.ai/v1/generation/stable-audio-1-0/text-to-audio"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "audio/mpeg"
            }

            payload = {
                "prompt": "Broken majesty, cinematic industrial ambient, emotional piano ripples, solemn atmosphere, 48khz",
                "seconds_total": 15 
            }

            try:
                # 採用 POST 請求
                response = requests.post(url, headers=headers, data=payload, timeout=60)

                if response.status_code == 200:
                    st.balloons()
                    st.success("✅ 生成成功！")
                    st.audio(response.content, format="audio/mpeg")
                else:
                    st.error(f"API 拒絕請求 (代碼: {response.status_code})")
                    # 這裡會顯示具體的錯誤原因
                    st.json(response.json())
                    
                    if response.status_code == 404:
                        st.warning("💡 如果持續 404，請檢查 Stability AI 官網是否要求針對 Audio 模型進行二次授權。")
            except Exception as e:
                st.error(f"連線異常: {str(e)}")

st.divider()
st.caption("ZENG JIAJING | 2026 實戰紀錄")
