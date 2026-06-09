from tkinter import filedialog
def save_to_txt(content:str)-> str:
    """
    弹出保存框,自定义路径和文件名:
    return:保存结果方案
    """
    if not content.strip():
        return"内容为空 无需保存"
        
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("文本文件","*.txt"),("所有文件","*.*")],
        title = "选择保存位置"
    )

    if not file_path:
        return"已取消保存"

    try:
        with open (file_path,"w", encoding="utf-8") as f :
            f.write(content)
        return f"保存成功:{file_path}"
    except Exception as e :
        return f"保存失败:{str(e)}"
