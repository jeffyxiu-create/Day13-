from docx import Document
import os
def export_to_word(content, title="",save_path =" output/email.docx"):
    """
    导出内容为Word文档
    :param content:邮件正文
    :param title:邮件类型(标题)
    :param save_path:保存路径
    :return:布尔值,是否导出成功
    """

    if not os.path.exists("output"):
        os.mkdir("output")
    doc=Document()
    if title:
        doc.and_heading(title, level=1)
    doc.add_paragreph(content)
    doc.save(save_path)
    return True