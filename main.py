import typing

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, GroupChat, GroupChatParticipants, GroupChatMessage, PtPMessage

# Инициализация базы данных и подключение к MariaDB
DATABASE_URL = "mysql+mysqlconnector://root:root@mariadb:3306/dbname"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Зависимость для создания сессии базы данных для каждого запроса
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Реализация сервиса пользователей
@app.post("/users/create")
async def create_user(login: str, password: str, firstname: str, lastname: str, email: str, title: str) -> typing.Dict:
    db = SessionLocal()
    user = User(
        user_login=login,
        user_password=password,
        user_firstname=firstname,
        user_lastname=lastname,
        user_email=email,
        user_title=title
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"status": "User created successfully"}


@app.get("/users/{login}")
async def get_user_by_login(login: str, db: Session = Depends(get_db)) -> typing.Dict[User.user_id, User.user_firstname, User.user_lastname, User.user_email, User.user_title]:
    user = db.query(User).filter(User.user_login == login).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.user_id, "firstname": user.user_firstname, "lastname": user.user_lastname,
            "email": user.user_email, "title": user.user_title}


'''Уточнить тип возвращаемого'''


@app.get("/users/search_user_by_name_and_lastname")
async def search_user_by_name_and_lastname(firstname: str, lastname: str, db: Session = Depends(get_db)) -> typing.List[typing.Dict[str, typing.Any]]:
    users = db.query(User).filter(User.user_firstname.ilike(f"%{firstname}%"),
                                  User.user_lastname.ilike(f"%{lastname}%")).all()
    result = [{"login": user.user_login, "firstname": user.user_firstname, "lastname": user.user_lastname,
               "email": user.user_email, "title": user.user_title} for user in users]
    return result


# Реализация сервиса групповых чатов
@app.post("/group_chats/create")
async def create_group_chat(chat_name: str, participants: list, db: Session = Depends(get_db)):
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
    participant = GroupChatParticipants(group_chat_id=chat_id, user_id=user_id)
    db.add(participant)
    db.commit()
    return {"status": "User added to group chat successfully"}


@app.post("/group_chats/add_message")
async def add_message_to_group_chat(chat_id: int, author: int, text: str, db: Session = Depends(get_db)):
    message = GroupChatMessage(chat_id=chat_id, message_author_id=author, text=text)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message_id": message.message_id}


@app.get("/group_chats/messages/{chat_id}")
async def get_group_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = db.query(GroupChatMessage).filter(GroupChatMessage.chat_id == chat_id).all()
    result = [{"message_id": message.message_id, "text": message.text, "author": message.message_author_id,
               "timestamp": message.timestamp} for message in messages]
    return result


# Реализация сервиса PtP чатов
@app.post("/ptp_messages/send")
async def send_ptp_message(sender: int, receiver: int, text: str, db: Session = Depends(get_db)):
    message = PtPMessage(sender_id=sender, receiver_id=receiver, text=text)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message_id": message.message_id}


@app.get("/ptp_messages/{user_id}")
async def get_ptp_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(PtPMessage).filter(PtPMessage.receiver_id == user_id).all()
    result = [{"message_id": message.message_id, "text": message.text, "sender": message.sender_id,
               "timestamp": message.timestamp} for message in messages]
    return result
