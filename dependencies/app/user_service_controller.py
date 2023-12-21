import typing
import uuid
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db_executor_service import get_db
from models import User

app = FastAPI()


# Реализация сервиса пользователей
@app.post("/users/create")
async def create_user(login: str, password: str, firstname: str, lastname: str, email: str, title: str,
                      db: Session = Depends(get_db)) -> typing.Dict:
    user_id = uuid.uuid4()
    try:
        # Проверка существования пользователя по user_login
        is_exist_login(' /*sharding 0*/;', login, db)
        is_exist_login(' /*sharding 1*/;', login, db)

        # Проверка существования пользователя по user_email
        is_exist_email(' /*sharding 0*/;', email, db)
        is_exist_email(' /*sharding 1*/;', email, db)

        # Создание нового пользователя
        user = User(
            user_id=str(user_id),
            user_login=login.strip(),
            user_password=password,
            user_firstname=firstname.strip(),
            user_lastname=lastname.strip(),
            user_email=email.strip(),
            user_title=title.strip()
        )
        db.add(user)
        db.commit()

    except NoResultFound:
        pass
    finally:
        db.close()
    return {"status": f"User created successfully", "user_id": user_id}


@app.get("/users/login/{login}")
async def get_user_by_login(login: str, db: Session = Depends(get_db)):
    list_from_1st_sharding_node = get_users_by_login_from_db(' /*sharding 0*/;', login, db)
    list_from_2nd_sharding_node = get_users_by_login_from_db(' /*sharding 1*/;', login, db)

    list_from_1st_sharding_node.extend(list_from_2nd_sharding_node)

    if not list_from_1st_sharding_node:
        raise HTTPException(status_code=404, detail="User not found")

    return list_from_1st_sharding_node[0]


@app.get("/users/search_user_by_name_and_lastname")
async def search_user_by_name_and_lastname(firstname: str, lastname: str, db: Session = Depends(get_db)) -> typing.List[typing.Dict[str, typing.Any]]:
    list_from_1st_sharding_node = get_users_by_firstname_and_lastname(' /*sharding 0*/;', firstname_mask=firstname, lastname_mask=lastname, db=db)
    list_from_2nd_sharding_node = get_users_by_firstname_and_lastname(' /*sharding 1*/;', firstname_mask=firstname, lastname_mask=lastname, db=db)

    list_from_1st_sharding_node.extend(list_from_2nd_sharding_node)

    if not list_from_1st_sharding_node:
        raise HTTPException(status_code=404, detail="No users with this credentials")

    return list_from_1st_sharding_node


def is_exist_login(sharding_node: str, login: str, db) -> None:
    existing_user_query = text(
        f"SELECT count(*) FROM messenger_service.users WHERE users.user_login = :login {sharding_node}")
    params = {'login': login}
    result = db.execute(existing_user_query, params)
    if result.fetchone()[0] > 0:
        raise HTTPException(status_code=400, detail="User with this login already exists")


def is_exist_email(sharding_node: str, email: str, db) -> None:
    existing_email_query = text(
        f"SELECT count(*) FROM messenger_service.users WHERE users.user_email = :email {sharding_node}")
    params = {'email': email}
    result = db.execute(existing_email_query, params)
    if result.fetchone()[0] > 0:
        raise HTTPException(status_code=400, detail="User with this email already exists")


def get_users_by_login_from_db(sharding_node: str, login: str, db) -> typing.List:
    existing_user_by_login_query = text(
        f"SELECT user_id, user_firstname, user_lastname, user_email, user_title FROM messenger_service.users WHERE users.user_login = :login {sharding_node}")

    params = {'login': login}
    result = db.execute(existing_user_by_login_query, params)

    user_objects = []
    for row in result:
        print(row)
        user = User()
        user.user_id = row[0]
        user.user_firstname = row[1]
        user.user_lastname = row[2]
        user.user_email = row[3]
        user.user_title = row[4]
        user_objects.append(user)
        print(user_objects)
    return user_objects



def get_users_by_firstname_and_lastname(sharding_node: str, firstname_mask: str, lastname_mask: str,  db):
    existing_user_by_name_and_lastname_query = text(
        f"SELECT user_id, user_login, user_firstname, user_lastname, user_email, user_title FROM messenger_service.users WHERE users.user_firstname like :%firstname_mask% and users.user_lastname like :%lastname_mask% {sharding_node}")

    params = {'firstname_mask': firstname_mask, 'lastname_mask':  lastname_mask}
    result = db.execute(existing_user_by_name_and_lastname_query, params)
    result = result.fetchall()



    user_objects = []
    for row in result:
        user = User()
        user.user_id = row[0]
        user.user_login = row[1]
        user.user_firstname = row[2]
        user.user_lastname = row[3]
        user.user_email = row[4]
        user.user_title = row[5]
        user_objects.append(user)

    return user_objects
