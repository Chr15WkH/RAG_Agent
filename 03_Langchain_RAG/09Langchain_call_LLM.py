from langchain_community.llms.tongyi import Tongyi

# qwen3-max是chatmodel，qwen-max是llm
llm = Tongyi(model="qwen-max")

'''
# 调用invoke向模型提问
response = llm.invoke(input="你是谁，你能做什么？")

print(response)
'''
# 用stream方法让模型流式输出结果
response = llm.stream(input="你是谁，你能做什么？")

for chunk in response:
    print(chunk, end = " ", flush = True)