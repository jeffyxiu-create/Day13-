#-----------模块1:导入库--------
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext,scrolledtext
import os

#------导入自已写的三个功能模块---
import organizer
import report
import duplicate_checker
from pathlib import Path
import threading

script_path = Path(__file__).resolve()
base_dir = script_path.parent
os.chdir(base_dir)
#============模块2:初始化主窗口==========
root = tk.Tk()
root.title("文件自动归档助手 V1.5 终极优化版")
root.geometry("600x520")

select_path = tk.StringVar()

#==========模块3:按键状态控制函数===========
def set_buttons_state(state):
    """
    统一控制所有按钮的可用状态
    :param state:"disabled"->禁用(变灰,不可点击)
    "normal"->恢复正常可点击
    """
    btn_start.config(state=state)
    btn_choose.config(stat=state)

#===========模块4:核心函数(子线程中运行)============
def run_organize_task():
    """文件整理的主逻辑,在子线程中执行"""
    path = select_path.get()
    if not path:
        root.after(0, lambda: log_box.insert(tk.END,"⚠ 请先选择文件夹!\n"))
        root.after(0,lambda:set_buttons_state("normal"))
        return
#在日志区输出"开始整理"的提示
    root.after(0, lambda: log_box.insert(tk.END,"====开始整理文件======\n"))
    root.after(0,lambda: log_box.see(tk.END))#让日志自动滚动到最新一行

    #------调用核心整理功能-----------执行之前在organizer写的organizer_files(path)函数
    count_result, file_detail = organizer.organize_files(path)

    #生成本地日志 + CSV报表
    report.write_organize_log(file_detail)
    report.export_csv_report(file_detail)

    #------调用查重检测.---执行之前在duplicate文件里写的函数 
    dup_list = duplicate_checker.find_duplicate_files(path)
    total_files = sum(count_result.values())
    def show_result():
        log_box.insert(tk.END,f"✅整理完成!共成功处理{total_files}个文件")
        log_box.insert(tk.END, f"📊分类统计:\n")
        log_box.insert(tk.END, f"PDF：{count_result['PDF']} 个\n")
        log_box.insert(tk.END, f"Word：{count_result['Word']} 个\n")
        log_box.insert(tk.END, f"Excel：{count_result['Excel']} 个\n")
        log_box.insert(tk.END, f"图片：{count_result['Image']} 个\n")
        log_box.insert(tk.END, f"其他：{count_result['Other']} 个\n")


        #展示重复文件结果
        if dup_list:
            log_box.insert(tk.END, f"\n检测到重复文件 ({len(dup_list)}个):\n")
            for item in dup_list:
                log_box.insert(tk.END, f" {item}\n")
        else:
            log_box.insert(tk.END, "\n✔未发现重复文件")

        #输出文件保存路径
        

        log_box.insert(tk.END, "\n日志已保存到 base_dir/logs/\n")
        log_box.insert(tk.END,"报表已保存到base_dir / reports/report.csv\n")
        log_box.insert(tk.END,"="*50 +"\n")
        log_box.see(tk.END)
        set_buttons_state("normal")
        btn_start.config(text="开始自动整理",bg="#009966")
    root.after(0, show_result)

#==========模块5:启动子线程函数============
def start_task_thread():
    """
    点击"开始自动整理"按钮后触发
    创建子线程运行整理任务, GUI 主线程保持响应, 不卡死
    """
    set_buttons_state("disabled")
    btn_start.config(text="整理中...", bg="#909399")
    task_thread = threading.Thread(target=run_organize_task)
    task_thread.daemon=True
    task_thread.start()

#============模块6:文件夹选择函数===========
def choose_folder():
    """点击"选择整理文件夹"按钮后触发
    弹出系统文件夹选择对话框,.把用户选择的路径存入 select_path
    """
    path = filedialog.askdirectory()
    if path:
        select_path.set(path)
        log_box.insert(tk.END, f"✅已选择目录:{path}\n")
        log_box.see(tk.END)

#===============模块7:搭配GUI界面控件============
tk.Label(root, text="文件自动归档助手 V1.5",font=("微软雅黑",18, "bold")).pack(pady=12)
frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, padx=20)
btn_choose = tk.Button(frame_top, text="选择整理文件夹",command=choose_folder,width=14)
btn_choose.pack(side=tk.LEFT)
tk.Label(frame_top, textvariable=select_path, fg="#222").pack(side=tk.LEFT, padx=10)

#开始整理按钮
btn_start = tk.Button(
    root,
    text="开始自动整理",
    command=start_task_thread,
    font=("微软雅黑",13),
    bg = "#009966",
    fg = "white",
    width=20
)
btn_start.pack(pady=18)

#日志展示区
tk.Label(
    root,
    text="运行日志&统计结果",
    font=("微软雅黑",11)
).pack()
log_box = scrolledtext.ScrolledText(root,width=85, height=20)
log_box.pack(padx=15,pady=5)

#===============模块8:启动窗口主循环===========
if __name__ == "__main__":
    root.mainloop()





