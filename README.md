# Arxiv LLM Paper Bot

一个自动获取arXiv最新LLM相关论文并通过飞书机器人推送的工具。该机器人会使用Deepseek AI对论文进行简单总结，让您快速了解最新研究动态。

## 功能特点

- 🤖 自动从arXiv获取最新的LLM相关论文
- 🧠 使用Deepseek AI进行论文摘要的智能总结
- 📱 通过飞书机器人推送消息
- ⏰ 支持定时任务（默认每天早上9点推送）

## 安装要求

- Python 3.7+
- pip包管理器

## 使用方式

- 配置 .env
- python arxiv_bot.py