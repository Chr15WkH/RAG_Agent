from openai import OpenAI

example_data = {
    '新闻报道': ''
}
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": ""},
        {"role": "system", "content": ""},
        {"role": "system", "content": ""},
    ],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end=" ", flush= True)