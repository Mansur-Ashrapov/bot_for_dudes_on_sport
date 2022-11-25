import app.config as config

from telethon.sessions import SQLiteSession
from telethon.sync import TelegramClient
from dependency_injector import containers, providers

from app.repositories import (
    UserRepository,
    NewUserRepository,
    HistoryRepository,
    PostsRepository,
    SentMessagesRepository,
    ProxysRepositrory
)
from app.login_collector import LoginCollector
from app.database.db import CustomDatabase
from app.invites_sendler import InvitesSendler


class AppContainer(containers.DeclarativeContainer):
    db = providers.Singleton(
        CustomDatabase,
        url=config.DATABASE_URL
    )

    users_repo = providers.Factory(
        UserRepository,
        db=db
    )
    new_users_repo = providers.Factory(
        NewUserRepository,
        db=db
    )
    posts_repo = providers.Factory(
        PostsRepository,
        db=db
    )
    history_repo = providers.Factory(
        HistoryRepository,
        db=db
    )
    sent_messages_repo = providers.Factory(
        SentMessagesRepository,
        db=db
    )
    proxys_repo = providers.Factory(
        ProxysRepositrory,
        db=db
    )

    login_collector = providers.Factory(
        LoginCollector,
        new_users_repo=new_users_repo,
        posts_repo=posts_repo,
        history_repo=history_repo,
        users_repo=users_repo
        # channels_repo=channels_repo
    )

    invites_sendler = providers.Factory(
        InvitesSendler,
        new_users_repo=new_users_repo,
        users_repo=users_repo,
        sent_messages_repo=sent_messages_repo,
    )