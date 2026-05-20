from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

# “装饰器（Decorator）”本质上是：在不修改原函数代码的情况下，给函数额外增加功能的一种机制。
# 本质就是接受函数，并返回新函数的函数。(在函数外层嵌套了一层函数)
# @tool 装饰器是把一个普通函数“包装”成 Agent 可以识别和调用的 Tool 对象。
@tool(description="查询天气")
def get_weather():
    return "下雨"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题。"
)

res = agent.invoke(
    {"messages":[
        {"role":"user","content":"明天慕尼黑的天气怎么样？"}
    ]}
)

parser = StrOutputParser()

for msg in res["messages"]:
    # 查看消息对应的类型名称，并将消息传入解析器，生成字符串
    print(f"{type(msg).__name__}: {parser.invoke(msg)}")