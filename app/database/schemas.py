import datetime

from dataclasses import dataclass


@dataclass
class PostDataclass:
    channel: str
    post_id: int
    last_id_comm: int


@dataclass
class NewUserDataclassIn:
    user_id: int
    username: str
    channel_from: str
    post_id: int

@dataclass
class NewUserDataclassOut(NewUserDataclassIn):
    add_date: datetime.datetime 


@dataclass
class UserDataclass:
    user_id: int


@dataclass
class PostHistoryDataclassIn:
    channel: str
    post_id: int
    count_new_users_post: int


@dataclass
class PostHistoryDataclassOut(PostHistoryDataclassIn):
    last_check_date: datetime.datetime 


@dataclass 
class SentMessagesDataclassIn:
    from_client: int
    participant_id: int


@dataclass
class SentMessagesDataclassOut(SentMessagesDataclassIn):
    sent_date: datetime.datetime


@dataclass
class TelegramClientDataclass:
    username: str
    api_hash: str
    api_id: str
    # proxy_id: int
