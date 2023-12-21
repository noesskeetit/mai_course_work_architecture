from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event
from models import Base
from random import choice
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


# Подключение шардинга: Реализовано засчет прослушки движка на определенное событие
@event.listens_for(Engine, "before_cursor_execute", retval=True)
def comment_sql_calls(conn, cursor, statement, parameters,
                      context, executemany):
    if statement.startswith('INSERT INTO users'):
        target = parameters.get("user_id")
        hash_target = hash(target) % 2
        print(hash_target)
        if hash_target % 2 == 0:
            comment = ' /*sharding 0*/;'
        else:
            comment = ' /*sharding 1*/;'
        statement = statement + comment
        return statement, parameters

    # elif ('SELECT' and 'WHERE users.user_login = %(user_login_1)s' and 'LIMIT %(param_1)s') in statement:
    #     for sharding_node in db_nodes:
    #         sharding_node = f' /*sharding {sharding_node}*/;'
    #         print(statement)
    #         print(sharding_node)
    #         statement = statement + sharding_node
    #         return statement, parameters

    else:
        return statement, parameters
