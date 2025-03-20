import os
import databases
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("middle_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("profile_picture", sqlalchemy.String, default=None),
    sqlalchemy.Column("role", sqlalchemy.String)
)

resume_table = sqlalchemy.Table(
    "resume",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("email", sqlalchemy.String, sqlalchemy.ForeignKey("users.email")),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("file_path", sqlalchemy.String),
)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("Database Url is not accessible or has not being set")

engine = sqlalchemy.create_engine(DATABASE_URL)
database = databases.Database(DATABASE_URL)

async def connect_db():
    """Connecting database at startup"""
    await database.connect()

async def disconnect_db():
    """Disconnecting database at shutdown"""
    await database.disconnect()

def create_tables():
    """Creating tables in the database"""
    metadata.create_all(engine)
    print("Created tables successfully✅")
# create_tables()