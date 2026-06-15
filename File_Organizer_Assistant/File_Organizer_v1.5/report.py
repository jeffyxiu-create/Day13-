import os
import csv
from datetime import datetime

#-------定义日志文件和报表文件存放的文件夹名
LOG_DIR = "logs"
REPORT_DIR = "reports"
os.makedirs(LOG_DIR, exist_ok = True)
os.makedirs(REPORT_DIR, exist_ok = True)

#----------------日志记录函数-------------
def write_organize_log(file_list):
    """把本次整理的文件明细追加写入日志文件
    :param file_list:文件整理明细列表,格式:[(文件名,分类),....]
    例如:[("report.pdf","PDF"),("pthoto.jpg,"image")]
    """
    log_path = os.path.join(LOG_DIR, "organize_log.txt")
    today = datetime.now().strftime("%Y-%m-%d")
    #追加写入日志,保留历史记录
    with open(log_path, "a", encoding ="utf-8") as f :
        f.write(f"/n======={today} 整理记录=========\n")
        for filename, category in file_list:
            f.write(f"{filename}->{category}\n")

#==========CSV报表导出函数==============
def export_csv_report(file_list):
    """
    把整理明细导出为csv表格文件(可直接用 Excel打开)
    :param file_list 文件整理明细列表,格式同上
    """
    csv_path = os.path.join(REPORT_DIR, "report.csv")
    header = ["文件名","分类"]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(file_list)