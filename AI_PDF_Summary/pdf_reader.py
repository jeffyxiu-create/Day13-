from pypdf import PdfReader
from pathlib import Path
base = Path(__file__).parent
pdf_path = base/"input_file"/"test.pdf"

MAX_CHAR =5000

def read_pdf(pdf_path: str) -> tuple[str, str]:
    """
    读取PDF全部文本内容
    返回(文本内容,是否被截断)
    """
    content =""
    tip=""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            content += page_text
       
        if not content.strip():
            return"","提示:当前为图片型PDF,无法提取文字"

        if len(content) > MAX_CHAR:
            content = content[:MAX_CHAR]
            tip = f"提示:内容较长,已截取前{MAX_CHAR}字符"
    except Exception as e:
        return "", f"PDF读取失败:{str(e)}"
    return content,tip
if __name__=="__main__":
    
    text,msg = read_pdf(pdf_path)
    print(msg)
    print(text)
    
        