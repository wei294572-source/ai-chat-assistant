"""
AI对话核心模块
支持多轮对话记忆和上下文管理
"""

import anthropic
from typing import List, Dict
import os


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

        # 延迟初始化客户端，避免启动时因缺少环境变量而失败
        self.client = None
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.conversation_history = []

        # 获取 API Key
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def _init_client(self) -> None:
        """延迟初始化 Anthropic 客户端"""
        if self.client is None:
            api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("请设置 ANTHROPIC_API_KEY 环境变量")
            self.client = anthropic.Anthropic(api_key=api_key)

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

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text
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
