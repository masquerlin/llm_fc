import openai, requests, torch
from functions_use import functions, functions_other
import api, json
import gradio as gr

def run_llm(prompt, history=[], functions=[], function_name='',function_parameters='',sys_prompt= f"You are an useful AI assistant that helps people solve the problem step by step."):
    try:
        openai.api_base = "http://localhost:8009/v1"
        openai.api_key = 'none'
        openai.api_request_timeout = 1 # 设置超时时间为10秒
        messages = []
        messages.extend(history)
        if 'function_call_output' in prompt:
            messages.append({"role": "function",  'name':prompt.split("'s ")[0],"content": prompt.split('function_call_output: ')[1]})
        else:
            messages.append({"role": "user", "content": "" + prompt})
        print(f'构造的messages********{messages}')
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
    print('清除gpu内存')
    if torch.cuda.is_available():
        with torch.cuda.device('cuda:0'):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
def process_function(function_call):
    if isinstance(function_call, dict):
        function_name = function_call.get('name')
        function_parameters = json.loads(function_call.get('arguments'))
        # 这种写法更有robust性，通用一点可以直接eval(function, **arguments) 就行
        if function_name == 'login':
            print('use function login')
            login_account = function_parameters.get('login_account')
            password = function_parameters.get('password')
            result = api.login(login_account, password)
        if function_name == 'upload_compare_documents':
            print('use function upload_compare_documents')
            file_a = function_parameters.get('file_a')
            file_b = function_parameters.get('file_b')
            is_a_ocr = function_parameters.get('is_a_ocr')
            is_b_ocr = function_parameters.get('is_b_ocr')
            file_a_format = function_parameters.get('file_a_format')
            file_b_format = function_parameters.get('file_b_format')
            token = function_parameters.get('token')
            result = api.upload_compare_documents(file_a, file_b, is_a_ocr, is_b_ocr, file_a_format, file_b_format, token)
        if function_name == 'word_to_pdf':
            print('use function word_to_pdf')
            file_path = function_parameters.get('file_path')
            async_mode = function_parameters.get('async_mode')
            output_format = function_parameters.get('output_format')
            input_format = function_parameters.get('input_format')
            result = api.word_to_pdf(file_path, async_mode, output_format, input_format)
        if function_name == 'get_history_events':
            print('use function get_history_events')
            date = function_parameters.get('date')
            result = api.get_history_events(date)
        if function_name == 'get_holiday_info':
            print('use function get_holiday_info')
            date = function_parameters.get('date')
            result = api.get_holiday_info(date)
        if function_name == 'get_today_date':
            result = api.get_today_date()
    else:
        result = ''
    return result

def model_chat(prompt, history=[], sys_prompt= f"You are an useful AI assistant that helps people solve the problem step by step."):
    responses = list()
    message=[{"role": "system", "content": sys_prompt}]
    if len(history) > 0:
        for history_msg in history:
            if 'function_call_output' in history_msg[0]:
                message.append({'role': 'function', 'name':history_msg[0].split("'s ")[0],'content': history_msg[0].split('function_call_output: ')[1]})
                message.append({'role': 'assistant', 'content': history_msg[1]})
            else:
                message.append({'role': 'user', 'content': history_msg[0]})
                message.append({'role': 'assistant', 'content': history_msg[1]})
            responses.append(history_msg)
    mylist = list()
    mylist.append(prompt)

    answer, function_call = run_llm(prompt=prompt, history=message, functions=functions_other)
    print(f"first_answer********{answer}")
    print(f"first_function_call********{function_call}")
    mylist.append(answer)
    responses.append(mylist)
    yield responses, {}, {}, {}
    message.append({'role': 'user', 'content': prompt})
    if not function_call:
        message.append({'role': 'assistant', 'content': answer})
        function_name = ''
        function_parameters = ''
        function_response = {}
    e_msg = ''
    mylist = list()
    i = 0
    while function_call and i < 3:
        print(f"第******{i}***********轮")
        function_name = function_call.get('name')
        function_parameters = json.loads(function_call.get('arguments').replace('False', 'false').replace('True', 'true'))
        function_call_use = {'name':function_name, 'arguments':function_call.get('arguments')}
        message.append({'role': 'assistant', 'content': answer, 'function_call':function_call_use})
        
        yield responses, {function_name : 'running'}, {'parameters':function_parameters}, {} 
        try:
            function_response = process_function(function_call)
            yield responses, {function_name : 'done'}, {'parameters':function_parameters}, function_response
        except Exception as e:
            print(f"error*********{e}")
            e_msg = str(e)
            function_response = {"error":e_msg}
            # function_response = {"result":'succeed'}
            
            yield responses, {function_name : 'error'}, {'parameters':function_parameters}, {"error":e}
        new_prompt = function_name + "'s " + 'function_call_output: ' + str(function_response)
        mylist.append(new_prompt)
        answer, function_call = run_llm(prompt=new_prompt, history=message, functions=functions_other)
        print(f"in_{i}_answer********{answer}")
        print(f"in_{i}_function_call********{function_call}")
        mylist.append(answer)
        responses.append(mylist)
        mylist = list()
        message.append({'role': 'function', 'name':function_name,'content': str(function_response)})
        message.append({'role': 'assistant', 'content': answer})
        i += 1
        yield responses, {function_name : 'done'}, {'parameters':function_parameters}, function_response
    if len(e_msg) > 0:
        yield responses, {function_name : 'error'}, {'parameters':function_parameters}, {'error': e_msg}
    else:
        yield responses, {function_name : 'done'}, {'parameters':function_parameters}, function_response
def clear_session():
    return '', [], {}, {}, {}
def main():
    with gr.Blocks(css="footer {visibility: hidden}",theme=gr.themes.Soft()) as demo:
        gr.Markdown("""<center><font size=10>llm with function calls</center>""")
        with gr.Row():
            function_json = gr.JSON(label='函数执行状态')
            parameter_json = gr.JSON(label='参数')
            result_json = gr.JSON(label='结果')
        with gr.Row(equal_height=False):
            chatbot = gr.Chatbot(label='智能bot回答',scale=1)
        with gr.Row():
            textbox = gr.Textbox(lines=3, label='提出你的问题吧')
        with gr.Row():
            with gr.Column():
                clear_history = gr.Button("🧹 clear")
                sumbit = gr.Button("🚀 submit")
        
        sumbit.click(model_chat, [textbox, chatbot], [chatbot, function_json, parameter_json, result_json])
        clear_history.click(fn=clear_session,
                            inputs=[],
                            outputs=[textbox, chatbot, function_json, parameter_json, result_json])
    demo.queue(api_open=False).launch(server_name='0.0.0.0', server_port=7860,max_threads=10, height=800, share=False)
if __name__ == "__main__":
    main()

#用getattr的方法获取函数, 也可以用eval的方法获取, 也可以用kernel的方法获取函数
# parameters = {'num' : 2, 'xx':4}
# function = getattr(api, 'add', None)
# print(function)
# result = function(**parameters)
# print(result)
