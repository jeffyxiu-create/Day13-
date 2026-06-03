def load_complaints(path):
    """读了txt文件,返回每一行投诉的列表"""
    try:
        with open(path,"r",encoding="utf-8")as f:
            lines = f.readlines()
            complaints = [line.strip() for line in lines if line.strip()]
            return complaints

    except Exception as e:
            print(f"读取文件出错:{e}")
            return[]