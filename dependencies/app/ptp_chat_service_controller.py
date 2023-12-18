from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db_executor_service import get_db
from models import PtPMessage

app = FastAPI()


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
