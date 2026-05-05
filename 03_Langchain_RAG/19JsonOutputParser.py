
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
'''
chain = prompt_template | chatmodel | parser | chatmodel | parser
这种链的构建其实不标准，正常情况下应有如下逻辑：
invoke/stream -> prompt_template -> chatmodel -> 数据处理 -> prompt_template -> chatmodel -> parser解析器 -> 最终结果
(即，上一个模型的输出结果，应该作为提示词模版的输入，构建下一个提示词，用来二次调用模型。)
'''

'''
提示词模版调用invoke方法时，输入必须是一个字典，包含了模版中定义的变量。(chain链只能调用invoke/stream方法，不能调用format方法，因为format方法不支持链式调用。)
因此，需要完成：
将模型输出的AIMessage对象 -> 转换为字典 -> 注入到第二个提示词模版中 -> 构建下一个提示词文本(PromptValue对象) ->
再调用模型进行二次回复 -> 最后用StrOutputParser解析器将最终结果转换为字符串类型。
'''

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

chatmodel = ChatTongyi(model='qwen3-max')

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，希望名字能够{description}，帮忙起名字，只给出一个名字，"
    "要求key是name，value是名字文本，请严格遵守格式要求"
)
second_prompt = PromptTemplate.from_template(
    "姓名是{name}，请帮我解析含义。"
)

chain = first_prompt | chatmodel | json_parser | second_prompt | chatmodel | str_parser
# 链最终的输出结果response为str类型
response : str = chain.invoke({"lastname": "林", "gender": "女儿", "description": "大气，有文化且不大众"})
print(response)
print(type(response))