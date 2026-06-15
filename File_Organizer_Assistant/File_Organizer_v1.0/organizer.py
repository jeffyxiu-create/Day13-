import os
import shutil
from pathlib import Path
FILE_CATEGORIES = {
    "PDF": [".pdf"],
    "Excel": [".xlsx", ".xls", ".csv"],
    "Word": [".docx", ".doc"],
    "Image": [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
}
#-------------功能:扫描文件---------
def scan_files(folder_path):
    """扫描指定文件夹，返回所有文件完整路径（排除文件夹"""
    file_list = []
    for item in os.listdir(folder_path):
        item_path=os.path.join(folder_path,item)
        if os.path.isfile(item_path):
            file_list.append(item_path)
    return file_list

#--------------功能:识别文件--------------
def get_file_category(file_path):
    """根据文件后缀判断分类,无匹配则归为 Other"""
    file_suffix= Path(file_path).suffix.lower()
    for category, suffix_list in FILE_CATEGORIES.items():
        if file_suffix in suffix_list:
            return category
    return "Other"

#-------------功能:自动建仓库-----------
def create_category_folders(base_output):
    """在输出目录下自动创建分类文件"""
    all_categories = list(FILE_CATEGORIES.keys()) + ["Other"]
    for cate in all_categories:
        cate_path = os.path.join(base_output, cate)
        if not os.path.exists(cate_path):
            os.mkdir(cate_path)

#-------------功能:执行整理工作---------
def organize_files(source_folder, output_folder):
    """主整理逻辑:扫描->分类->建目录->移动文件,返回分类统计结果"""
    count_result = {
        "PDF":0,
        "Excel":0,
        "Word":0,
        "Image":0,
        "Other":0
    }
    #1.扫描:先把需要处理的文件全部找出来
    file_list = scan_files(source_folder)
    if not file_list:
        return {},"未扫描到任何文件"

    #2.建目录:先把货架准备好    
    create_category_folders(output_folder)
    count_result= {category:0 for category in FILE_CATEGORIES.keys()}

    #3.循环搬运:给每个文件找家
    for file_path in file_list:
        category = get_file_category(file_path)
        target_dir = os.path.join(output_folder, category)
        target_path = os.path.join(target_dir, os.path.basename(file_path))

        try:
            shutil.move(file_path, target_path)
            count_result[category]=count_result.get(category,0)+1
        except Exception as e:
            print(f"移动文件失败：{file_path},错误信息：{e}")
    return  count_result,"整理完成"





