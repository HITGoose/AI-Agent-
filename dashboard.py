import streamlit as st
import os
import time
from securag_engine import SecuRAG
from pdf_loader import load_pdf_to_chroma # 👈 复用我们昨天写的加载器
#前端页面展示 streamlit 缺点是每次都会从头跑一次代码到结尾


# --- 1. 页面配置 (Page Config) ---
st.set_page_config(
    page_title="SecuRAG Control Panel",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SecuRAG: 隐私优先的安全智能助手")
st.markdown("### Powered by Local Privacy & Hybrid Sanitization")

# --- 2. 初始化引擎 (Session State) ---
# Streamlit 每次点击都会刷新代码，所以要用 session_state 记住“机器人”
# 否则每问一句话它都要重启一次，太慢了
# session_state 是streamlit提供的用来存储的字典，但关闭网页就会清除之前的数据，相当于临时栈
if "bot" not in st.session_state:
    with st.spinner("正在启动安全引擎..."):
        st.session_state.bot = SecuRAG()
        st.success("引擎已就绪！")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. 侧边栏：知识投喂区 (Sidebar) ---
with st.sidebar:
    st.header("📂 知识库管理 (Ingestion)")
    
    # 文件上传组件
    uploaded_file = st.file_uploader("上传 PDF 文档", type=["pdf"])
    
    if uploaded_file and st.button("开始学习 (Ingest)"):
        with st.spinner("正在读取并切片..."):
            # 1. 先把文件存成临时的 temp.pdf
            temp_path = "temp_upload.pdf"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. 调用昨天的 pdf_loader 进行入库
            load_pdf_to_chroma(temp_path)
            
            # 3. 删掉临时文件
            os.remove(temp_path)
            
        st.success(f"✅ 已成功学习: {uploaded_file.name}")
        st.balloons() # 放个气球庆祝一下

# --- 4. 主界面：聊天窗口 (Chat Interface) ---

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("向 SecuRAG 提问..."):
    # 1. 显示用户的问题
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI 思考并回答
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 SecuRAG 正在思考 (检索 + 脱敏)...")
        
        # --- 核心调用 ---
        response = st.session_state.bot.chat(prompt)
        # ---------------
        
        # 3. 如果是安全拦截，显示红色警告！
        if "Security Alert" in response:
            message_placeholder.error(response) # 变红
        else:
            message_placeholder.markdown(response) # 正常显示
            
    # 4. 记入历史
    st.session_state.messages.append({"role": "assistant", "content": response})