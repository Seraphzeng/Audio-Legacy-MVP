import streamlit as st
import requests
import json

st.set_page_config(page_title="Family Sound Records", page_icon="🎙️")

st.title("Family Sound Records 聲音藝術實驗室")
st.write("目標：解決 404 報錯，成功生成音樂資產。")

# 1. 密鑰讀取（極致清洗）
try:
    # 確保 API Key 乾乾淨淨
    api_key = st.secrets["STABILITY_KEY"].strip()
except Exception as e:
    st.error("❌ Secrets 中找不到 STABILITY_KEY，請檢查配置。")
    st.stop()

uploaded_file = st.file_uploader("上傳一段語音自述...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("✨ 點擊生成：構建『破碎莊嚴』音景"):
        with st.spinner("正在連線 Stability AI 穩定端點 (v1)..."):
            
            # 使用官方文檔建議的生成端點
            url = "https://api.stability.ai/v1/generation/stable-audio-1-0/text-to-audio"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json", # 強制指定 JSON 格式
                "Accept": "audio/mpeg"
            }

            # 針對你的音樂審美調校的 Prompt
            payload = {
                "prompt": "Broken majesty, cinematic industrial, emotional piano, deep ambient textures, solemn and majestic, 48khz",
                "seconds_total": 30, # 設定生成的總長度
                "steps": 50          # 增加生成步數以提高音質
            }

            try:
                # 這次我們用 json=payload，這會自動處理 JSON 編碼
                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    st.balloons()
                    st.success("✅ 生成成功！實驗 1.0 跑通了。")
                    st.audio(response.content, format="audio/mpeg")
                    
                    st.download_button(
                        label="💾 下載這段聲音遺產",
                        data=response.content,
                        file_name="majesty_sound_v1.mp3",
                        mime="audio/mpeg"
                    )
                else:
                    # 如果依舊出錯，打印出詳細的 JSON 錯誤信息
                    st.error(f"API 拒絕了請求 (Status: {response.status_code})")
                    try:
                        st.json(response.json())
                    except:
                        st.text(response.text)
                    
            except Exception as e:
                st.error(f"系統異常: {str(e)}")

st.divider()
st.caption("ZENG JIAJING | 2026-04-10 凌晨 實戰紀錄")
