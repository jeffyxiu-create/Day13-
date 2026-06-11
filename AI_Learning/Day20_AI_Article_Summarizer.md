# AI 文章摘要工具 Day20
基于 Python + Tkinter + OpenAI API 开发的长文章摘要提取工具。

## 功能介绍
1. 支持粘贴长文本/文章
2. AI 自动生成全文摘要
3. 智能提取核心关键词
4. 结果导出为 TXT / Markdown 格式
5. 完善输入校验 & API 异常捕获

## 技术栈
- Python
- Tkinter 桌面GUI
- OpenAI Chat API
- 文件读写

## 使用方法
1. 安装依赖：`pip install openai`
2. 替换代码内 OpenAI API Key
3. 运行 `Day20_AI_Article_Summarizer.py`
4. 粘贴文章 → 生成结果 → 选择导出格式

## 学习要点
- 长文本上下文窗口、Token 基础概念
- AI 信息压缩、结构化 Prompt 设计
- 桌面GUI 交互与文件导出
- 全局异常处理