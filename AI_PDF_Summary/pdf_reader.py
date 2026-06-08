from pypdf import PdfReader
def read_pdf(pdf_path: str)->str:
    """传入pdf路径,返回全文档文本"""
    try:
        reader = PdfReader(pdf_path)
        all_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text
        return all_text
    except Exception as e :
        return f"读取PDF失败:{str(e)}"
