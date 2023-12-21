import typing

from fastapi import HTTPException
from sqlalchemy import text

from models import User




def is_exist_user_id(sharding_node: str, user_id: str, db) -> typing.List:
    existing_user_id_query = text(
        f"SELECT user_login, user_password, user_firstname, user_lastname, user_email, user_title, user_id FROM messenger_service.users WHERE users.user_id = :user_id {sharding_node}")

    params = {'user_id': user_id}
    result = db.execute(existing_user_id_query, params)

    user_objects = []

    for row in result:

        user = User()

        user.user_login = row[0]
        user.user_password = row[1]
        user.user_firstname = row[2]
        user.user_lastname = row[3]
        user.user_email = row[4]
        user.user_title = row[5]
        user.user_id = row[6]
        user_objects.append(user)

    return user_objects


def is_exist_login(sharding_node: str, login: str, db) -> None:
    existing_user_login_query = text(
        f"SELECT count(*) FROM messenger_service.users WHERE users.user_login = :login {sharding_node}")
    params = {'login': login}
    result = db.execute(existing_user_login_query, params)
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

        user = User()

        user.user_id = row[0]
        user.user_firstname = row[1]
        user.user_lastname = row[2]
        user.user_email = row[3]
        user.user_title = row[4]
        user_objects.append(user)

    return user_objects



def get_users_by_firstname_and_lastname(sharding_node: str, firstname_mask: str, lastname_mask: str,  db):
    existing_user_by_name_and_lastname_query = text(
        f"SELECT user_id, user_login, user_firstname, user_lastname, user_email, user_title FROM messenger_service.users WHERE users.user_firstname like :firstname_mask and users.user_lastname like :lastname_mask {sharding_node}")

    params = {'firstname_mask': f"%{firstname_mask}%", 'lastname_mask':  f"%{lastname_mask}%"}
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
