from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage

'''
model的输入有明确要求：只能是PromptValue、Str以及Sequence[MessageLikeRepresentable]三种类型。
但比如调用链 chain = prompt_template | model1 | model2 时就会报错,因为model1的输出是AIMessage对象，不是上述三种类型之一。
为了解决这个问题，Langchain提供了一个StrOutputParser类，可以将模型的输出（如AIMessage对象）转换为字符串类型，满足模型输入的要求。
解决办法：chain = prompt_template | model1 | StrOutputParser() | model2
StrOutputParser是一个字符串输出解析器类，(是Runnabale接口子类，可以入链)实现了OutputParser接口，专门用于将模型输出转换为字符串类型。
'''
parser = StrOutputParser()
chatmodel = ChatTongyi(model='qwen3-max')
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，希望名字能够{description}一些，帮忙起名字，只给出一个名字。"
    )
chain = prompt_template | chatmodel | parser | chatmodel | parser
# : AIMessage用于类型提示(Type Hinting)，告诉开发者和IDE，chain.invoke的输出是一个AIMessage对象,实际不影响代码运行，但是需导入AIMessage类。
response: AIMessage = chain.invoke({"lastname": "林", "gender": "女儿", "description": "文雅"}) # 链的最后用了parser之后，response的类型是字符串类型了，不是AIMessage了。
print(response)
print(type(response))