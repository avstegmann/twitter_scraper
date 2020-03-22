import GetOldTweets3 as got
import csv
import datetime
import re
import time
from urlextract import URLExtract


extractor = URLExtract()


def create_file(file_name):
    csv_columns = ['Username', 'Date', 'Text', 'Hashtags', 'url']
    with open(file_name, 'a', encoding='UTF-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='|')
        writer.writeheader()
        csvfile.close()


def save_tweets(tweets, csv_file):
    csv_columns = ['Username', 'Date', 'Text', 'Hashtags', 'url']
    print('------------------')
    with open(csv_file, 'a', encoding='UTF-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='|')
        # writer.writeheader()
        for data in tweets:
            writer.writerow(data)
        csvfile.close()


def get_tweets(term, start_date, days, file_name):
    term = term + ' -filter:retweets'
    start = start_date
    since = start - datetime.timedelta(days=1)
    until = start_date - datetime.timedelta(days=days)
    counter = 0
    while start > until:
        tweets = []
        startcriteria = str(start)
        sincecriteria = str(since)
        print('Start:  ' + startcriteria)
        tweetcriteria = got.manager.TweetCriteria().setQuerySearch(term).setSince(sincecriteria).setUntil(startcriteria)
        try:
            for item in got.manager.TweetManager.getTweets(tweetcriteria):
                tweet = {'Username': re.sub('[|";]', '', item.username), 'Date': item.date,
                         'Text': re.sub('[|";]', '', item.text), 'Hashtags': re.sub('[|";]', '', item.hashtags),
                         'url': extractor.find_urls(item.text)}
                tweets.append(tweet)
            print('Finish: ' + sincecriteria)
            save_tweets(tweets, file_name)
            start = start - datetime.timedelta(days=1)
            since = start - datetime.timedelta(days=1)
            counter += 1
            if counter == 5:
                print('-> break <-')
                counter = 0
                time.sleep(100)
                pass
        except:
            print('-> error break <-')
            time.sleep(10)
            pass
    return print('done')


def main():
    term = input('Search term:\n')
    year = int(input('Year:\n'))
    month = int(input('Month:\n'))
    day = int(input('Day:\n'))
    start_date = datetime.date(year, month, day)
    days = int(input('How many days:\n'))
    file_name = input('Write new file name.\n')
    if len(file_name.split('.')) == 1:
        file_name += '.csv'
    try:
        f = open(file_name)
        f.close()
    except IOError:
        create_file(file_name)
    get_tweets(term, start_date, days, file_name)


if __name__ == '__main__':
    main()
