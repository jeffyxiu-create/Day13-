#-----------模块1:导入库--------
import os
import tkinter as tk
from tkinter import filedialog,messagebox,scrolledtext
from datetime import datetime
import threading
from pathlib import Path

#------导入自已写的三个功能模块---
from organizer import sort_by_type, sort_by_date, sort_by_size
from report import export_csv_report
from duplicate_checker import find_duplicate_files

#自动定位项目根目录
script_path = Path(__file__).resolve()
base_dir = script_path.parent
os.chdir(base_dir)

#提前创建输出目录，exist_ok=True表示已存在也不报错
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)

#模块3：全局变量声明
log_text_widget = None
btn_start = None
btn_choose = None
select_folder = None
sort_mode = None

#==========模块4:按键状态控制函数===========
def write_log(msg):
    """日志写入函数:同时做两件事
    1. 把日志追加到界面日志文件
    2. 写入本地logs/run.log文件
    """
    global log_text_widget
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_log = f"[{now}]{msg}\n"
    if log_text_widget:
        log_text_widget.after(0, lambda: log_text_widget.insert(tk.END, full_log))
        log_text_widget.after(0, lambda: log_text_widget.see(tk.END))
        log_file = os.path.join("logs", "run.log")
        with open( log_file, "a", encoding="utf-8") as f :
            f.write(full_log)

#统一控制所有按钮可用/禁用
def set_buttons_state(state):
    """
    统一控制所有按钮的可用状态
    :param state:"disabled"->禁用(变灰,不可点击)
    "normal"->恢复正常可点击
    """
    global btn_start, btn_choose
    btn_start.config(state=state)
    btn_choose.config(stat=state)

#===========后台核心函数(子线程中运行)============
def run_sort_task(folder_path, mode):
    """
    真正执行整理的函数,运行在后台子线程里
    这样主线程(界面)不会卡死,用户还能看到日志滚动
    参数:
    folder_path->用户选中的文件夹绝对路径
    mode-> 整理模式字符串:"type"/ "date"/ "size"
    """
    file_list = []
    try: 
        
        if mode =="type":
            file_list = sort_by_type(folder_path, write_log)
        elif mode == "date":
            file_list =sort_by_date(folder_path, write_log)
        elif mode =="size":
            file_list =sort_by_size(folder_path, write_log)

            write_log(f"DEBUG: 扫描到 {len(file_list)} 个文件，准备生成报表...")
        
        if file_list:
            report_path, total = export_csv_report(file_list)
        else:
            write_log("警告：没有获取到任何文件数据，报表可能为空！")
            total = 0
            report_path="无"

        
        dup_list = find_duplicate_files(folder_path)
        write_log(f"整理完成!总计扫描文件:{total}个")
        if dup_list:
            write_log(f"检测到重复文件共{len(dup_list)}个:")

            for item in dup_list:
                write_log(f"{item}")
        else:
            write_log("未检测到任何重复文件")
        write_log(f"CSV报表保存路径:{report_path}")
        write_log("="*60)
        #弹窗提示完成
        log_text_widget.after(0, lambda:messagebox.showinfo(
            "执行完成",
            f"整理完毕\n 文件总数:{total}\n重复文件:{len(dup_list)}个\n报表已存入reports文件夹"))
    except Exception as e:
        err_msg = f"任务执行失败,异常信息:{str(e)}"
        write_log(err_msg)
        log_text_widget.after(0, lambda:messagebox.showerror("运行异常",err_msg))
    finally:
        log_text_widget.after(0, lambda: set_buttons_state(tk.NORMAL))
        log_text_widget.after(0, lambda: btn_start.config(text = "开始整理",bg="#409EFF"))

#启动子线程入口
def start_sort():
    """
    点击"开始整理"按钮触发
    职责:校验输入->锁定按钮->启动子线程
    """
    global select_folder, sort_mode
    path = select_folder.get()
    if not os.path.isdir(path):
        messagebox.showerror("路径错误","请先选择有效的文件夹!")
        return
    mode = sort_mode.get()
    #锁定按钮防止重复点击
    set_buttons_state(tk.DISABLED)
    btn_start.config(text="整理中...",bg="#909399")
    write_log(f"已启动[{mode}]分类任务,后台处理中,请稍候...")

    #创建守护线程
    task_thread = threading.Thread(target = run_sort_task, args=(path, mode),daemon= True)
    task_thread.start()
#============文件夹选择函数===========
def choose_folder():
    """点击"选择整理文件夹"按钮后触发
    弹出系统文件夹选择对话框,.把用户选择的路径存入 select_path
    """
    global select_folder
    path = filedialog.askdirectory()
    if path:
        select_folder.set(path)
        write_log(f"✅已选择目录:{path}\n")

#=============模块5:构建GUI主界面=
def main_gui():
    global log_text_widget, btn_start, btn_choose,select_folder,sort_mode
    root = tk.Tk()
    
    root.title("文件自动归档助手 V2.0终极优化版")
    root.geometry("600x520")
    select_folder = tk.StringVar()
    sort_mode = tk.StringVar(value="type")

    tk.Label(root, text="文件自动归档助手 V2.5",font=("微软雅黑",18, "bold")).pack(pady=12)
    frame_path = tk.Frame(root, pady=6)
    frame_path.pack(fill=tk.X, padx=20)
    btn_choose = tk.Button(frame_path, text="选择整理文件夹",command=choose_folder,width=14)
    btn_choose.pack(side="left")
    tk.Label(frame_path, textvariable=select_folder, fg="#222").pack(side="left", padx=8)

    # 分类模式单选框
    frame_mode = tk.Frame(root, pady=6)
    frame_mode.pack()
    tk.Label(frame_mode, text="整理模式：", font=("微软雅黑", 11)).pack(side="left")
    tk.Radiobutton(frame_mode, text="类型分类", variable=sort_mode, value="type").pack(side="left", padx=10)
    tk.Radiobutton(frame_mode, text="日期分类", variable=sort_mode, value="date").pack(side="left", padx=10)
    tk.Radiobutton(frame_mode, text="大小分类", variable=sort_mode, value="size").pack(side="left", padx=10)

    #开始整理按钮
    # 开始整理按钮
    btn_start = tk.Button(
        root,
        text="开始整理",
        command=start_sort,
        bg="#409EFF",
        fg="white",
        font=("微软雅黑", 12),
        width=20,
        height=2
    )
    btn_start.pack(pady=12)

    # 日志展示区
    tk.Label(root, text="运行日志 & 统计结果", font=("微软雅黑", 11)).pack()
    log_text_widget = scrolledtext.ScrolledText(root, width=72, height=12)
    log_text_widget.pack(padx=12, pady=4)

    root.mainloop()

if __name__ == "__main__":
    main_gui()


    
      
    






