import streamlit as st
import requests
import re

# 頁面基本配置
st.set_page_config(page_title="Family Sound Records", page_icon="🎙️")
st.title("Family Sound Records 聲音藝術實驗室")

# 1. 強力清洗機制：防止 latin-1 編碼錯誤
def hard_clean_key(input_str):
    if not input_str:
        return ""
    # 只允許 ASCII 字符，徹底剔除不可見字符或全形符號
    return re.sub(r'[^A-Za-z0-9\-_]', '', input_str).strip()

try:
    # 從 Secrets 讀取並清洗
    raw_key = st.secrets.get("STABILITY_KEY", "")
    api_key = hard_clean_key(raw_key)
    
    if not api_key:
        st.error("❌ 錯誤：請在 Streamlit Secrets 中配置 STABILITY_KEY")
        st.stop()
except Exception as e:
    st.error(f"❌ 無法讀取 Secrets: {e}")
    st.stop()

# 2. 交互介面
uploaded_file = st.file_uploader("上傳一段語音...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("✨ 執行轉化：生成『破碎莊嚴』音景"):
        with st.spinner("正在連線 Stability AI (授權驗證中)..."):
            
            # 策略：嘗試 Stable Audio 1.0 端點
            url = "https://api.stability.ai/v1/generation/stable-audio-1-0/text-to-audio"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "audio/mpeg"
            }

            payload = {
                "prompt": "Broken majesty, cinematic industrial ambient, emotional piano ripples, solemn atmosphere",
                "seconds_total": 15 
            }

            try:
                # 發送請求
                response = requests.post(url, headers=headers, data=payload, timeout=45)

                if response.status_code == 200:
                    st.balloons()
                    st.success("✅ 實驗成功！權限已生效並生成音樂。")
                    st.audio(response.content, format="audio/mpeg")
                elif response.status_code == 404:
                    st.warning("⚠️ 收到 404 錯誤。這通常是因為 Community License 激活後，伺服器數據同步需要時間（約 15-30 分鐘）。")
                    st.info("建議：請先合上電腦休息，明早醒來權限同步後再試一次。")
                    st.json(response.json())
                else:
                    st.error(f"API 拒絕請求 (Status: {response.status_code})")
                    try:
                        st.json(response.json())
                    except:
                        st.write(response.text)
                        
            except Exception as e:
                st.error(f"連線發生異常: {str(e)}")

st.divider()
st.caption("ZENG JIAJING | 2026 聲音藝術實驗紀錄")
