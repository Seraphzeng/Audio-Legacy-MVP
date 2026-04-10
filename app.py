import streamlit as st
import requests
import re

# 頁面配置
st.set_page_config(page_title="Family Sound Records", page_icon="🎙️")

st.title("Family Sound Records 聲音藝術實驗室")
st.write("當前任務：強制修復編碼報錯並執行 API 調用")

# 1. 超強效 Key 清洗函數
def hard_clean_key(input_str):
    if not input_str:
        return ""
    # 只允許 ASCII 範圍內的英文字母、數字和基礎橫槓符號
    # 徹底剔除所有全形引號、空格或不可見字符
    cleaned = re.sub(r'[^A-Za-z0-9\-_]', '', input_str)
    return cleaned.strip()

try:
    # 從 Secrets 讀取並清洗
    raw_key = st.secrets.get("STABILITY_KEY", "")
    api_key = hard_clean_key(raw_key)
    
    if not api_key:
        st.error("❌ 錯誤：清洗後的 API Key 為空。請檢查 Streamlit Secrets 配置。")
        st.stop()
except Exception as e:
    st.error(f"❌ 無法訪問 Secrets: {e}")
    st.stop()

# 2. 文件上傳介面
uploaded_file = st.file_uploader("上傳一段語音自述...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("✨ 執行轉化：生成『破碎莊嚴』音景"):
        with st.spinner("正在執行加密傳輸並生成音樂..."):
            
            # 使用官方推薦的 Stable Audio 1.0 穩定端點
            url = "https://api.stability.ai/v1/generation/stable-audio-1-0/text-to-audio"
            
            # 手動構建 headers，避免 Python requests 自動編碼時出錯
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "audio/mpeg"
            }

            # 優化後的 Prompt 參數
            payload = {
                "prompt": "Broken majesty, cinematic industrial ambient, emotional piano ripples, solemn atmosphere, high fidelity, 48khz",
                "seconds_total": 15  # 測試階段設定為 15 秒以節省點數
            }

            try:
                # 發送請求，設定 30 秒超時防止掛死
                response = requests.post(url, headers=headers, data=payload, timeout=30)

                if response.status_code == 200:
                    st.balloons()
                    st.success("✅ 實驗成功！已成功繞過編碼限制並生成音軌。")
                    st.audio(response.content, format="audio/mpeg")
                    
                    st.download_button(
                        label="💾 下載生成音軌",
                        data=response.content,
                        file_name="legacy_v1_fixed.mp3",
                        mime="audio/mpeg"
                    )
                else:
                    # 如果失敗，顯示詳細狀態碼，幫助診斷是點數問題還是端點問題
                    st.error(f"API 拒絕請求 (Status: {response.status_code})")
                    try:
                        st.json(response.json())
                    except:
                        st.write(response.text)
                        
            except Exception as e:
                st.error(f"連線發生異常: {str(e)}")

# 底部紀錄
st.divider()
st.caption("ZENG JIAJING | 2026 聲音藝術實驗紀錄")
