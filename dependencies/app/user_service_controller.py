import typing

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from db_executor_service import SessionLocal
from db_executor_service import get_db
from models import User

app = FastAPI()


# Реализация сервиса пользователей
@app.post("/users/create")
async def create_user(login: str, password: str, firstname: str, lastname: str, email: str, title: str) -> typing.Dict:
    db = SessionLocal()
    try:
        # Проверка существования пользователя по user_login
        existing_user = db.query(User).filter(func.lower(User.user_login) == func.lower(login)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this login already exists")

        # Проверка существования пользователя по user_email
        existing_user_email = db.query(User).filter(func.lower(User.user_email) == func.lower(email)).first()
        if existing_user_email:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Создание нового пользователя
        user = User(
            user_login=login.strip(),
            user_password=password,
            user_firstname=firstname.strip(),
            user_lastname=lastname.strip(),
            user_email=email.strip(),
            user_title=title.strip()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except NoResultFound:
        pass
    finally:
        db.close()
    return {"status": f"User created successfully", "user_id": user.user_id}


@app.get("/users/login/{login}")
async def get_user_by_login(login: str, db: Session = Depends(get_db)) -> typing.Dict[str, typing.Any]:
    user = db.query(User).filter(User.user_login == login).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.user_id, "firstname": user.user_firstname, "lastname": user.user_lastname,
            "email": user.user_email, "title": user.user_title}


@app.get("/users/search_user_by_name_and_lastname")
async def search_user_by_name_and_lastname(firstname: str, lastname: str, db: Session = Depends(get_db)) -> typing.List[
    typing.Dict[str, typing.Any]]:
    users = db.query(User).filter(
        func.lower(User.user_firstname).like(func.lower("%" + firstname + "%")),
        func.lower(User.user_lastname).like(func.lower("%" + lastname + "%"))
    ).all()

    result = [{"user_id": user.user_id, "login": user.user_login, "firstname": user.user_firstname,
               "lastname": user.user_lastname,
               "email": user.user_email, "title": user.user_title} for user in users]
    if not users:
        raise HTTPException(status_code=404, detail="No user with this credentials")

    return result
