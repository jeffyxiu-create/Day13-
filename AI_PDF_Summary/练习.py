


from pypdf import PdfReader
def read_pdf(file_path):
    reader = PdfReader(file_path)

    all_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            all_text+= page_text
    return all_text
# all_text="" 空容器,准备装文字
# all_text=0  如果装的是数字,就用0
# all_text=[]如果装的是列表,就用[]

