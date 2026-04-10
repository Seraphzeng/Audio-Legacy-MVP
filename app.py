import streamlit as st
import requests
import re

st.set_page_config(page_title="Family Sound Records", page_icon="🎙️")
st.title("Family Sound Records 聲音藝術實驗室")

# 1. 強力清洗 Key：確保發送給伺服器的只有純淨的 ASCII 字符
def hard_clean_key(input_str):
    if not input_str:
        return ""
    return re.sub(r'[^A-Za-z0-9\-_]', '', input_str).strip()

try:
    # 讀取 Secrets
    raw_key = st.secrets["STABILITY_KEY"]
    api_key = hard_clean_key(raw_key)
except Exception as e:
    st.error("❌ 找不到 STABILITY_KEY。請確保 Secrets 格式為: STABILITY_KEY = \"sk-...\"")
    st.stop()

uploaded_file = st.file_uploader("上傳一段語音...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("✨ 執行轉化：生成『破碎莊嚴』音景"):
        with st.spinner("正在連線 Stability AI 穩定端點..."):
            
            # 注意：這是針對 Stable Audio 1.0 的精確路徑
            url = "https://api.stability.ai/v1/generation/stable-audio-1-0/text-to-audio"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "audio/mpeg"
            }

            # 使用標準參數，避免冗餘數據導致 400/404
            payload = {
                "prompt": "Broken majesty, cinematic industrial ambient, solemn atmosphere, emotional ripples",
                "seconds_total": 15 
            }

            try:
                # 採用 data=payload 以 multipart/form-data 形式發送（這對 v1 接口最穩定）
                response = requests.post(url, headers=headers, data=payload, timeout=45)

                if response.status_code == 200:
                    st.balloons()
                    st.success("✅ 實驗成功！音樂已生成。")
                    st.audio(response.content, format="audio/mpeg")
                else:
                    # 如果依舊報錯，顯示詳細信息
                    st.error(f"API 拒絕請求 (Status: {response.status_code})")
                    try:
                        st.json(response.json())
                    except:
                        st.write("伺服器返回內容：", response.text)
            except Exception as e:
                st.error(f"連線異常: {str(e)}")

st.divider()
st.caption("ZENG JIAJING | 2026 聲音藝術實驗紀錄")
