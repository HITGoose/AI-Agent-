import streamlit as st
import requests
import uuid
import time # 用来模拟一点点延迟，让动画更好看

# --- 1. 页面基本配置 ---
st.set_page_config(
    page_title="SecuRAG 防御控制台",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 配置后端 API 地址
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/chat"

# --- 2. 初始化会话 ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "您好！我是 **SecuRAG** 安全卫士。\n\n当前系统运行在 **🔒 本地隐私模式**。\n我会对您的每一次输入进行 **Regex + AI** 双重安全审计。"}
    ]

# --- 3. 侧边栏 (控制中心) ---
with st.sidebar:
    st.title("🛡️ SecuRAG Console")
    st.markdown("---")
    
    st.subheader("System Status")
    # 🔥 真实的连接检查逻辑
    # 创建两列，用来放指示灯
    col1, col2 = st.columns([1, 4])
    
    try:
        # 尝试 ping 后端的 /health 接口，超时设置短一点(1秒)，免得卡顿
        health_res = requests.get(f"{BASE_URL}/health", timeout=3)
        
        if health_res.status_code == 200:
            # ✅ 活的：显示绿灯
            st.success("🟢 API Server: Online")
            # 简单起见，API 活了我们假设 DB 也连上了 (通常 API 启动时连不上 DB 会报错退出)
            st.success("🟢 Vector DB: Connected")
        else:
            # ⚠️ 半死不活：状态码不对
            st.error(f"🔴 API Error: {health_res.status_code}")
            st.error("🔴 Vector DB: Unknown")
            
    except requests.exceptions.ConnectionError:
        # ❌ 死的：完全连不上
        st.error("🔴 API Server: Offline")
        st.error("🔴 Vector DB: Disconnected")
        st.caption("⚠️ 请检查 `api_server.py` 是否运行")

    st.info(f"🔑 Session ID: `{st.session_state.session_id}`")
    
    st.markdown("---")
    # 🔥 新增：知识库管理区
    st.subheader("📚 Knowledge Base")
    
    # 文件上传器
    uploaded_file = st.file_uploader("Upload Research Paper", type=["pdf"])
    
    if uploaded_file is not None:
        # 显示上传按钮
        if st.button("📥 Ingest to RAG"):
            with st.spinner("正在读取并向量化 (Vectorizing)..."):
                try:
                    # 1. 准备发给后端的包裹
                    # multipart/form-data 格式
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    
                    # 2. 发送请求给刚才写的 /upload 接口
                    # 注意：上传文件不需要 json=payload，而是 files=files
                    response = requests.post(f"{BASE_URL}/upload", files=files, timeout=300)
                    
                    # 3. 处理结果
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("status") == "success":
                            st.success(f"✅ {data['msg']}")
                        else:
                            st.error(f"❌ 入库失败: {data['msg']}")
                    else:
                        st.error(f"Server Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

    st.markdown("---")
    current_temp = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.1 )
# 渲染历史消息
for msg in st.session_state.messages:
    # 根据是否是警告，决定用什么颜色渲染
    if "Security Alert" in msg["content"] or "Request denied" in msg["content"]:
        with st.chat_message(msg["role"], avatar="🛡️"):
            st.error(msg["content"], icon="🚨") # 红色警报框
    else:
        # 普通消息
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 显示 AI 回答 (带加载动画)
    # --- 5. 处理输入 ---
if prompt := st.chat_input("请输入问题..."):
    # 显示用户提问
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 显示 AI 回答 (带加载动画)
    with st.chat_message("assistant", avatar="🛡️"):
        
        # [修改点 1] 初始化暂存变量 (为了把结果带出缩进块)
        final_answer = ""
        is_blocked = False
        error_msg = ""

        # 创建一个状态容器
        with st.status("🔍 正在进行多层安全审计...", expanded=True) as status:
            try:
                st.write("Checking Deterministic Rules (Regex)...")
                time.sleep(0.3) 
                st.write("Auditing via AI Firewall (DeepSeek-R1)...")
                time.sleep(0.3) 
                st.write("Routing to Knowledge Base...")
                
                # 发送请求
                payload = {
                    "query": prompt, 
                    "session_id": st.session_state.session_id, 
                    "temperature": current_temp
                }
                response = requests.post(API_URL, json=payload, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    # [修改点 2] 这里只赋值，不显示！
                    final_answer = data.get("answer", "")
                    
                    # 判断是否被拦截
                    is_blocked = "Security Alert" in final_answer or "Request denied" in final_answer
                    
                    if is_blocked:
                        # 拦截了：状态栏变红
                        status.update(label="❌ 威胁已拦截 (Threat Blocked)", state="error", expanded=False)
                    else:
                        # 通过了：状态栏变绿，并自动收起
                        status.update(label="✅ 安全检查通过 (Safe)", state="complete", expanded=False)
                else:
                    status.update(label="⚠️ API Server Error", state="error")
                    error_msg = f"Server returned {response.status_code}"
                    
            except Exception as e:
                status.update(label="❌ Connection Failed", state="error")
                error_msg = str(e)

        # [修改点 3] 关键！这里【取消缩进】了！
        # 此时已经跳出了 with st.status 的管辖范围，内容会显示在折叠框的【下面】
        
        if error_msg:
            st.error(error_msg)
        
        elif final_answer:
            if is_blocked:
                # 如果是被拦截的，显示大红框
                st.error(final_answer, icon="🚨")
            else:
                # 如果是正常的，直接显示文字 (这样就不用点开折叠框了！)
                st.markdown(final_answer)
                # 加个小注脚增加专业感
                st.caption(f"🔧 Temp: {current_temp} | Mode: Local Privacy")

            # 最后再存入历史记录
            st.session_state.messages.append({"role": "assistant", "content": final_answer})