import openai, requests, torch
from functions_use import functions
import api
qwen_api_url = ''
def run_llm(prompt, history=[], functions=[], sys_prompt= f"You are an useful AI assistant that helps people solve the problem step by step."):
    try:
        openai.api_base = qwen_api_url
        openai.api_key = 'none'
        openai.api_request_timeout = 1 # 设置超时时间为10秒
        messages=[{"role": "system", "content": sys_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": "" + prompt})
        response = openai.ChatCompletion.create(
            model = "qwen_tog",
            messages = messages,
            temperature=0.58,
            max_tokens=2048,
            functions=functions
            )
        data_res = response['choices'][0]['message']['content']
        function_call = response['choices'][0]['message']['function_call']
        return data_res, function_call
    finally:
        torch_gc()
def torch_gc():
    print('清除内存')
    if torch.cuda.is_available():
        with torch.cuda.device('gpu:0'):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
def process_function(function_call):
    if isinstance(function_call, dict):
        function_name = function_call.get('name')
        function_parameters = function_call.get('parameters')
        if function_name == 'login':
            login_account = function_parameters.get('login_account')
            password = function_parameters.get('password')
            result = api.login(login_account, password)
        if function_name == 'upload_compare_documents':
            file_a = function_parameters.get('file_a')
            file_b = function_parameters.get('file_b')
            is_a_ocr = function_parameters.get('is_a_ocr')
            is_b_ocr = function_parameters.get('is_b_ocr')
            file_a_format = function_parameters.get('file_a_format')
            file_b_format = function_parameters.get('file_b_format')
            token = function_parameters.get('token')
            result = api.upload_compare_documents(file_a, file_b, is_a_ocr, is_b_ocr, file_a_format, file_b_format, token)
        if function_name == 'word_to_pdf':
            file_path = function_parameters.get('file_path')
            async_mode = function_parameters.get('async_mode')
            output_format = function_parameters.get('output_format')
            input_format = function_parameters.get('input_format')
            result = api.word_to_pdf(file_path, async_mode, output_format, input_format)
    else:
        result = ''
    return result

def chat(prompt, history):
    answer, function_call = run_llm(prompt=prompt)
    i = 0
    while function_call and i < 3:
        function_response = process_function(function_call)
        new_answer = answer + str(function_response)
        answer, function_call = run_llm(prompt=new_answer)
        i += 1
    pass


# parameters = {'num' : 2, 'xx':4}
# function = getattr(api, 'add', None)
# print(function)
# result = function(**parameters)
# print(result)
