# ♈️ Aries: ArXiv Research Intelligent Efficient Summary
## Arxiv Paper to Feishu


<p align="center">
  <img src="assert/ARIES.webp" alt="ARIES Logo" width="200"/>
</p>



[中文文档](README_zh.md)
---

<p align="center">
  <a href=""><img src="https://img.shields.io/badge/Aries-v1.0-darkcyan"></a>
  <a href='https://github.com/LAMDASZ-ML/Aries'><img src='https://img.shields.io/badge/Project-Page-Green'></a>
  <a href=""><img src="https://img.shields.io/github/stars/LAMDASZ-ML/Aries?color=4fb5ee"></a>
  <a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FLAMDASZ-ML%2FAries&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visitors&edge_flat=false"/></a>
  <a href=""><img src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
  <a href=""><img src="https://img.shields.io/github/last-commit/LAMDASZ-ML/Aries?color=blue"></a>
</p>


## 🎉 Introduction

A tool that automatically fetches the latest LLM-related papers from arXiv and pushes them through Feishu bots. The bot uses Deepseek AI for intelligent filtering and summarization, helping you stay up-to-date with the latest research developments.

---

## ✨ Features

- 🤖 **Auto Paper Fetching**: Scrapes the latest LLM-related papers from arXiv.
- 🧠 **Smart Filtering & Summarization**: Uses Deepseek AI for high-quality filtering and summarization.
- 📱 **Multi-bot Support**: Configure multiple Feishu bots to push to different groups.
- ⏰ **Scheduled Tasks**: Default push at 9 AM daily, customizable.
- ⚙️ **Flexible Configuration**: Customize paper types, filtering rules, and push methods via config file.
- 📊 **History Tracking**: Pushed papers are recorded in `paper_history.json` to avoid duplicates.

---

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables:
   - Create a `.env` file and fill in as follows:
     ```
     DEEPSEEK_API_KEY=your_deepseek_api_key
     WEBHOOK_URL_1=https://your_first_webhook_url
     WEBHOOK_URL_2=https://your_second_webhook_url
     ```

3. Configure `config.yaml` to customize paper types and filtering rules.

4. Run the script:
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration Guide

### Environment Variables

- `DEEPSEEK_API_KEY`: **Required**, for calling Deepseek API.
- `WEBHOOK_URL_[n]`: **Required**, Feishu bot webhook URLs, multiple can be configured.

### Configuration Details:

- **`paper_types`**: Define settings for each paper type.
  - **`enabled`**: Status, `true` to enable, `false` to disable.
  - **`search_query`**: arXiv search query, supports logical conditions and keyword combinations.
  - **`keywords`**: Keyword list for paper filtering.
  - **`prompt`**: Prompt for Deepseek to judge paper relevance, generated based on search_query and keywords. Can be modified.
  - **`max_papers`**: Maximum number of papers per push (default 5, customizable).

- **`general`**: Global configuration.
  - **`max_search_results`**: Maximum number of papers returned by search.
  - **`schedule_time`**: Daily scheduled task time (24-hour format).

---

## ❗ Important Notes

1. Ensure sufficient Deepseek API Key quota.
2. Feishu Webhook URLs should be obtained from bot settings in Feishu groups.
3. Recommended to deploy on a server for continuous operation.
4. New paper types can be added or existing configurations adjusted via `config.yaml`.

---

## ❓ FAQ

1. **API Call Failure**
   - Check if the Deepseek API Key is correct.
2. **Message Push Failure**
   - Verify if the Webhook URL is valid.
3. **Test Push**
   - Uncomment `agent.run()` in the `main` function to run directly.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/license/mit).
