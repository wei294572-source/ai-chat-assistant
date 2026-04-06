# AI客服对话应用

> 一个基于Anthropic Claude API的智能客服对话应用，支持多轮对话记忆。

## 📋 项目简介

本项目是一个面向客服行业的AI对话应用程序，使用Python和Streamlit构建，集成Anthropic Claude API实现智能对话。应用支持多轮对话记忆，能够保持上下文连贯性，为用户提供专业、高效的客服服务。

## ✨ 核心功能

- **智能对话**: 基于Claude-3.5模型的高质量对话体验
- **多轮记忆**: 支持连续对话，自动维护对话上下文
- **客服专用**: 针对客服场景优化的系统提示词
- **简洁界面**: 使用Streamlit构建的现代化Web界面
- **对话统计**: 实时显示对话消息统计信息
- **快速重置**: 一键清除对话历史，重新开始

## 🏗️ 技术架构

```
ai_chat_app/
├── app.py              # Streamlit Web应用主程序
├── chat_core.py        # AI对话核心模块
├── requirements.txt    # Python依赖包
├── .env.example       # 环境变量示例
├── .gitignore         # Git忽略文件
└── README.md          # 项目说明文档
```

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| Streamlit | 1.35.0 | Web应用框架 |
| Anthropic SDK | 0.34.2 | Claude API集成 |
| python-dotenv | 1.0.1 | 环境变量管理 |

## 🚀 快速开始

### 1. 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 2. 安装步骤

#### 2.1 克隆或下载项目

```bash
cd ai_chat_app
```

#### 2.2 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

#### 3.1 获取Anthropic API密钥

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册或登录账号
3. 在 API Keys 页面创建新的API密钥

#### 3.2 配置环境变量

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入你的API密钥
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 4. 启动应用

```bash
streamlit run app.py
```

应用将自动在浏览器中打开，默认地址为：`http://localhost:8501`

## 📱 使用指南

### 基本操作

1. **发送消息**: 在输入框中输入问题，按Enter键或点击发送
2. **查看回复**: AI回复会实时显示在对话区域
3. **连续对话**: 支持多轮对话，AI会记住上下文
4. **查看统计**: 侧边栏显示对话统计信息
5. **重置对话**: 点击"清除对话历史"按钮重新开始

### 客服场景示例

| 用户问题 | AI回复示例 |
|---------|-----------|
| 如何退款？ | 您好，关于退款问题，您可以通过以下方式申请退款... |
| 产品价格？ | 您好，我们的产品定价如下：基础版99元/月... |
| 找不到订单？| 您好，请提供订单号或注册邮箱，我来帮您查询... |

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|-------|------|-------|
| `ANTHROPIC_API_KEY` | Anthropic API密钥（必填） | - |
| `ANTHROPIC_MODEL` | Claude模型名称 | claude-3-5-sonnet-20241022 |

### 可用模型

- `claude-3-5-sonnet-20241022` (推荐，平衡性能和成本)
- `claude-3-opus-20240229` (最强性能，成本较高)
- `claude-3-haiku-20240307` (快速响应，成本最低)

## 📦 项目文件说明

| 文件 | 说明 |
|------|------|
| `app.py` | Streamlit Web应用主入口 |
| `chat_core.py` | 对话管理核心类，处理API调用和上下文 |
| `requirements.txt` | Python依赖包列表 |
| `.env.example` | 环境变量配置示例 |
| `.gitignore` | Git版本控制忽略文件 |

## 🐛 常见问题

### Q1: 提示"请设置 ANTHROPIC_API_KEY 环境变量"

**A**: 请确保已正确配置 `.env` 文件，并且API密钥有效。

### Q2: 应用无法启动

**A**: 检查Python版本是否为3.8+，并确认依赖包已正确安装。

### Q3: AI回复很慢

**A**: 网络延迟可能导致响应慢，可以尝试切换到 `claude-3-haiku` 模型以获得更快响应。

### Q4: 如何自定义系统提示词？

**A**: 编辑 `chat_core.py` 文件中的 `system_prompt` 变量，可以修改AI的角色和行为。

## 📊 对话管理

### ConversationManager 类

`chat_core.py` 中的 `ConversationManager` 类负责：

- 管理对话历史记录
- 调用Anthropic API获取AI回复
- 维护对话上下文
- 提供对话统计功能

### 主要方法

| 方法 | 说明 |
|------|------|
| `add_user_message()` | 添加用户消息 |
| `add_assistant_message()` | 添加助手消息 |
| `get_response()` | 获取AI响应 |
| `reset_conversation()` | 重置对话历史 |
| `get_conversation_summary()` | 获取对话摘要 |

## 🔒 安全建议

1. **保护API密钥**: 不要将 `.env` 文件提交到版本控制系统
2. **限制输入长度**: 在生产环境中建议对用户输入进行长度限制
3. **内容过滤**: 根据业务需求添加内容过滤机制
4. **速率限制**: 实施API调用速率限制以控制成本

## 📄 许可证

本项目仅供学习和演示使用。

## 🤝 贡献

欢迎提交问题和改进建议！

---

**开发者**: Claude Code AI
**创建日期**: 2026-03-31
