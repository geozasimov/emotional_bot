from utils import config

from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from aiogram import Router, F
from aiogram.types import Message

cfg = config.load()

chat = GigaChat(
    credentials=cfg.gigachat_key,
    model='GigaChat:latest',
    verify_ssl_certs=False
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Ты — высококвалифицированный специалист по развитию 
            эмоционального интеллекта. Ты обладаешь глубокими знаниями 
            в области психологического благополучия, управления эмоциями и 
            межличностных отношений. Ты помогаешь людям достигать гармонии в 
            жизни, справляться со стрессом и улучшать свою эмоциональную 
            осведомленность. Ты всегда поддерживаешь позитивное мышление и 
            предлагаешь практичные советы, которые помогают людям не только 
            развивать свои эмоции, но и поддерживать здоровый образ жизни, 
            улучшая их физическое и психоэмоциональное состояние. Каждый 
            твой ответ обязательно включает рекомендации для поддержания 
            внутренней гармонии и баланса.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = chat.invoke(prompt)
    return {"messages": response}

workflow = StateGraph(state_schema=MessagesState)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

app = workflow.compile(checkpointer=MemorySaver())

gigachat_router = Router()

@gigachat_router.message(~F.text.startswith("/"))
async def handle_chat_message(message: Message):
    user_id = message.from_user.id
    prompt = message.text
    config = {"configurable": {"thread_id": user_id}}
    input_messages = [HumanMessage(content=prompt)]
    output = await app.ainvoke({"messages": input_messages}, config)
    response = output["messages"][-1].content
    await message.answer(response)

