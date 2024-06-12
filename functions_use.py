functions = [
{
    'name_for_human': '用户登录',
    'name_for_model': 'login',
    'description_for_model': '当用户需要登录系统时调用此函数进行鉴权',
    'parameters': [
        {
            'name': 'login_account',
            'description': '用户名',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'password',
            'description': '用户密码',
            'required': True,
            'schema': {
                'type': 'string'
            }
        }
    ],
    "returns": {
        "type": "object",
        "properties": {
            "error_code": {"type": "integer", "description": "错误码，0表示正确返回"},
            "code": {"type": "integer", "description": "状态码，200表示成功"},
            "msg": {"type": "string", "description": "描述信息"},
            "status": {"type": "string", "description": "登录状态"},
            "data": {
                "type": "object",
                "properties": {
                    "gf_user": {"type": "boolean", "description": "是否为广发用户"},
                    "id": {"type": "string", "description": "系统用户id"},
                    "login_account": {"type": "string", "description": "登录账户信息"},
                    "menus": {"type": "array", "description": "用户对应的目录信息"},
                    "roles": {"type": "array", "description": "用户对应的权限"},
                    "token": {"type": "string", "description": "用户对应的登录token"},
                    "username": {"type": "string", "description": "用户名"}
                }
            }
        }
    }
}
,
{
    'name_for_human': '上传比对文档',
    'name_for_model': 'upload_compare_documents',
    'description_for_model': '当用户需要上传两个文档进行比对时调用此函数',
    'parameters': [
        {
            'name': 'file_a_path',
            'description': 'A文档的文件路径',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'file_b_path',
            'description': 'B文档的文件路径',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'is_a_ocr',
            'description': 'A文档是否是扫描件',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'is_b_ocr',
            'description': 'B文档是否是扫描件',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'file_a_format',
            'description': 'A文档格式类型（stream: 文件流， md5: 已存在的文件id）',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'file_b_format',
            'description': 'B文档格式类型（stream: 文件流， md5: 已存在的文件id）',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'token',
            'description': '用户的登录token',
            'required': True,
            'schema': {
                'type': 'string'
            }
        }
    ],
    "returns": {
        "type": "object",
        "properties": {
            "error_code": {"type": "integer", "description": "错误码，0表示正确返回"},
            "file_a": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string", "description": "A文档id(md5值)"},
                    "document_name": {"type": "string", "description": "A文档名称"},
                    "document_path": {"type": "string", "description": "A文档s3路径"},
                    "document_type": {"type": "string", "description": "A文档类型"},
                    "file_type": {"type": "string", "description": "A文件类型（是否为扫描件）"}
                }
            },
            "file_b": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string", "description": "B文档id(md5值)"},
                    "document_name": {"type": "string", "description": "B文档名称"},
                    "document_path": {"type": "string", "description": "B文档s3路径"},
                    "document_type": {"type": "string", "description": "B文档类型"},
                    "file_type": {"type": "string", "description": "B文件类型（是否为扫描件）"}
                }
            },
            "task_id": {"type": "string", "description": "比对任务id"}
        }
        }
}
,
{
    'name_for_human': 'Word转PDF',
    'name_for_model': 'word_to_pdf',
    'description_for_model': '当用户需要将Word文档转换为PDF时调用此函数',
    'parameters': [
        {
            'name': 'file_path',
            'description': 'Word文档的文件路径',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'async_mode',
            'description': '获取转换结果的方式（true: 异步（轮询）、false：同步）',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'output_format',
            'description': '输出格式',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'input_format',
            'description': '输入文档的格式 （docx、doc）',
            'required': True,
            'schema': {
                'type': 'string'
            }
        }
    ],
    "returns": {
        "type": "object",
        "properties": {
            "error_code": {"type": "integer", "description": "错误码，0表示正确返回"},
            "msg": {"type": "string", "description": "描述信息"},
            "status": {"type": "string", "description": "状态"},
            "data": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string", "description": "转换后的文档id"},
                    "document_name": {"type": "string", "description": "转换后的文档名称"},
                    "document_path": {"type": "string", "description": "转换后的文档路径"}
                }
            }}}
}
]