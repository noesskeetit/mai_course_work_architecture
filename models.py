from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_login = Column(String(50), nullable=False, unique=True)
    user_firstname = Column(String(50), nullable=False)
    user_lastname = Column(String(50), nullable=False)
    user_email = Column(String(100), nullable=False, unique=True)
    user_password = Column(String(50), nullable=False)
    user_title = Column(String(20))
    insert_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define one-to-many relationship with GroupChatParticipants
    group_chat_participants = relationship("GroupChatParticipants", back_populates="user")


class GroupChat(Base):
    __tablename__ = 'group_chats'

    group_chat_id = Column(Integer, primary_key=True, autoincrement=True)
    group_chat_name = Column(String(50), nullable=False, unique=True)
    insert_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define one-to-many relationship with GroupChatParticipants
    group_chat_participants = relationship("GroupChatParticipants", back_populates="group_chat")

    # Define one-to-many relationship with GroupChatMessage
    group_chat_messages = relationship("GroupChatMessage", back_populates="group_chat")


class GroupChatParticipants(Base):
    __tablename__ = 'group_chat_participants'

    group_chat_participant_id = Column(Integer, primary_key=True, autoincrement=True)
    group_chat_id = Column(Integer, ForeignKey('group_chats.group_chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    # Define many-to-one relationships
    group_chat = relationship("GroupChat", back_populates="group_chat_participants")
    user = relationship("User", back_populates="group_chat_participants")


class GroupChatMessage(Base):
    __tablename__ = 'group_chat_messages'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('group_chats.group_chat_id'), nullable=False)
    text = Column(String(500), nullable=False)
    message_author_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Define many-to-one relationships
    group_chat = relationship("GroupChat", back_populates="group_chat_messages")
    user = relationship("User", back_populates="group_chat_messages")


class PtPMessage(Base):
    __tablename__ = 'ptp_messages'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    text = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Define many-to-one relationships
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])



