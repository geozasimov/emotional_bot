from database.postgres import Database
from utils import config
from datetime import datetime

cfg = config.load()

db = Database(cfg)

async def read_parameter(user_id, field):
    res = await db.fetch(f'SELECT {field} FROM users WHERE user_id = $1', user_id)
    if res:
        return res[0][field]
    return None

async def update_parameter(user_id, field, value):
    query = f"UPDATE users SET {field} = $1 WHERE user_id = $2"
    await db.execute(query, value, user_id)

async def add_user(user_id, name, age, gender, height, weight, timezone):
    query = """
    INSERT INTO users (user_id, name, age, gender, height, weight, timezone)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    """
    await db.execute(query, user_id, name, age, gender, height, weight, timezone)

async def get_user(user_id):
    query = """
    SELECT * FROM users WHERE user_id = $1
    """
    result = await db.fetch(query, user_id)
    return result

async def save_emotion_data(user_id, data):
    query = """
    INSERT INTO daily_survey (user_id, survey_date, physical_activity, stress, mood, sleep_quality)
    VALUES ($1, $2, $3, $4, $5, $6)
    """
    await db.execute(query, user_id, data['survey_date'], data['physical_activity'], data['stress'], data['mood'], data['sleep_quality'])

async def save_monthly_emotion_data(user_id, data):
    query = """
    INSERT INTO monthly_survey (user_id, survey_date, bot, support, updates)
    VALUES ($1, $2, $3, $4, $5)
    """
    await db.execute(query, user_id, data['survey_date'], data['mark1'], data['mark2'], data['mark3'])

async def get_weekly_emotion_data(user_id, field):
    query = f"""
    SELECT survey_date, {field} FROM daily_survey
    WHERE user_id = $1 AND survey_date >= now() - interval '7 days'
    ORDER BY survey_date ASC
    """
    data = await db.fetch(query, user_id)
    if data:
        return data
    return None


async def save_action(user_id, username, action_type, message, timestamp):
    query = """
    INSERT INTO user_actions (user_id, username, action_type, message, timestamp)
    VALUES ($1, $2, $3, $4, $5)
    """
    await db.execute(query, user_id, username, action_type, message, timestamp)
