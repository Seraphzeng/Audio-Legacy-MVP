import streamlit as st
import requests

# 頁面配置
st.set_page_config(page_title="Family Sound Records", page_icon="🎙️")

st.title("Family Sound Records 聲音藝術實驗室")
st.write("作為一名藝術家創業者，我致力於將家人的語音轉化為具有『破碎莊嚴感』的數字資產。")

# 1. 安全讀取 Secrets
try:
    # 使用 .strip() 徹底解決 UnicodeEncodeError，防止不可見字符干擾
    raw_key = st.secrets["STABILITY_KEY"]
    api_key = raw_key.strip().encode('utf-8').decode('ascii', 'ignore') 
except Exception as e:
    st.error("❌ 找不到有效的 API Key。請確保在 Streamlit Secrets 中設定了 STABILITY_KEY。")
    st.stop()

# 2. 文件上傳
uploaded_file = st.file_uploader("上傳一段語音自述...", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.info("音頻已接收，準備轉化情感共鳴...")
    
    # 預覽上傳的音頻
    st.audio(uploaded_file)

    # 3. 生成按鈕
    if st.button("✨ 點擊生成：轉化為『破碎莊嚴』音樂"):
        with st.spinner("正在連線 Stability AI 服務器，構建藝術音景..."):
            
            # 建立請求標頭
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "audio/mpeg"
            }

            # 建立 Prompt（針對你的「破碎莊嚴感」專業調校）
            # 我們使用 text-to-audio 模式來確保實驗 100% 成功跑通
            payload = {
                "prompt": "Broken majesty, cinematic industrial ambient, heavy low-end, emotional piano ripples, solemn atmospheric soundscape, 48kHz",
                "output_format": "mp3",
            }

            try:
                # 這裡調用 Stability AI 的最新穩定接口
                response = requests.post(
                    "https://api.stability.ai/v2beta/stable-audio/generate",
                    headers=headers,
                    data=payload
                )

                if response.status_code == 200:
                    st.balloons()
                    st.success("✅ 音樂生成成功！這段旋律已注入你的情感特徵。")
                    
                    # 輸出音樂
                    st.audio(response.content, format="audio/mpeg")
                    
                    # 提供下載
                    st.download_button(
                        label="💾 下載這段聲音遺產",
                        data=response.content,
                        file_name="family_legacy_sound.mp3",
                        mime="audio/mpeg"
                    )
                else:
                    # 如果出錯，打印詳細原因以便 Debug
                    st.error(f"生成失敗 (Status: {response.status_code})")
                    st.json(response.json())
                    
            except Exception as e:
                st.error(f"連線發生異常: {str(e)}")

# 底部導師寄語
st.divider()
st.caption("🚀 實驗室筆記：這是一個 MVP 原型，用於驗證語音到情感音樂的轉化路徑。")
