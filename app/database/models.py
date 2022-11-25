from sqlalchemy import BigInteger, Column, Integer, String, Table, DateTime, Boolean
from sqlalchemy.sql import func

from app.database.db import metadata


User = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('user_id', BigInteger, unique=True)
)

NewUser = Table(
    'new_users',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('user_id', BigInteger, unique=True),
    Column('channel_from', String),
    Column('post_id', BigInteger),
    Column('username', String),
    Column('add_date', DateTime, default=func.now()) 
)

Post = Table(
    'posts',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('channel', String),
    Column('post_id', BigInteger),
    Column('last_id_comm', BigInteger, default=0)
)

History = Table(
    'history',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('channel', String),
    Column('post_id', BigInteger),
    Column('count_new_users_post', Integer),
    Column('last_check_date', DateTime, default=func.now(), onupdate=func.now())
)

SentMessages = Table(
    'sent_messages',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('from_client', BigInteger),
    Column('participant_id', BigInteger),
    Column('sent_date', DateTime, default=func.now())
)

Proxy = Table(
    'proxys',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('addr', String),
    Column('port', Integer),
    Column('login', String),
    Column('password', String)
)