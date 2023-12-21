import typing
import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from user_sharding_methods import get_users_by_login_from_db, get_users_by_firstname_and_lastname, is_exist_user_id, \
    is_exist_login, \
    is_exist_email
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db_executor_service import get_db
from models import User

app = FastAPI()


# Реализация сервиса пользователей
# Создание нового пользователя
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


# Поиск по логину
@app.get("/users/login/{login}")
async def get_user_by_login(login: str, db: Session = Depends(get_db)):
    list_from_1st_sharding_node = get_users_by_login_from_db(' /*sharding 0*/;', login, db)
    list_from_2nd_sharding_node = get_users_by_login_from_db(' /*sharding 1*/;', login, db)

    list_from_1st_sharding_node.extend(list_from_2nd_sharding_node)

    if not list_from_1st_sharding_node:
        raise HTTPException(status_code=404, detail="User not found")

    return list_from_1st_sharding_node[0]


# Поиск по маске имени и фамилии
@app.get("/users/search_user_by_name_and_lastname")
async def search_user_by_name_and_lastname(firstname: str, lastname: str, db: Session = Depends(get_db)):
    list_from_1st_sharding_node = get_users_by_firstname_and_lastname(' /*sharding 0*/;', firstname_mask=firstname,
                                                                      lastname_mask=lastname, db=db)
    list_from_2nd_sharding_node = get_users_by_firstname_and_lastname(' /*sharding 1*/;', firstname_mask=firstname,
                                                                      lastname_mask=lastname, db=db)

    list_from_1st_sharding_node.extend(list_from_2nd_sharding_node)

    if not list_from_1st_sharding_node:
        raise HTTPException(status_code=404, detail="No users with this credentials")

    return list_from_1st_sharding_node


# Update пользователя

@app.put("/users/update/{user_id}")
async def update_user(user_id: str, login: str, password: str, firstname: str, lastname: str, email: str, title: str,
                      db: Session = Depends(get_db)) -> typing.Dict:
    try:
        # Получение пользователя по user_id
        list_from_1st_sharding_node = is_exist_user_id(' /*sharding 0*/;', user_id, db)
        list_from_2nd_sharding_node = is_exist_user_id(' /*sharding 1*/;', user_id, db)

        list_from_1st_sharding_node.extend(list_from_2nd_sharding_node)
        user = list_from_1st_sharding_node[0]
        if user and (is_exist_email(' /*sharding 0*/;', email, db) and is_exist_email(' /*sharding 1*/;', email, db)):
            # Обновление данных пользователя с использованием SQL-запроса
            query = text(f'UPDATE users SET user_login = :login, user_password = :password, user_firstname = :firstname, user_lastname = :lastname, user_email = :email, user_title = :title WHERE user_id = :user_id /*sharding {hash(user_id) % 2}*/;')
            params = {'login': login.strip(), 'password': password, "firstname": firstname.strip(), 'lastname': lastname.strip(), "email": email.strip(), "title": title.strip(), "user_id": user_id}

            db.execute(query, params)
            # Коммит изменений в базе данных
            db.commit()

        return {"status": f"User updated successfully", "user_id": user_id}

    except Exception as e:
        # Обработка ошибок при обновлении пользователя
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

    finally:
        # Закрытие соединения с базой данных
        db.close()
