# Проектное задание
Бот создан для развития эмоционального интеллекта с помощью GigaChat. Проект выполнен в рамках научно-исследовательского семинара "Искусственный интеллект в инженерном образовании" МИЭМ НИУ ВШЭ студентами группы БИВ234:
- Чибировым Русланом
- Засимовым Георгием.

# Блок-схема
[Посмотреть блок-схему]()

![scheme](Scheme.drawio)

# Как запустить
## Telegram bot
@emotional_intelligence1_Bot

## Для разработчиков
```
git clone https://github.com/geozasimov/emotional_bot
cd emotional_bot
```
Добавьте свою конфигурацию в .env файл, а точнее параметры базы данных, токен Gigachat от сбер и токен телеграмм бота от BotFather

Пример файла .env:
```
POSTGRES_PASSWORD=...

POSTGRES_USER=...

POSTGRES_DB=...

POSTGRES_HOST=...

POSTGRES_PORT=...

TELEGRAM_TOKEN="..."

GIGACHAT_KEY="..."
```
запустить бота:
```
docker-compose run migrate
docker-compose up --build
```



