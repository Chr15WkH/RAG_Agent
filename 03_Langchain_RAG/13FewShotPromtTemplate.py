from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms.tongyi import Tongyi

"""
FewShotPromptTemplate参数：
    • examples: 示例数据，list，内套字典
    • example_prompt: 示例数据的提示词模板
    • prefix: 组装提示词，示例数据前内容
    • suffix: 组装提示词，示例数据后内容
    • input_variables: 列表，注入的变量列表
"""
# 示例数据的提示词模版
example_template = PromptTemplate.from_template("单词：{word}, 反义词：{antonym}")

# 示例数据
example_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"}
]

#Few shot提示词模版对象
few_shot_prompt = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example_data,
    prefix="给出给定词的反义词，有如下示例：",
    suffix="基于示例告诉我：{input_word}的反义词是？",
    input_variables=['input_word'] # 注入的变量，input_word是要注入的变量，也就是上面的word变量
)

# 获得最终提示词
prompt_text = few_shot_prompt.invoke(input={"input_word": "左"}).to_string()
print(prompt_text)

# 调用模型
llms = Tongyi(model="qwen-max")
response = llms.invoke(input=prompt_text)
print(response)