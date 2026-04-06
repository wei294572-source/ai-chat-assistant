"""
AI对话核心模块
支持多轮对话记忆和上下文管理
使用 Groq API
"""

import os
import httpx


class ConversationManager:
    """对话管理器，处理多轮对话的上下文和记忆"""

    def __init__(self, system_prompt: str = None):
        """
        初始化对话管理器

        Args:
            system_prompt: 系统提示词，定义AI的角色和行为
        """
        # 客服行业专用系统提示
        self.system_prompt = system_prompt or """你是一位专业的客服AI助手，具有以下特点：

1. 专业友好：以礼貌、专业、耐心的态度回答用户问题
2. 高效准确：快速理解用户需求，提供准确的解决方案
3. 知识丰富：熟悉产品功能、服务流程、常见问题解答
4. 同理心强：理解用户情绪，提供有温度的服务
5. 问题引导：当问题不够明确时，主动引导用户提供更多信息

请用中文回复，保持专业且亲切的语气。"""

        # Groq 配置
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
        self.model = os.getenv("GROQ_MODEL", "llama3-70b-8192")
        self.conversation_history = []
        self._http_client = None

    def _init_client(self) -> None:
        """延迟初始化 Groq 客户端"""
        if self._http_client is None:
            if not self.api_key:
                raise ValueError("请设置 GROQ_API_KEY 环境变量")
            # 使用 httpx 调用 Groq API
            self._http_client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=60.0
            )

    def add_user_message(self, message: str) -> None:
        """添加用户消息到对话历史"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message: str) -> None:
        """添加助手消息到对话历史"""
        self.conversation_history.append({
            "role": "assistant",
            "content": message
        })

    def get_response(self) -> str:
        """
        获取AI响应

        Returns:
            AI的回复内容
        """
        try:
            # 延迟初始化客户端
            self._init_client()

            # Groq API 使用 /chat/completions 端点
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "max_tokens": 2048,
                "temperature": 0.7
            }

            # 如果有 system prompt，添加到 messages 开头
            if self.system_prompt:
                payload["messages"] = [{"role": "system", "content": self.system_prompt}] + self.conversation_history

            response = self._http_client.post("/chat/completions", json=payload)
            response.raise_for_status()

            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]
            self.add_assistant_message(assistant_message)

            return assistant_message

        except Exception as e:
            return f"抱歉，获取回复时出现错误：{str(e)}"

    def reset_conversation(self) -> None:
        """重置对话历史"""
        self.conversation_history = []

    def get_conversation_summary(self) -> Dict:
        """
        获取对话摘要

        Returns:
            包含对话统计信息的字典
        """
        user_messages = [m for m in self.conversation_history if m["role"] == "user"]
        assistant_messages = [m for m in self.conversation_history if m["role"] == "assistant"]

        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages)
        }
