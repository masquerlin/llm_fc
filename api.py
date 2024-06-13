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

import requests

def get_history_events(date):
    """
    调用聚合数据的历史上的今天事件列表API，根据指定日期获取历史事件列表。
    
    参数:
    api_key (str): 你的API key。
    date (str): 查询的日期，格式为'M/D'（例如'1/1'表示1月1日）。
    
    返回:
    dict: API返回的响应结果。如果请求失败，返回包含错误信息的字典。
    """
    api_url = 'http://v.juhe.cn/todayOnhistory/queryEvent.php'
    request_params = {
        'key': '20f3ee5db3daabd25a2a3527856a4e65',
        'date': date,
    }
    
    response = requests.get(api_url, params=request_params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': '请求异常', 'status_code': response.status_code}



import requests

def get_holiday_info(date):
    """
    调用聚合数据的节假日安排查询API，根据指定日期获取节假日安排信息。
    
    参数:
    api_key (str): 你的API key。
    date (str): 查询的日期，格式为'YYYY-MM-DD'（例如'2021-05-09'）。
    detail (str, optional): 详细信息参数，可选，默认值为空字符串。
    
    返回:
    dict: API返回的响应结果。如果请求失败，返回包含错误信息的字典。
    """
    api_url = 'http://apis.juhe.cn/fapig/calendar/day'
    request_params = {
        'key': '8cbb780f1e5968959c4e1c0bce27843a',
        'date': date,
        'detail': '',
    }
    
    response = requests.get(api_url, params=request_params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': '请求异常', 'status_code': response.status_code}


from datetime import datetime

def get_today_date():
    """
    获取当天日期，格式为'yyyy-mm-dd'。
    
    返回:
    str: 当前日期，格式为'yyyy-mm-dd'。
    """
    today = datetime.today()
    formatted_date = today.strftime('%Y-%m-%d')
    return formatted_date