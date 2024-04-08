import gradio as gr
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.memory import ConversationBufferMemory

load_dotenv()

TITLE="酒店智能客服系统"
DESCRIPTION="""
基于提供的数据，实现一个智能的酒店客服系统。核心功能如下：
* 价格区间检索：用户可以指定一个价格区间，如 300-500 元，系统返回此价格范围内的酒店列表。
* 名称检索：用户可以直接输入酒店名称或部分名称进行查询，系统会返回与该名称匹配或相近的酒店。
* 评分检索：用户可以选择查找高于或低于某一评分的酒店。
* 设施检索：用户可以根据需要的设施（如游泳池、健身房、WIFI）来筛选酒店。
* 多轮对话：系统能够理解用户的多轮对话上下文，例如：提出“我要一个有游泳池的酒店”后，再提要求“价格在 500 元以下的”。
* 安全防护：系统设计时需注意输入检查与处理，防止恶意代码或输入导致系统崩溃或数据泄露。
"""

db = SQLDatabase.from_uri("sqlite:///hotels.db")
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
memory = ConversationBufferMemory(
    input_key="input", 
    output_key='output',
    memory_key="chat_history",
    return_messages=True
)

# copy and translate from original version of create_sql_agent
'''
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct sqlite query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.
'''
prefix = '''
你是一个订票平台的客服，你需要礼貌地回复用户关于酒店的问询。
回复时，首先将用户的问题结合对话历史，整理成一个完整的问题，复述一遍，然后再输出回答。

回复的答案如果具有多个可能性，那么在列出这些可能性后，推荐一个最佳的答案。
每次的回复都需要礼貌且专业，用中文回复用户

在处理用户的问题的过程中，你需要与一个SQL数据库进行交互。
在接收到输入问题后，创建一个语法正确的sqlite查询语句进行执行，然后根据查询结果回答问题。
除非用户指定了希望获取的具体例子数量，否则始终将查询结果限制在最多5个。
可以根据相关列对结果进行排序，以返回数据库中最有趣的示例。
永远不要查询某个特定表的所有列，只查询问题中给定的相关列。
你可以使用下面的工具与数据库进行交互。
只使用以下的工具。只使用以下工具返回的信息来构建最终答案。
你必须在执行查询前仔细检查你的查询语句。如果执行查询时出现错误，重写查询语句后再试。

不要对数据库执行任何DML语句（INSERT, UPDATE, DELETE, DROP等）。

如果用户的问题似乎与酒店查询无关，请礼貌地把用户引导到回来。

以下是一些对话的例子：
示例1:
用户：我想找 300-500 元之间的酒店住宿，给我一个列表。
你：好的，我会为您查找价格在 300-500 元之间的酒店住宿。
...
用户：我想找一个有游泳池的酒店。
你：好的，我会为您查找一个有游泳池子且价格在 300-500 元之间的酒店。
...

示例2:
用户：我想找一个有游泳池的酒店。
你：好的，我会为您查找一个有游泳池的酒店。
...
用户：价格在 500 元以下的。
你：好的，我会为您查找一个有游泳池且价格在 500 元以下的酒店。
...

'''

suffix = """开始!

对话历史：
{chat_history}

问题：{input}

思考：我应该查看数据库中的表格，看看我能查询什么。然后我应该查询最相关表的架构。
{agent_scratchpad}"""

agent_executor = create_sql_agent(
        llm, 
        db=db, 
        agent_type="openai-tools", 
        prefix=prefix,
        suffix=suffix,
        verbose=True,
        agent_executor_kwargs={"memory": memory}
    )

def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    response = agent_executor.invoke({"input": message})
    return response['output']

demo = gr.ChatInterface(
    predict,
    title=TITLE,
    description=DESCRIPTION,
)
demo.launch()