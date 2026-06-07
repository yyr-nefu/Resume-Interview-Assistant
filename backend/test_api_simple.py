import os
from openai import OpenAI

api_key = 'sk-f7a3f8ab460d47b8a0bc6f5f46d5b42b'
base_url = 'https://api.deepseek.com/v1'

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

try:
    print("正在测试 DeepSeek API 连接...")
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[
            {'role': 'system', 'content': '你是一个专业的面试官。'},
            {'role': 'user', 'content': '请用中文简单介绍一下自己作为面试官的角色。'}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    print("API 连接成功！")
    print("回复内容:", response.choices[0].message.content)
    
except Exception as e:
    print("API 连接失败:", str(e))
    import traceback
    traceback.print_exc()