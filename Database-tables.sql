CREATE TABLE `users` (
   `id` int NOT NULL AUTO_INCREMENT,
   `name` varchar(100) DEFAULT NULL,
   `password` varchar(100) NOT NULL,
   `aadhar` varchar(12) NOT NULL,
   `age` int DEFAULT NULL,
   `gender` enum('Male','Female','Others') DEFAULT NULL,
   `location` varchar(100) DEFAULT NULL,
   `email` varchar(100) DEFAULT NULL,
   `reports_filed` int DEFAULT NULL,
   `selfie` mediumblob DEFAULT NULL,
   PRIMARY KEY (`id`),
   UNIQUE KEY `aadhar` (`aadhar`),
   UNIQUE KEY `name` (`name`)
 )

 CREATE TABLE `profiles` (
   `id` int NOT NULL AUTO_INCREMENT,
   `user_id` int DEFAULT NULL,
   `profile_picture` mediumblob,
   `Interests` varchar(200) DEFAULT NULL,
   `Bio` varchar(2000) DEFAULT NULL,
   PRIMARY KEY (`id`),
   KEY `user_id` (`user_id`),
   CONSTRAINT `profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
 ) 

 CREATE TABLE `photos` (
   `photo_id` int NOT NULL AUTO_INCREMENT,
   `user_id` int DEFAULT NULL,
   `photo` mediumblob,
   `upload_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`photo_id`),
   KEY `user_id` (`user_id`),
   CONSTRAINT `photos_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
 )

 CREATE TABLE friend_requests (
    request_id INT NOT NULL AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_date TIMESTAMP NULL,
    PRIMARY KEY (request_id),
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_request (sender_id, receiver_id)
);
CREATE TABLE friends (
    friendship_id INT NOT NULL AUTO_INCREMENT,
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    friendship_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (friendship_id),
    FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_friendship (user1_id, user2_id)
);

CREATE TABLE not_interested (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    not_interested_user_id INT NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (not_interested_user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_not_interested (user_id, not_interested_user_id)
);

CREATE TABLE messages (
    message_id INT NOT NULL AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message_text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (message_id),
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_chat_users (sender_id, receiver_id)
);

CREATE TABLE chat_sessions (
    session_id INT NOT NULL AUTO_INCREMENT,
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    last_message_id INT,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id),
    FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (last_message_id) REFERENCES messages(message_id) ON DELETE SET NULL
);