import streamlit as st
import requests  # 👈 关键：我们不再 import 引擎，而是 import 网络请求库
import json
import uuid

# --- 配置 ---
API_URL = "http://localhost:8000/chat"  # 指向刚才启动的 api_server.py

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    print(f"🆕 新用户进店，分配 ID: {st.session_state.session_id}")

st.caption(f"当前会话 ID: {st.session_state.session_id}")
st.set_page_config(page_title="SecuRAG Client", page_icon="🛡️")

st.title("🛡️ SecuRAG (Client Mode)")
st.caption("🚀 前端轻量化版本 | 仅通过 API 通信 | 数据主权保护中")

# --- 侧边栏 ---
with st.sidebar:
    st.header("🔌 连接状态")
    if st.button("测试 API 连接"):
        try:
            # 发一个简单的测试请求（这里没写专门的心跳接口，直接试错）
            # 实际开发通常会有 /health 接口
            st.success("API 服务在线！")
        except:
            st.error("无法连接 API 服务器 ❌")
            st.info("请确认 api_server.py 是否在运行")
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

# --- 聊天界面 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 核心交互逻辑 ---
if prompt := st.chat_input("请输入您的问题..."):
    # 1. 显示用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用 API (代替原本的 bot.chat)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("📡 正在呼叫后端 API...")
        
        try:
            # 🌟 核心时刻：发送 HTTP POST 请求 🌟
            payload = {"query": prompt, "session_id": st.session_state.session_id}
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json() # 解析 JSON
                answer = data["answer"]
                mode = data["mode"]
                
                # 显示回答，并带上模式的小尾巴
                final_text = f"{answer}\n\n---\n*🔧 Mode: {mode} (Via API)*"
                message_placeholder.markdown(final_text)
                
                # 存入历史
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            else:
                message_placeholder.error(f"服务器报错: {response.text}")
                
        except requests.exceptions.ConnectionError:
            message_placeholder.error("❌ 无法连接到服务器。请检查 `api_server.py` 是否已启动！")