from openai import OpenAI
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role":"system", "content":"你是一个AI助理，回答很简洁"},
        {"role":"user", "content":"小红有两只宠物狗"},
        {"role":"assistant", "content":"好的"},
        {"role":"user", "content":"小明有三只宠物狗"},
        {"role":"assistant", "content":"好的"},
        {"role":"user", "content":"一共有几只宠物？"},
    ],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end=" ", flush=True)