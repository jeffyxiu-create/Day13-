from pathlib import Path
import csv
import os

# 获取当前脚本所在目录
base_dir = Path(__file__).resolve().parent
CSV_PATH = base_dir/"data"/"result.csv"

def save_to_csv(complaint,category,reply):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CSV_PATH.exists()
    with open(CSV_PATH,"a",newline="",encoding="utf-8-sig") as f :
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["投诉内容","分类","回复话术"])
        writer.writerow([complaint, category,reply])
       
