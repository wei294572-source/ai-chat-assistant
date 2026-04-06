"""
AI客服对话应用 - Streamlit Web界面
"""

import streamlit as st
from dotenv import load_dotenv
import os
from chat_core import ConversationManager

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="AI客服助手",
    page_icon="🤖",
    layout="centered"
)


def main():
    """主应用函数"""

    # 检查API Key
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("⚠️ 请设置 ANTHROPIC_API_KEY 环境变量")
        st.info("请在项目目录下创建 .env 文件，并添加你的API Key")
        st.code("ANTHROPIC_API_KEY=your_api_key_here")
        return

    # 初始化session state
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
        st.session_state.messages = []
        # 添加欢迎消息
        welcome_msg = """您好！我是AI客服助手，很高兴为您服务！👋

我可以帮您解答以下类型的问题：
• 产品功能咨询
• 使用问题解决
• 服务流程说明
• 常见问题解答

请随时告诉我您的需求，我会尽力为您提供帮助！"""
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    # 页面标题
    st.title("🤖 AI客服助手")
    st.markdown("---")

    # 对话历史显示
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 用户输入区域
    if prompt := st.chat_input("请输入您的问题..."):
        # 添加用户消息到界面
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 添加用户消息到对话管理器
        st.session_state.conversation_manager.add_user_message(prompt)

        # 显示"正在回复"
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                # 获取AI响应
                response = st.session_state.conversation_manager.get_response()
                st.markdown(response)

        # 添加AI回复到消息历史
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 侧边栏 - 控制面板
    with st.sidebar:
        st.header("⚙️ 控制面板")

        # 对话统计
        st.subheader("对话统计")
        summary = st.session_state.conversation_manager.get_conversation_summary()
        st.metric("消息总数", summary["total_messages"])
        st.metric("用户消息", summary["user_messages"])
        st.metric("AI回复", summary["assistant_messages"])

        # 清除对话
        st.subheader("操作")
        if st.button("🗑️ 清除对话历史", type="secondary"):
            st.session_state.conversation_manager.reset_conversation()
            st.session_state.messages = []
            # 重新添加欢迎消息
            welcome_msg = """您好！我是AI客服助手，很高兴为您服务！👋

请问有什么可以帮助您的？"""
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
            st.rerun()

        # 使用说明
        st.subheader("ℹ️ 使用说明")
        st.markdown("""
        1. 在输入框中输入您的问题
        2. 按Enter键或点击发送
        3. AI会基于对话历史理解您的需求
        4. 支持多轮连续对话
        5. 点击"清除对话历史"可重新开始
        """)


if __name__ == "__main__":
    main()
