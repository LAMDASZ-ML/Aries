# ♈️ Aries: ArXiv Research Intelligent Efficient Summary
## Arxiv 论文推送到飞书

<p align="center">
  <img src="assert/ARIES.webp" alt="ARIES Logo" width="200"/>
</p>



[English](README.md)

<p align="center">
  <a href=""><img src="https://img.shields.io/badge/Aries-v1.0-darkcyan"></a>
  <a href='https://github.com/LAMDASZ-ML/Aries'><img src='https://img.shields.io/badge/Project-Page-Green'></a>
  <a href=""><img src="https://img.shields.io/github/stars/LAMDASZ-ML/Aries?color=4fb5ee"></a>
  <a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FLAMDASZ-ML%2FAries&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visitors&edge_flat=false"/></a>
  <a href=""><img src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
  <a href=""><img src="https://img.shields.io/github/last-commit/LAMDASZ-ML/Aries?color=blue"></a>
</p>

## 介绍

一个自动获取 arXiv 最新 LLM 相关论文，并通过飞书机器人推送的工具。该机器人使用 Deepseek AI 对论文进行智能筛选和总结，帮助您快速了解最新研究动态。

---

## 功能特点

- 🤖 **自动获取最新论文**：从 arXiv 抓取最新的 LLM 相关论文。
- 🧠 **智能筛选与总结**：使用 Deepseek AI 提供高质量的筛选和总结。
- 📱 **支持多机器人推送**：可配置多个飞书机器人，分别推送到不同群组。
- ⏰ **定时任务支持**：默认每天早上 9 点推送，支持自定义。
- ⚙️ **灵活配置**：通过配置文件自定义论文类型、筛选规则和推送方式。
- 📊 **历史记录**：推送过的论文会记录在 `paper_history.json` 文件中，下次推送时会跳过。

---

## 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 配置环境变量：
   - 创建一个 `.env` 文件，按照下方样例填写：
     ```
     DEEPSEEK_API_KEY=your_deepseek_api_key
     WEBHOOK_URL_1=https://your_first_webhook_url
     WEBHOOK_URL_2=https://your_second_webhook_url
     ```

3. 配置 `config.yaml`，自定义论文类型和筛选规则。

4. 启动脚本：
   ```bash
   python main.py
   ```

---

## 配置说明

### 环境变量配置

- `DEEPSEEK_API_KEY`：**必填**，用于调用 Deepseek API。
- `WEBHOOK_URL_[n]`：**必填**，飞书机器人的 Webhook 地址，可配置多个。

#### 配置说明：

- **`paper_types`**：定义每种论文类型的具体设置。
  - **`enabled`**：启用状态，`true` 表示启用，`false` 表示禁用。
  - **`search_query`**：在 arXiv 上使用的搜索查询，支持逻辑条件和关键词组合。
  - **`keywords`**：用于筛选论文的关键词列表。
  - **`prompt`**：使用 Deepseek 或其他工具判断论文相关性的提示词，已经根据search_query和keywords生成。用户可以自行修改。
  - **`max_papers`**：单次推送的最大论文数量（默认 5，可自行修改）。

- **`general`**：全局配置。
  - **`max_search_results`**：搜索返回的最大论文数量。
  - **`schedule_time`**：每天定时任务运行时间（24 小时制）。

---

## 注意事项

1. 确保 Deepseek API Key 额度充足。
2. 飞书 Webhook 地址需要在飞书群中通过机器人设置获取。
3. 建议部署在服务器上持续运行。
4. 可通过编辑 `config.yaml` 添加新的论文类型或调整现有配置。

---

## 常见问题

1. **API 调用失败**
   - 请检查 Deepseek API Key 是否正确。
2. **消息推送失败**
   - 请确认 Webhook 地址是否有效。
3. **测试推送**
   - 可取消 `main` 函数中的 `schedule` 注释，直接运行 `agent.run()`。

---

## 📝 待办事项

- 📚 文章收集与管理
  - [x] arXiv论文自动抓取
  - [ ] 文章历史记忆存储
  - [ ] 相关论文关联分析
  - [ ] 论文分类归档系统

- 🔍 文章智能处理
  - [x] Auto Summary: 论文自动摘要
  - [ ] Auto Review: 论文自动点评
  - [ ] Auto Survey: 领域综述生成

- 📢 多平台推送
  - [x] 飞书机器人推送
  - [ ] 微信机器人集成
  - [ ] 小红书内容发布

--- 

## License

本项目使用 [MIT License](https://opensource.org/license/mit)。
