from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event
from models import Base

# Инициализация базы данных и подключение к MariaDB
engine = create_engine("mysql+pymysql://root:root@proxysql:6033/messenger_service")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Создадим генератор для сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@event.listens_for(Engine, "before_cursor_execute", retval=True)
def comment_sql_calls(conn, cursor, statement, parameters,
                      context, executemany):

    if statement == '''INSERT INTO users (user_id, user_login, user_firstname, user_lastname, user_email, user_password, user_title, insert_date, update_date) VALUES (%(user_id)s, %(user_login)s, %(user_firstname)s, %(user_lastname)s, %(user_email)s, %(user_password)s, %(user_title)s, %(insert_date)s, %(update_date)s)''':
        target = parameters.get("user_id")
        hash_target = hash(target) % 2
        print(hash_target)
        if hash_target % 2 == 0:
            comment = ' /*sharding 0*/;'
        else:
            comment = ' /*sharding 1*/;'
        statement = statement + comment
        print(statement)
    return statement, parameters
