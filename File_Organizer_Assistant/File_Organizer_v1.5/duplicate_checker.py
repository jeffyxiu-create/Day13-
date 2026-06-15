import os
def find_duplicate_files(folder_path):
    """精准重得文件检测
    规则：完整文件名(包含后缀)完全一致才判定为重复
   """
#------初始化两个容器-----------
    name_map = {}
    duplicates = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            if file not in name_map:
                name_map[file] = []
            name_map[file].append(full_path)


    for filename, path_list in name_map.items():
        if len(path_list) > 1:
            duplicates.extend(path_list)
    return duplicates




