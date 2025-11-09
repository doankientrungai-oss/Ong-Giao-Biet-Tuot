import streamlit as st

# --- Cấu hình trang ---
st.set_page_config(page_title="AI Studio App", layout="wide")

# --- Tiêu đề & hướng dẫn ---
st.title("🚀 Ứng dụng AI Studio của Thầy Trung")
st.write("""
Ứng dụng được nhúng trực tiếp từ Google AI Studio.
Nếu không hiển thị được, hãy kiểm tra lại quyền chia sẻ của app (đặt ở chế độ **Public** hoặc **Anyone with the link**).
""")

# --- Liên kết app gốc ---
ai_studio_url = "https://ai.studio/apps/drive/1tnQADEGoxLBpt1f-qqdIJ70KCPHK16s3"

# --- Nhúng app bằng iframe ---
st.components.v1.iframe(ai_studio_url, height=900, scrolling=True)
