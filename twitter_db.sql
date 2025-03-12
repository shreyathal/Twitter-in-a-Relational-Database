CREATE DATABASE Twitter_DB;
USE Twitter_DB; 

-- Create FOLLOWS table
CREATE TABLE FOLLOWS (
    user_id INT,
    follows_id INT,
    PRIMARY KEY (user_id, follows_id)
);

-- Create TWEET table
CREATE TABLE TWEET (
    tweet_id INT PRIMARY KEY,
    user_id INT,
    tweet_ts DATETIME,
    tweet_text VARCHAR(140),
    FOREIGN KEY (user_id) REFERENCES FOLLOWS(user_id) ON DELETE CASCADE
);

ALTER TABLE TWEET
MODIFY COLUMN tweet_id INT AUTO_INCREMENT;

ALTER TABLE TWEET
DROP FOREIGN KEY tweet_ibfk_1;

