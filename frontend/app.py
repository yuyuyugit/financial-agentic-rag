import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="Financial Agentic RAG", layout="wide")

# Sidebar - System Status
with st.sidebar:
    st.header("系统状态")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ 后端已连接")
        else:
            st.error("❌ 后端离线")
    except:
        st.error("❌ 后端离线")

    st.divider()
    st.subheader("查询类型说明")
    st.markdown("🟢 **简单查询**：直接查询用户资产、持仓、股价等")
    st.markdown("🔵 **复杂查询**：需要 Agent 分析的多步骤问题")

# Main area
st.title("🤖 Financial Agentic RAG Demo")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "query_type" in message:
            if message["query_type"] == "simple":
                st.caption("🟢 简单查询")
            elif message["query_type"] == "complex":
                st.caption("🔵 Agent 分析")

# Chat input
user_input = st.chat_input("输入您的问题...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from backend
    with st.spinner("处理中..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"query": user_input},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()

            answer = data.get("answer", "无法获取答案")
            query_type = data.get("query_type", "unknown")

            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "query_type": query_type
            })

            with st.chat_message("assistant"):
                st.markdown(answer)
                if query_type == "simple":
                    st.caption("🟢 简单查询")
                elif query_type == "complex":
                    st.caption("🔵 Agent 分析")

        except requests.exceptions.ConnectionError:
            st.error("❌ 无法连接到后端服务")
        except requests.exceptions.Timeout:
            st.error("❌ 请求超时")
        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")
