import os

def create_test_files():
    # 测试文件夹路径（默认在桌面创建）
    desktop_path = os.path.expanduser("~/Desktop")
    test_folder = os.path.join(desktop_path, "test_files")
    
    # 创建测试文件夹
    os.makedirs(test_folder, exist_ok=True)
    print(f"✅ 测试文件夹已创建：{test_folder}")

    # 定义要生成的测试文件列表
    test_files = [
        # 文档类
        "项目报告.pdf",
        "会议记录.docx",
        "销售数据.xlsx",
        "演示文稿.pptx",
        "读书笔记.txt",
        "配置文件.json",
        "日志文件.log",
        
        # 图片类
        "风景照片.jpg",
        "工作截图.png",
        "图标文件.ico",
        "矢量图.svg",
        
        # 音视频类
        "会议录音.mp3",
        "教程视频.mp4",
        
        # 压缩包
        "项目资料.zip",
        "备份文件.rar",
        
        # 未知格式
        "乱码文件.abc",
        "未知格式.xyz",
        "奇怪后缀.123"
    ]

    # 生成文件
    for filename in test_files:
        file_path = os.path.join(test_folder, filename)
        # 写入少量内容，确保文件不为空
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"This is a test file: {filename}\n")
        print(f"📄 已生成测试文件：{filename}")

    print("\n🎉 所有测试文件已生成完毕！")
    print("👉 现在你可以打开你的文件整理助手，选择桌面上的 test_files 文件夹进行测试了。")

if __name__ == "__main__":
    create_test_files()