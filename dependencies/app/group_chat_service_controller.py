import typing

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from db_executor_service import get_db
from models import User, GroupChat, GroupChatParticipants, GroupChatMessage

app = FastAPI()


# Реализация сервиса групповых чатов

@app.post("/group_chats/create")
async def create_group_chat(chat_name: str, participants: list[int], db: Session = Depends(get_db)):
    chat = GroupChat(group_chat_name=chat_name)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    for participant_id in participants:
        participant = GroupChatParticipants(group_chat_id=chat.group_chat_id, user_id=participant_id)
        db.add(participant)

    db.commit()
    return {"group_chat_id": chat.group_chat_id}


@app.post("/group_chats/add_user")
async def add_user_to_group_chat(chat_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        # Проверка существования пользователя
        existing_user = db.query(User).filter(User.user_id == user_id).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Проверка существования участника группового чата
        existing_participant = db.query(GroupChatParticipants).filter(
            GroupChatParticipants.group_chat_id == chat_id,
            GroupChatParticipants.user_id == user_id
        ).first()
        if existing_participant:
            raise HTTPException(status_code=400, detail="User already added to group chat")

        # Добавление пользователя в групповой чат
        participant = GroupChatParticipants(group_chat_id=chat_id, user_id=user_id)
        db.add(participant)
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

    return {"status": "User successfully added to group chat", "user_id": user_id}


@app.post("/group_chats/add_message")
async def add_message_to_group_chat(chat_id: int, author: int, text: str, db: Session = Depends(get_db)):
    message = GroupChatMessage(chat_id=chat_id, message_author_id=author, text=text)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message_id": message.message_id}


@app.get("/group_chats/messages/{chat_id}")
async def get_group_chat_messages(chat_id: int, db: Session = Depends(get_db)) -> typing.List[typing.Dict]:
    messages = db.query(GroupChatMessage).filter(GroupChatMessage.chat_id == chat_id).all()
    result = [{"message_id": message.message_id, "text": message.text, "author": message.message_author_id,
               "timestamp": message.timestamp} for message in messages]
    return result
