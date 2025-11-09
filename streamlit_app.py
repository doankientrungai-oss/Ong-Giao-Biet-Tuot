import streamlit as st
import os
from google import genai
from google.genai import types

# ============================================================
# 🧩 BƯỚC 0: Thiết lập biến môi trường tạm thời (local)
# ============================================================
# Thầy chỉ cần nhập API key một lần ở đây cho mỗi lần chạy thử local.
# Khi triển khai lên Streamlit Cloud, có thể xóa đoạn này và dùng st.secrets["GEMINI_API_KEY"]

if "GEMINI_API_KEY" not in os.environ:
    st.sidebar.markdown("## 🔑 Thiết lập API Key (chạy local)")
    api_key_input = st.sidebar.text_input("Nhập GEMINI_API_KEY của bạn:", type="password")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.sidebar.success("✅ Đã thiết lập GEMINI_API_KEY tạm thời.")
    else:
        st.warning("⚠️ Vui lòng nhập API key để tiếp tục.")
        st.stop()

# ============================================================
# 🎨 CSS TÙY CHỈNH - FOOTER CỐ ĐỊNH
# ============================================================
st.markdown("""
<style>
    footer {visibility: hidden;}
    .custom-footer-container {
        position: fixed;
        bottom: 0px;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 5px 0;
        z-index: 999999;
        border-top: 1px solid #f0f2f6;
        text-align: center;
        font-size: 0.7em;
        color: grey;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🤖 BƯỚC 1: Khởi tạo Gemini Client (sử dụng biến môi trường)
# ============================================================
@st.cache_resource
def get_gemini_client():
    try:
        api_key = os.environ["GEMINI_API_KEY"]
        return genai.Client(api_key=api_key)
    except KeyError:
        st.error("❌ Không tìm thấy GEMINI_API_KEY trong biến môi trường.")
        st.stop()

client = get_gemini_client()

# ============================================================
# 🧠 BƯỚC 2: Cấu hình “Bộ não” và phiên trò chuyện
# ============================================================
if "chat_session" not in st.session_state:
    system_instruction = """
Bạn là "Ông Giáo Biết Tuốt" – trợ giảng học tập thông minh, thân thiện, kiên nhẫn.
Hỗ trợ học sinh THCS và THPT trong tất cả các môn học: Toán, Lý, Hóa, Văn, Anh, Sử, Địa, GDCD, Tin học, Công nghệ.
Giải thích từng bước, giúp học sinh hiểu bản chất, không làm thay hoàn toàn.
Luôn khích lệ, động viên, dùng ngôn ngữ tích cực và phù hợp lứa tuổi.
Trình bày công thức bằng LaTeX khi cần.
"""

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=1
    )

    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=config
    )

# ============================================================
# 💬 BƯỚC 3: Giao diện người dùng
# ============================================================
st.title("🎓 Ông giáo Biết tuốt")
st.caption("Xin chào em! Thầy sẽ giúp em học tốt hơn!")

st.markdown("---")
st.markdown("**Hãy nhập câu hỏi hoặc tải ảnh bài tập lên nhé!**")
st.markdown("---")

# ------------------------------------------------------------
# 📷 CHỨC NĂNG TẢI ẢNH
# ------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Tải ảnh bài tập (Toán, Lý, Hóa, Văn, Anh, Sử, Địa...)",
    type=["png", "jpg", "jpeg"],
    key="file_uploader"
)

image_part = None
image_bytes = None

if uploaded_file:
    image_bytes = uploaded_file.read()
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=uploaded_file.type)
    st.sidebar.image(image_bytes, caption="Ảnh bài tập đã tải lên", use_column_width=True)
    st.info("📸 Ảnh đã tải lên thành công. Hãy nhập câu hỏi để tôi giúp nhé!")

# ------------------------------------------------------------
# 🧾 HIỂN THỊ LỊCH SỬ CHAT
# ------------------------------------------------------------
for message in st.session_state.chat_session.get_history():
    role = "👩‍🎓 Học sinh" if message.role == "user" else "🧑‍🏫 Gia sư"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# ------------------------------------------------------------
# ✏️ HỘP NHẬP LIỆU
# ------------------------------------------------------------
if prompt := st.chat_input("Nhập câu hỏi của em (ví dụ: Giải bài toán, phân tích bài thơ...)"):
    contents = [prompt]

    if image_part:
        contents.insert(0, image_part)
        with st.chat_message("👩‍🎓 Học sinh"):
            st.markdown("**Bài tập có ảnh đính kèm:**")
            st.image(image_bytes, width=150)
            st.markdown(prompt)
    else:
        st.chat_message("👩‍🎓 Học sinh").markdown(prompt)

    with st.spinner("🤖 Gia sư đang suy nghĩ..."):
        try:
            response = st.session_state.chat_session.send_message(contents)
            with st.chat_message("🧑‍🏫 Gia sư"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Lỗi: {e}")

# ============================================================
# 📊 FOOTER / THÔNG TIN
# ============================================================
st.divider()
st.markdown(
    """
    <div class="custom-footer-container">
        Ứng dụng được phát triển bởi <b>Thầy Đoàn Kiên Trung</b> – Zalo: 0909629947
    </div>
    """,
    unsafe_allow_html=True
)
