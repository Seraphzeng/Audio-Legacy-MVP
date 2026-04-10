import streamlit as st
import requests

st.set_page_config(page_title="Family Sound Records", page_icon="🎙️")

st.title("Family Sound Records 聲音藝術實驗室")
st.write("目前狀態：後端 API 聯調中... 目標：實現『破碎莊嚴感』音樂生成。")

# 1. 徹底清洗 Key，確保沒有任何編碼問題
try:
    raw_key = st.secrets["STABILITY_KEY"]
    api_key = raw_key.strip().encode('utf-8').decode('ascii', 'ignore')
except Exception as e:
    st.error("❌ Secrets 配置錯誤，請檢查 STABILITY_KEY 是否填寫正確。")
    st.stop()

uploaded_file = st.file_uploader("上傳一段語音...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("✨ 執行生成：轉化為『破碎莊嚴』音樂"):
        with st.spinner("正在調用 Stability Audio 1.0 引擎..."):
            
            # 使用 v1 穩定版接口，這通常比 beta 版更不容易報 404
            url = "https://api.stability.ai/v1/generation/stable-audio-1-0/text-to-audio"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "audio/mpeg"
            }

            # 這是針對你「破碎莊嚴感」風格微調的 Prompt
            payload = {
                "prompt": "Broken majesty, minimalist industrial, cinematic soundscape, emotional strings, low drone, 48kHz, professional master",
                "seconds_total": 30
            }

            try:
                # 注意：這裡使用 data=payload 發送表單數據
                response = requests.post(url, headers=headers, data=payload)

                if response.status_code == 200:
                    st.balloons()
                    st.success("✅ 實驗成功！聲音遺產已生成。")
                    st.audio(response.content, format="audio/mpeg")
                    st.download_button("💾 下載音軌", response.content, file_name="majesty_v1.mp3")
                else:
                    st.error(f"API 報錯 (Status: {response.status_code})")
                    # 顯示具體錯誤，幫助我們判斷是餘額不足還是參數問題
                    st.json(response.json())
                    
            except Exception as e:
                st.error(f"連線異常：{str(e)}")

st.divider()
st.caption("ZENG JIAJING | 2026 聲音藝術實驗紀錄")
