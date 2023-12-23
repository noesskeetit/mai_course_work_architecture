from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    user_login = Column(String(50), nullable=False, unique=True)
    user_firstname = Column(String(50), nullable=False)
    user_lastname = Column(String(50), nullable=False)
    user_email = Column(String(50), nullable=False, unique=True)
    user_password = Column(String(50), nullable=False)
    user_title = Column(String(20))
    insert_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Определение отношения один-ко-многим с GroupChatParticipants
    group_chat_participants = relationship("GroupChatParticipants", back_populates="user")
    group_chat_messages = relationship("GroupChatMessage", back_populates="user")

    # Добавление индекса на столбец user_login
    Index('idx_user_login', user_login, unique=True)


    def dict(self):
        return {
            "user_id": self.user_id,
            "user_login": self.user_login,
            "user_firstname": self.user_firstname,
            "user_lastname": self.user_lastname,
            "user_email": self.user_email,
            "user_password": self.user_password,
            "user_title": self.user_title
        }



class GroupChat(Base):
    __tablename__ = 'group_chats'

    group_chat_id = Column(Integer, primary_key=True, autoincrement=True)
    group_chat_name = Column(String(50), nullable=False)
    insert_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Определение отношения один-ко-многим с GroupChatParticipants
    group_chat_participants = relationship("GroupChatParticipants", back_populates="group_chat")

    # Определение отношения один-ко-многим с GroupChatMessage
    group_chat_messages = relationship("GroupChatMessage", back_populates="group_chat")


class GroupChatParticipants(Base):
    __tablename__ = 'group_chat_participants'

    group_chat_participant_id = Column(Integer, primary_key=True, autoincrement=True)
    group_chat_id = Column(Integer, ForeignKey('group_chats.group_chat_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)

    # Определение отношения многие-к-одному
    group_chat = relationship("GroupChat", back_populates="group_chat_participants")
    user = relationship("User", back_populates="group_chat_participants")


class GroupChatMessage(Base):
    __tablename__ = 'group_chat_messages'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('group_chats.group_chat_id'), nullable=False)
    text = Column(String(500), nullable=False)
    message_author_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Определение отношения многие-к-одному
    group_chat = relationship("GroupChat", back_populates="group_chat_messages")
    user = relationship("User", back_populates="group_chat_messages")


class PtPMessage(Base):
    __tablename__ = 'ptp_messages'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    receiver_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    text = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Определение отношения многие-к-одному
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
