import os
import shutil
 
#全局文件分类规则库------------
FILE_RULES = {
    "PDF":[".pdf"],
    "Word":[".doc",".docx"],
    "Excel":[".xls",".xlsx",".csv"],
    "Image":[".jpg",".jpeg",".png",".gif",".bmp"]
}

#============后缀->类别匹配函数=======
def get_file_category(suffix):
    """
    根据文件后缀名,返回对应的分类名称
    :param suffix: 文件后缀.例如".pdf",".docx"(字符串)
    :return: 分类名称字符串,例如"PDF", "Word", 未匹配则返回"Other"
    """
    for category, suffix_list in FILE_RULES.items():
        if suffix.lower() in suffix_list:
            return category
    return "Other"

#=======文件整理=============
def organize_files(source_folder):
    """
    核心整理函数:扫描指定目录,按类别自动移动文件
    :param source_folder:需要整理的目标文件夹路径(字符串)
    :return: (count_dict, file_detail)
    coutn_dict->各类别整理数量的字典
    file_detail->每个文件整理结果的明细列表
    """
    count_dict={
        "PDF":0,
        "Word":0,
        "Excel":0,
        "Image":0,
        "Other":0,
    }
    file_detail = []

#===============遍历并处理每个文件==============
    for file in os.listdir(source_folder):
        file_full_path = os.path.join(source_folder,file)

        if os.path.isdir(file_full_path):
            continue
        #分离文件名与后缀
        _, suffix = os.path.splitext(file)
        category = get_file_category(suffix)

        target_folder = os.path.join(source_folder, category)
        os.makedirs(target_folder, exist_ok = True)
        target_path = os.path.join(target_folder,file)
        if os.path.exists(target_path):
            print(f"[跳过-防覆盖]{file}->目标目录已存在同名文件,已保护原始数据")
            continue
        
        try: 
            shutil.move(file_full_path, target_path)
            count_dict[category] += 1
            file_detail.append((file, category))
        except Exception as e:
            print(f"[移动失败]{file}->错误信息:{str(e)}")
    return count_dict, file_detail












