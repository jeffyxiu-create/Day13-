import os
import shutil
import json
from datetime import datetime
from pathlib import Path
current_path = Path(__file__).resolve()
base_dir = current_path.parent


#读取配置文件
def load_config():
    
    config_path = base_dir/"config"/"config.json"
    with open(config_path, "r", encoding="utf-8")as f:
        return json.load(f)
CONFIG = load_config()
TYPE_RULES = CONFIG["type_rules"]
SIZE_SMALL = CONFIG["size_split"]["small"]
SIZE_MEDIUM = CONFIG["size_split"]["medium"]


#模块3：按类型分类===========
def sort_by_type(source_dir, log_callback=None):
    """按文件后缀分类，规则从config.json读取"""
    if log_callback:
        log_callback(f"DEBUG: 正在扫描目录: {source_dir}")
        items = os.listdir(source_dir)
        log_callback(f"DEBUG: 扫描到 {len(items)} 个项目")
        for item in items:
            log_callback(f"DEBUG: 发现项目: {item}")
    file_list=[]
   
    # 1. 关键点：获取一份静态的文件列表，排除所有文件夹
    items = os.listdir(source_dir)
    # 使用列表推导式只获取文件，过滤掉已经存在的子文件夹
    all_files = [f for f in items if os.path.isfile(os.path.join(source_dir, f))]
    for cat_name in TYPE_RULES.keys():
        os.makedirs(os.path.join(source_dir, cat_name),exist_ok=True)
        os.makedirs(os.path.join(source_dir, "Other"),exist_ok=True)
    #----遍历源文件夹里的所有内容
    for filename in all_files:
        file_path = os.path.join(source_dir, filename)
        if os.path.isdir(file_path):
            continue
        #获取文件后缀小写
        suffix = os.path.splitext(filename)[1].lower()
        target_cat="Other"
        for cat_name, suffix_list in TYPE_RULES.items():
            if suffix in suffix_list:
                target_cat = cat_name
                break
        target_dir = os.path.join(source_dir, target_cat)
        target_path = os.path.join(target_dir,filename)
        
        try:
            # 如果目标已存在，shutil.move 会报错，这里简单处理：跳过或覆盖
            if os.path.exists(target_path):
                if log_callback:
                    log_callback(f"警告：文件已存在，跳过: {filename}")
                continue 
            
            shutil.move(file_path, target_path)
            file_list.append((filename, target_cat))
            if log_callback:
                log_callback(f"类型分类：{filename}->{target_cat}")
        except Exception as e:
            if log_callback:
                log_callback(f"移动出错 {filename}: {str(e)}")
    return file_list

#=========模块4：按日期分类=============
def get_file_date_folder(file_path):
    """辅助函数:获取文件的修改年月,返回"2026-06"格式的字符串
    作用:根据这个字符串给文件找到对应的年月文件夹
    """
    mtime = os.path.getmtime(file_path)
    date_obj = datetime.fromtimestamp(mtime)
    return date_obj.strftime("%Y-%m")

def sort_by_date(source_dir, log_callback=None):
    """按文件修改年月分类,自动创建"2026-06"这样的年月文件夹
    参数:
    source_dir-> 目标文件夹路径
    log_callback->日志回调函数
    """
    file_list =[]
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        #路过子文件夹,只处理文件
        if os.path.isdir(file_path):
            continue
        #调用辅助函数,获取年月字符串(文件名)
        folder_name = get_file_date_folder(file_path)
        #在源目录下创建年月子文件夹,路径
        target_dir = os.path.join(source_dir, folder_name)
        os.makedirs(target_dir, exist_ok= True)

        #拼出完整目标路径,移动文件
        target_path = os.path.join(target_dir, filename)
        shutil.move(file_path, target_path)
        file_list.append((filename,folder_name))
        if log_callback:
            log_callback(f"日期分类:{filename}->{folder_name}/")
    return file_list

#================模块5:按大小分类============
def get_size_folder(file_path):
    """辅助函数:判断文件太小属于哪个区间,返回文件夹名称字符串
    Small(小文件) /Medium(中等)/Large(大文件)
    """
    
    file_size = os.path.getsize(file_path)
    if  file_size <=SIZE_SMALL:
        return"Small"
    elif file_size <= SIZE_MEDIUM:
        return"Medium"
    else:
        return"Large"

def sort_by_size(source_dir, log_callback=None):
    """
    按文件大小分类
    """
    file_list=[]
    #size 根目录:source_dir/size/
    size_root = os.path.join(source_dir, "Size")
    #预先创建三个分类文件夹
    for folder in ["Small","Medium","Large"]:
        os.makedirs(os.path.join(size_root, folder), exist_ok = True)
    
    for filename in os.listdir(source_dir):
        file_path = os.path.join(size_root, filename)
        #跳过所有子文件夹(包括刚建的size/文件夹)
        if os.path.isdir(file_path):
            continue
        #判断文件属于哪个大小区间
        size_folder = get_size_folder(file_path)
        #拼出完整目标路径:source_dir/size/small/xxx.pdf
        target_dir = os.path.join(size_root, size_folder)
        target_path= os.path.join(target_dir, filename)
        shutil.move(file_path, target_path)
        file_list.append((filename,size_folder))

        if log_callback:
            log_callback(f"大小分类:{filename}->size/{size_folder}/")
    return file_list






    
        
 
