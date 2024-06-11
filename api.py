import requests

def login(login_account, password):
    url = "http://ibivs-test.gf.com.cn/validate/api/backend/user/login"
    payload = {
        "login_account": login_account,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def upload_compare_documents(file_a_path, file_b_path, is_a_ocr, is_b_ocr, file_a_format, file_b_format, token):
    url = "http://ibivs-test.gf.com.cn/pdfCompare/v1/upload_file"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    files = {
        "file_a": open(file_a_path, 'rb'),
        "file_b": open(file_b_path, 'rb'),
        "is_a_ocr": (None, str(is_a_ocr).lower()),  # True or False to "true" or "false"
        "is_b_ocr": (None, str(is_b_ocr).lower()),  # True or False to "true" or "false"
        "file_a_format": (None, file_a_format),
        "file_b_format": (None, file_b_format)
    }
    
    response = requests.post(url, files=files, headers=headers)
    return response.json()

def add(num):
    return num + 1
def word_to_pdf(file_path, async_mode, output_format, input_format):
    url = "http://ibivs-test.gf.com.cn/word2pdf/api/docx2pdf"
    payload = {
        "async": async_mode,
        "output-format": output_format,
        "format": input_format
    }
    files = {
        "data": open(file_path, 'rb')
    }
    
    response = requests.post(url, data=payload, files=files)
    return response.json()
# 使用登录接口
# login_response = login("gf_test", "gf_test")
# print(login_response)

# # 使用比对文档上传接口
# token = login_response["data"]["token"]
# upload_response = upload_compare_documents(
#     file_a_path="path/to/file_a.pdf",
#     file_b_path="path/to/file_b.pdf",
#     is_a_ocr=False,
#     is_b_ocr=False,
#     file_a_format="stream",
#     file_b_format="stream",
#     token=token
# )
# print(upload_response)

# # 使用Word转PDF接口
# word2pdf_response = word_to_pdf(
#     file_path="path/to/word_file.docx",
#     async_mode="true",
#     output_format="pdf",
#     input_format="docx"
# )
# print(word2pdf_response)
