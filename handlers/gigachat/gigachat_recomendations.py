from utils import config

from langchain_core.messages import HumanMessage
from langchain_gigachat import GigaChat
from langchain.prompts import PromptTemplate

cfg = config.load()

chat = GigaChat(
    credentials=cfg.gigachat_key,
    model='GigaChat:latest',
    verify_ssl_certs=False
)

emotion_template = PromptTemplate(
    input_variables=["age", "gender"],
    template="""Ты очень хороший специалист по развитию эмоционального интеллекта, ты отлично знаешь как давать правильные
    рекомендации индивидуально для каждого, учитывая пол, возраст человека.

    Данные пользователя:
    - Возраст: {age} лет
    - Пол: {gender}
   

    Ты должен:
    1. Генерировать советы по развитию эмоционального интеллекта.
    2. Генерировать мотивационнные сообщения.
    3. Определять эмоции.
    
    Ответ дай БЕЗ каких-либо формул, потому что твой ответ не получится отформатировать.
    Ответ начни с фразы: *Вот ваши рекомендации по развитию эмоционального интеллекта:*.
    """
)



async def emotion_recommendations(age, gender):
    prompt = emotion_template.format(
        age=age,
        gender=gender,
    )

    result = chat.invoke([HumanMessage(content=prompt)])
    return result.content


