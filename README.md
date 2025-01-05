# Arxiv Paper to Feishu

一个自动获取arXiv最新LLM相关论文并通过飞书机器人推送的工具。该机器人会使用Deepseek AI对论文进行智能筛选和总结，让您快速了解最新研究动态。

## 功能特点

- 🤖 自动从arXiv获取最新的LLM相关论文
- 🧠 使用Deepseek AI进行论文筛选和智能总结
- 📱 支持多个飞书机器人同时推送
- ⏰ 支持定时任务（默认每天早上9点推送）
- ⚙️ 支持通过配置文件自定义论文类型和筛选规则

## 安装要求

- Python 3.10+
- pip包管理器

## 快速开始

1. 安装依赖：
```

## 配置说明

### 环境变量配置
- `DEEPSEEK_API_KEY`：必填，用于调用Deepseek API
- `WEBHOOK_URL_[n]`：必填，飞书机器人的webhook地址，支持配置多个

### 论文类型配置
在`config.yaml`中可以配置多个论文类型，每个类型包含：
- `enabled`：是否启用该类型
- `search_query`：arXiv搜索关键词
- `keywords`：初步筛选的关键词列表
- `prompt`：用于判断论文相关性的Deepseek提示词
- `max_papers`：该类型最大论文数量
- `title`：推送消息的标题

### 通用配置
- `max_search_results`：初始搜索的最大结果数
- `schedule_time`：定时推送时间（24小时制）
- `summary_prompt`：论文总结的提示词模板

## 注意事项

1. 确保Deepseek API key有足够的额度
2. 飞书webhook地址需要在飞书群机器人设置中获取
3. 建议部署在服务器上持续运行
4. 可以通过修改config.yaml添加新的论文类型或调整现有配置

## 常见问题

1. 如遇到API调用失败，请检查Deepseek API key是否正确
2. 如消息推送失败，请确认webhook地址是否有效
3. 想要立即测试，可以取消main函数中的schedule注释，直接运行agent.run()

## License

MIT License