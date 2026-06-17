# File_Organizer_Assistant V2.0 企业级文件自动归档助手
## 项目简介
基于Python Tkinter开发的可视化文件整理工具，面向办公、企业文档归档场景，支持三种自动分类模式，配置化规则管理，内置日志、CSV报表、重复文件检测，完整工程化结构，可直接用于作品集面试展示。

## 核心功能
- ✅ 按文件类型自动分类（配置文件自定义后缀规则，无需修改代码）
- ✅ 按文件修改日期归档（自动生成 年-月 目录）
- ✅ 按文件体积大小分层管理 Small/Medium/Large
- ✅ 重复文件扫描检测
- ✅ 操作日志持久化存储
- ✅ 整理结果导出CSV统计报表
- ✅ 可视化GUI单选切换分类模式

## 项目目录架构
# File_Organizer_Assistant V2.0 企业级文件自动归档助手
## 项目简介
基于Python Tkinter开发的可视化文件整理工具，面向办公、企业文档归档场景，支持三种自动分类模式，配置化规则管理，内置日志、CSV报表、重复文件检测，完整工程化结构，可直接用于作品集面试展示。

## 核心功能
- ✅ 按文件类型自动分类（配置文件自定义后缀规则，无需修改代码）
- ✅ 按文件修改日期归档（自动生成 年-月 目录）
- ✅ 按文件体积大小分层管理 Small/Medium/Large
- ✅ 重复文件扫描检测
- ✅ 操作日志持久化存储
- ✅ 整理结果导出CSV统计报表
- ✅ 可视化GUI单选切换分类模式

## 项目目录架构
File_Organizer_Assistant/
├── main.py # GUI 主程序入口
├── organizer.py # 核心分类逻辑
├── report.py # CSV 报表导出
├── duplicate_checker.py # 重复文件检测
├── config/
│ └── config.json # 全局分类配置文件
├── logs/ # 运行日志存储
├── reports/ # CSV 报表输出目录
├── screenshots/ # 项目截图
├── demo/ # 演示视频
└── README.md

## 运行环境
Python 3.8+
内置库：tkinter / os / json / shutil / datetime 无需额外pip安装

## 使用教程
1. 克隆仓库
```bash
git clone xxx你的github仓库地址
cd File_Organizer_Assistant