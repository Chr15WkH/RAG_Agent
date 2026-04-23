from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
# 基于PromptTemplate，实现zero-shot
# 基于FewShotPromptTemplate，实现few-shot
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，希望名字能够{description}一些，帮忙起名字，请简略回答。"
)
'''
# 变量注入，生成提示词文本
promt_text = prompt_template.format(lastname="王", gender="女儿", description="文雅")

# 创建模型对象
llms = Tongyi(model="qwen-max")

# 调用模型获取结果，invoke方式
response = llms.invoke(input=promt_text)
print(response)
'''

# 创建模型对象
llms = Tongyi(model="qwen-max")

# 构建执行链，只有PromtTmeplate对象可以加入，字符串不行。
chain = prompt_template | llms

# 链对象调用invoke方法，调用模型
response = chain.invoke(input={"lastname": "王", "gender": "女儿", "description": "文雅"})

print(response)