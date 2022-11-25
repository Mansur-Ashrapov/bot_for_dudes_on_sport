from app.repositories.user_rep import UserRepository
from app.repositories.new_user_rep import NewUserRepository
from app.repositories.history_rep import HistoryRepository
from app.repositories.post_rep import PostsRepository
from app.repositories.sent_messages_rep import SentMessagesRepository
from app.repositories.proxys_rep import ProxysRepositrory


__all__ = ('UserRepository', 'NewUserRepository', 'HistoryRepository', 'PostsRepository', 'SentMessagesRepository', 'ProxysRepositrory')