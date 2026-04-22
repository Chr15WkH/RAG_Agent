from openai import OpenAI

'''
#一、openai库的基础使用
#1.获取client对象，创建OPENAI类对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
#2.调用模型
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "你是一个python编程专家，并且不说废话，简单回答"},
        {"role": "assistant", "content": "好的，我是编程专家，并且不多逼逼，你要问什么？"},
        {"role": "user", "content": "输出1-10的数字，并使用python代码"},
    ]
)
#3.处理回复结果
print(response.choices[0].message.content)
'''

#二、openai库的流式输出模式
#1.获取client对象，创建OPENAI类对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
#2.调用模型
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "你是一个python编程专家，并且话非常多"},
        {"role": "assistant", "content": "好的，我是编程专家，并且话很多，你要问什么？"},
        {"role": "user", "content": "输出1-10的数字，并使用python代码"}
    ],
    stream=True
)
#3.处理回复结果
for chunk in response:
    print(chunk.choices[0].delta.content,
          end=" ",      #每一段之间以空格分隔
          flush=True    #立刻刷新缓冲区
          )