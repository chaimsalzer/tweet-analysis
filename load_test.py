from TwitterAPI import TwitterAPI
import json
import pprint
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime
import politicians
import time
import tweet_mail

test = ['@alfranken','@amyklobuchar', '@SenAngusKing', '@SenatorBoxer', '@SenatorBarb']

#max = 180

#should be 100
all_politicians = politicians.us_house+politicians.us_senate

#reduce to one measurement per day
# test with integrated mail sender.
#dummy values test

CONSUMER_KEY = 'D3ffNafoksntbQNRIUR9GwWZh'
CONSUMER_SECRET = 'SMTjPzDbybBCFzBXPzHb5dn7DwrIfQev92fnloeWwQctaF23BM'
ACCESS_TOKEN_KEY = '2646985382-G1T7rnwoTrvETulIC8LDLRSO6PSz3eM0mFh0hGx'
ACCESS_TOKEN_SECRET = '46g24926lCBtV1oXfcsE3rrdw7aRSC7dexN88H249CgMz'
api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
pp = pprint.PrettyPrinter(indent=4)


def start():
    request_num = 0

    with open('data.json', 'r') as f:
        j_data = json.load(f)
        print('json data loaded')
        key = (len(j_data['sample']))
        today = str(datetime.date.today())
        j_data['sample'].append({"date":today})

        for query in test:
            request_num += 1
            if request_num == 180:
                print('waiting for 15 minutes...')
                #sleep 15 minutes after 180 requests
                time.sleep(905)
                print('finished waiting')
            r = api.request('users/show', {'screen_name': query})
            data = (json.loads(r.text))

            j_data['sample'][key][query] = {
                'name': data['name'],
                'followers_count': data['followers_count'],
                'friends_count':data['friends_count'],
                'listed_count':data['listed_count'],
                'statuses_count':data['statuses_count'],
                'tweets': {}}
            print('connecting to twitter...',request_num)
            tweet_list = get_tweets(query,today)
            i = 0
            for tweet_data in tweet_list:
                j_data['sample'][key][query]['tweets'][i] = {
                    'tweetID': tweet_data['tweetID'],
                    'created_at': tweet_data['created_at'],
                    'text': tweet_data['text'],
                    'textblob': tweet_data['textblob'],
                    'NLTK': tweet_data['NLTK'],
                    'RT': tweet_data['RT'],
                    'others': tweet_data['others']
                }
                i += 1

    with open('data.json', 'w') as f:
        f.write(json.dumps(j_data))
        tweet_mail.tweet_mail()


def get_tweets(q,today):
    r = api.request('search/tweets', {'q': "%s since:%s" %(q,today),'count': '100','result_type': 'recent','lang':'en'})
    data = (json.loads(r.text))['statuses']
    sid = SentimentIntensityAnalyzer()
    all_tweets = []
    for i in range(0, len(data)):
        text = data[i]['text'].encode('ascii','ignore').decode('ascii')
        if "RT" in text:
            RT = True
        else: RT = False
        others = text.count('@')
        sent = TextBlob(text)
        valance = sent.sentiment.polarity
        NLTK = sid.polarity_scores(text)
        tweet_data = {'tweetID':data[i]['id'],'created_at':data[i]['created_at'],'text':text,'textblob':valance,
                      'NLTK': NLTK['compound'],'RT':RT,'others':others}
        # print(data[i])
        all_tweets.append(tweet_data)
    return all_tweets

# start()
with open('data.json', 'r') as f:
    j_data = json.load(f)
    print('json data loaded')
    key = (len(j_data['sample']))
    today = str(datetime.date.today())
    j_data['sample'].append(j_data['sample'][key-1])
    print(j_data['sample'][key])
    print(j_data['sample'][key-1])
