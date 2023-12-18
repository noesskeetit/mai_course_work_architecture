-- Создание БД
CREATE DATABASE messenger_service;


-- Создание таблицы User
CREATE TABLE messenger_service.User (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  user_login VARCHAR(50) NOT NULL UNIQUE,
  user_firstname VARCHAR(50) NOT NULL,
  user_lastname VARCHAR(50) NOT NULL,
  user_email VARCHAR(50) NOT NULL UNIQUE,
  user_password VARCHAR(50) NOT NULL,
  user_title VARCHAR(20),
  insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL ,
  update_date DATETIME NULL ON UPDATE CURRENT_TIMESTAMP NOT NULL
);

-- Создание таблицы GroupChat
CREATE TABLE messenger_service.GroupChat (
  group_chat_id INT PRIMARY KEY AUTO_INCREMENT,
  group_chat_name VARCHAR(50) NOT NULL,
  insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  update_date DATETIME NULL ON UPDATE CURRENT_TIMESTAMP NOT NULL
);

-- Создание таблицы GroupChatParticipants
CREATE TABLE messenger_service.GroupChatParticipants (
  group_chat_participant_id INT PRIMARY KEY AUTO_INCREMENT,
  group_chat_id INT NOT NULL,
  user_id INT,
  FOREIGN KEY (group_chat_id) REFERENCES GroupChat(group_chat_id),
  FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Создание таблицы GroupChatMessage
CREATE TABLE messenger_service.GroupChatMessage (
  message_id INT PRIMARY KEY AUTO_INCREMENT,
  chat_id INT NOT NULL,
  text TEXT NOT NULL ,
  message_author_id INT NOT NULL ,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL ,
  FOREIGN KEY (chat_id) REFERENCES GroupChat(group_chat_id),
  FOREIGN KEY (message_author_id) REFERENCES User(user_id)
);

-- Создание таблицы PtPMessage
CREATE TABLE messenger_service.PtPMessage (
  message_id INT PRIMARY KEY AUTO_INCREMENT,
  sender_id INT NOT NULL,
  receiver_id INT NOT NULL,
  text TEXT NOT NULL ,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  FOREIGN KEY (sender_id) REFERENCES User(user_id),
  FOREIGN KEY (receiver_id) REFERENCES User(user_id)
);

-- Вставка первичных данных
INSERT INTO messenger_service.User (user_id, user_login, user_firstname, user_lastname, user_email, user_password, user_title) VALUES
(1, 'user1', 'John', 'Doe', 'john.doe@example.com', 'password1', 'mister'),
(2, 'user2', 'Jane', 'Doe', 'jane.doe@example.com', 'password2', 'miss'),
(3, 'user3', 'Bob', 'Smith', 'bob.smith@example.com', 'password3', 'mister');

INSERT INTO messenger_service.GroupChat (group_chat_id, group_chat_name) VALUES
(1, 'Team Chat'),
(2, 'Project Chat');

INSERT INTO messenger_service.GroupChatParticipants (group_chat_participant_id, group_chat_id, user_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 2),
(4, 2, 3);

INSERT INTO messenger_service.GroupChatMessage (message_id, chat_id, text, message_author_id) VALUES
(1, 1, 'Hello team!', 1),
(2, 1, 'Hi everyone!', 2),
(3, 2, 'Discussing project details...', 2),
(4, 2, 'Sure, let"s meet tomorrow.', 3);

INSERT INTO messenger_service.PtPMessage (message_id, sender_id, receiver_id, text) VALUES
(1, 1, 2, 'Hey Jane, how are you?'),
(2, 2, 3, 'Bob, do you have the latest report?');
