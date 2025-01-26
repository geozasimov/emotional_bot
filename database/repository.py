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

async def add_user(user_id, name, age, gender):
    query = """
    INSERT INTO users (user_id, name, age, gender)
    VALUES ($1, $2, $3, $4)
    """
    await db.execute(query, user_id, name, age, gender)

async def get_user(user_id):
    query = """
    SELECT * FROM users WHERE user_id = $1
    """
    result = await db.fetch(query, user_id)
    return result


async def save_action(user_id, username, action_type, message, timestamp):
    query = """
    INSERT INTO user_actions (user_id, username, action_type, message, timestamp)
    VALUES ($1, $2, $3, $4, $5)
    """
    await db.execute(query, user_id, username, action_type, message, timestamp)
