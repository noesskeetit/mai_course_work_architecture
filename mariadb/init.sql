-- Создание БД
CREATE DATABASE messenger_service;


-- Создание таблицы User
CREATE TABLE messenger_service.users (
    user_id VARCHAR(36) PRIMARY KEY DEFAULT UUID(),
    user_login VARCHAR(50) NOT NULL,
    user_firstname VARCHAR(50) NOT NULL,
    user_lastname VARCHAR(50) NOT NULL,
    user_email VARCHAR(50) NOT NULL,
    user_password VARCHAR(50) NOT NULL,
    user_title VARCHAR(20),
    insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_date DATETIME NULL ON UPDATE CURRENT_TIMESTAMP NOT NULL
);
-- Добавление индекса на столбец user_login
ALTER TABLE messenger_service.users ADD INDEX idx_user_login (user_login);

-- Создание таблицы GroupChat
CREATE TABLE messenger_service.group_chats (
  group_chat_id INT PRIMARY KEY AUTO_INCREMENT,
  group_chat_name VARCHAR(50) NOT NULL,
  insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  update_date DATETIME NULL ON UPDATE CURRENT_TIMESTAMP NOT NULL
);

-- Создание таблицы GroupChatParticipants
CREATE TABLE messenger_service.group_chat_participants (
  group_chat_participant_id INT PRIMARY KEY AUTO_INCREMENT,
  group_chat_id INT NOT NULL,
  user_id VARCHAR(36) DEFAULT UUID(),
  FOREIGN KEY (group_chat_id) REFERENCES group_chats(group_chat_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Создание таблицы GroupChatMessage
CREATE TABLE messenger_service.group_chat_messages (
  message_id INT PRIMARY KEY AUTO_INCREMENT,
  chat_id INT NOT NULL,
  text TEXT NOT NULL ,
  message_author_id VARCHAR(36) NOT NULL DEFAULT UUID(),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL ,
  FOREIGN KEY (chat_id) REFERENCES group_chats(group_chat_id),
  FOREIGN KEY (message_author_id) REFERENCES users(user_id)
);

-- Создание таблицы PtPMessage
CREATE TABLE messenger_service.ptp_messages (
  message_id INT PRIMARY KEY AUTO_INCREMENT,
  sender_id VARCHAR(36) NOT NULL DEFAULT UUID(),
  receiver_id VARCHAR(36) NOT NULL DEFAULT UUID(),
  text TEXT NOT NULL ,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  FOREIGN KEY (sender_id) REFERENCES users(user_id),
  FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);

-- Вставка первичных данных
INSERT INTO messenger_service.users (user_id, user_login, user_firstname, user_lastname, user_email, user_password, user_title) VALUES
('09bf30c9-f8e5-4987-bd04-e98f503778fc', 'user1', 'John', 'Doe', 'john.doe@example.com', 'password1', 'mister'),
('10bf30c9-f8e5-4987-bd04-e98f503778fc', 'user2', 'Jane', 'Doe', 'jane.doe@example.com', 'password2', 'miss'),
('11bf30c9-f8e5-4987-bd04-e98f503778fc', 'user3', 'Bob', 'Smith', 'bob.smith@example.com', 'password3', 'mister');

INSERT INTO messenger_service.group_chats (group_chat_id, group_chat_name) VALUES
(1, 'Team Chat'),
(2, 'Project Chat');

INSERT INTO messenger_service.group_chat_participants (group_chat_participant_id, group_chat_id, user_id) VALUES
(1, 1, '09bf30c9-f8e5-4987-bd04-e98f503778fc'),
(2, 1, '10bf30c9-f8e5-4987-bd04-e98f503778fc'),
(3, 2, '10bf30c9-f8e5-4987-bd04-e98f503778fc'),
(4, 2, '11bf30c9-f8e5-4987-bd04-e98f503778fc');

INSERT INTO messenger_service.group_chat_messages (message_id, chat_id, text, message_author_id) VALUES
(1, 1, 'Hello team!', '09bf30c9-f8e5-4987-bd04-e98f503778fc'),
(2, 1, 'Hi everyone!', '10bf30c9-f8e5-4987-bd04-e98f503778fc'),
(3, 2, 'Discussing project details...', '10bf30c9-f8e5-4987-bd04-e98f503778fc'),
(4, 2, 'Sure, let"s meet tomorrow.', '11bf30c9-f8e5-4987-bd04-e98f503778fc');

INSERT INTO messenger_service.ptp_messages (message_id, sender_id, receiver_id, text) VALUES
(1, '09bf30c9-f8e5-4987-bd04-e98f503778fc', '10bf30c9-f8e5-4987-bd04-e98f503778fc', 'Hey Jane, how are you?'),
(2, '10bf30c9-f8e5-4987-bd04-e98f503778fc', '11bf30c9-f8e5-4987-bd04-e98f503778fc', 'Bob, do you have the latest report?');

