# import statements
import mysql.connector
import random

class TwitterAPI:
    def __init__(self, db_params):
        '''
        class to represent a Tweet
        :param db_params: dictionary containing database connection parameters
        '''
        self.conn = self.create_connection(**db_params)

    def create_connection(self, username, password, host, database):
        '''
        establishes connections to previously created database
        '''
        return mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )

    def fetch_random_user_id(self):
        '''
        fetches a random user ID from the "FOLLOWS" table in the SQL database
        :return: a random user ID or None if no result
        '''
        c = self.conn.cursor(buffered=True)

        # execute a query to fetch a random user ID from the "FOLLOWS" table
        query = "SELECT User_ID FROM FOLLOWS ORDER BY RAND(%s)"
        seed_value = random.random()  # use a random seed value for better performance
        c.execute(query, (seed_value,))

        # fetch the result
        result = c.fetchone()
        random_user_id = result[0] if result else None

        # close the cursor to clear the result set
        c.close()

        return random_user_id

    def insert_tweet(self, user_id, text):
        '''
        inserts tweet into Tweet SQL table
        :param user_id: the user the tweet is written by
        :param text: the text of the tweet
        :return: nothing, just inserts tweet into the database table
        '''
        c = self.conn.cursor()
        c.execute('INSERT INTO TWEET (user_id, tweet_text) VALUES (%s, %s)', (user_id, text))
        self.conn.commit()

    def get_home_timeline(self, user_id):
        '''
        returns a user's home timeline
        :param user_id: to identify the specific Twitter user
        :return: the user's (the person associated with the user-id) home timeline
        '''

        c = self.conn.cursor(buffered=True)

        # fetching the 10 most recent tweets posted by users followed by this specific user
        c.execute('''
                  SELECT TWEET.user_id, TWEET.tweet_text, TWEET.tweet_ts
                  FROM TWEET
                  WHERE TWEET.user_id IN (
                      SELECT TWEET.user_id FROM TWEET WHERE TWEET.user_id != %s
                      ORDER BY TWEET.tweet_ts
                  )
                  ORDER BY TWEET.tweet_ts
                  ''', (user_id,))

        result = c.fetchall()

        # close the cursor to clear the result set
        c.close()

        return result


