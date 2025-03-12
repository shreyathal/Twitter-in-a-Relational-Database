# import statements
from twitter_api import TwitterAPI
import time


def load_tweets(api=TwitterAPI, file_path='/Users/shreyathalvayapati/Desktop/DS4300/tweet.csv'):
    '''
    loads tweets from csv file and determines the load rate
    :param api: the Twitter api imported from separate file
    :param file_path: path to where the csv file with relevant data is located
    :return: nothing, just loads data and prints out the rate
    '''

    # before any tweets are loaded
    start_time = time.time()
    tweet_count = 0

    # iterates through each row of CSV and load into relevant SQL table
    with open(file_path, 'r', encoding='utf-8') as file:

        # skips the header row
        next(file)

        for row in file:
            user_id, tweet_text = row.strip().split(',')
            api.insert_tweet(user_id, tweet_text)
            # add one to the tweet count for each row
            tweet_count += 1

    # after all the rows have been iterated through
    end_time = time.time()
    time_taken = end_time - start_time

    # POST tweets/sec calculation
    tweets_per_second = tweet_count / time_taken if time_taken > 0 else 0
    print(f'Tweets per second: {tweets_per_second:.2f}')


def measure_home_timeline_speed(api):
    '''
    calculates how many home timelines can be retrieved per second
    :param api: the imported twitter_api (provided as a parameter for the sake of abstraction)
    :return: nothing, just computes speed of retrieval and prints calculation
    '''

    # fetch random user IDs from the database (just one in this case, to not overwhelm computer)
    random_user_ids = [api.fetch_random_user_id() for _ in range(1)]

    # before any home timelines are retrieved
    start_time = time.time()
    timeline_count = 0

    # retrieve home timelines of choosen random users
    for random_user in random_user_ids:
        home_timeline = api.get_home_timeline(random_user)

        # process or print the home_timeline (modify as needed)
        print(f'Home Timeline for User {random_user}: {home_timeline}')

        timeline_count += 1

    end_time = time.time()

    # total time taken to retrieve all 5 home timelines
    time_taken = end_time - start_time

    # calculate how many timelines are retrieved in one second
    timelines_per_second = timeline_count / time_taken if time_taken > 0 else 0

    print(f'Timelines per second: {timelines_per_second:.2f}')


def main():

    # log in details
    db_params = {
        'username': 'root',
        'password': 'Huskiesuntil2025!',
        'host': '127.0.0.1',
        'database': 'Twitter_DB',
    }

    # initiate API
    api = TwitterAPI(db_params)

    # pass in API to the two main functions
    load_tweets(api)
    measure_home_timeline_speed(api)


if __name__ == "__main__":
    main()
