from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
'''
除了 Json/StrOutputParser 这类固定功能的解析器之外,也可以自己编写 Lambda 匿名函数来完成自定义逻辑的数据转换。
可以基于 RunnableLambda 类实现这个功能：
RunnableLambda 类是 LangChain 内置的，将普通函数等转换为 Runnable 接口实例，方便自定义函数加入 chain。

语法：
RunnableLambda(函数对象或 Lambda 匿名函数)

Lambda(匿名函数)是 Python 中一种无需显式定义函数名的轻量级函数，常用于简单、一次性、内联的函数逻辑。
语法结构: lambda 参数1, 参数2, ... : 表达式(即返回值)  
等价于 
def 函数名(参数1, 参数2, ...):
    return 表达式
'''

str_parser = StrOutputParser()
# 定义一个自定义的函数，将AIMessage对象转换为字典，提取content作为name的值。并通过RunnableLambda将其转换为Runnable对象，方便加入chain。
# 注意：这里的 ai_msg：只是 lambda 的输入参数名（占位符），真正的值是在 chain 运行时由 LangChain 自动传进来的
my_func =  RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

chatmodel = ChatTongyi(model="qwen3-max")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，希望名字能够{description}，帮忙起名字，只给出一个名字，"
)

second_prompt = PromptTemplate.from_template(
    "姓名是{name}，请帮我解析含义。"
)

chain = first_prompt | chatmodel | my_func | second_prompt | chatmodel | str_parser
'''
跳过 RunnableLambda 类，直接让函数加入链也是可以的。如下所示：
(chain = first_prompt | model | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | model | str_parser)
因为 Runnable 接口类在实现 __or__ (也就是 | 操作符)的时候，支持 Callable 接口的实例。
函数就是 Callable 接口的实例，如上代码示例，| 符号（底层是调用 __or__ ）组链，是支持函数加入的。其本质是将函数自动转换为 RunnableLambda
'''
response : str = chain.invoke({"lastname": "林", "gender": "女儿", "description": "大气，有文化且不大众"})
print(response)
print(type(response))