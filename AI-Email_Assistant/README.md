# AI Email Assistant V1.5 企业版
基于 Python + Tkinter + OpenAI 实现的智能邮件生成工具，适配日常办公全场景。

## 功能介绍
1. 多类型邮件模板：商务/投诉/面试感谢/请假/催款/客户跟进/会议邀请
2. 智能Prompt自动切换
3. 多格式导出：TXT / Markdown / Word
4. 完善的API异常捕获与GUI弹窗提示
5. 多线程优化，界面不卡顿，防重复点击

## 项目结构
AI_Email_Assistant/
├── main.py # 主程序 + GUI 界面
├── prompts.py # 邮件提示词模板
├── ai_helper.py # AI 接口调用 + 异常处理
├── export_docx.py # Word 导出功能
├── requirements.txt # 依赖清单
├── README.md # 项目说明
├── error_bank.md # 问题排查日志
├── output/ # 导出文件目录
└── screenshots/ # 项目截图目录

## 运行方式
python main1.5.py

## 技术亮点
Tkinter Combobox 下拉组件使用
提示词工程（Prompt 模板化管理）
模块化代码拆分，易维护扩展
try-except 全局异常捕获
多线程解决 GUI 卡顿问题
办公常用文件格式导出实现

## 🛠️ 项目核心设计要点
为了保证程序的稳定性与用户体验，本项目采用了以下关键设计：
1.  **模块化架构**：按功能拆分文件，提升代码可维护性；
2.  **多线程处理**：网络请求与耗时操作放入子线程，避免GUI卡顿；
3.  **主线程安全更新**：通过 `root.after()` 实现跨线程UI更新；
4.  **防重复点击机制**：通过按钮状态控制避免用户误操作；
5.  **全局异常捕获**：关键接口调用添加异常处理，提升程序鲁棒性；
6.  **编码与文件处理**：统一UTF-8编码，防止中文乱码，兼容主流办公格式导出。