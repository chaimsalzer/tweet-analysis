from TwitterAPI import TwitterAPI
import json
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime
import politicians
import time
import tweet_mail

# test = ["@JohnBoozman","@JohnCornyn", "@KellyAyotte",]

all_politicians = politicians.us_house+politicians.us_senate


CONSUMER_KEY = 'D3ffNafoksntbQNRIUR9GwWZh'
CONSUMER_SECRET = 'SMTjPzDbybBCFzBXPzHb5dn7DwrIfQev92fnloeWwQctaF23BM'
ACCESS_TOKEN_KEY = '2646985382-G1T7rnwoTrvETulIC8LDLRSO6PSz3eM0mFh0hGx'
ACCESS_TOKEN_SECRET = '46g24926lCBtV1oXfcsE3rrdw7aRSC7dexN88H249CgMz'
api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)

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


def start():
    today = str(datetime.date.today())
    request_num = 0
    jata = {"datetime":today}
    for query in all_politicians:
        request_num += 1
        if request_num%100 == 0:
            print('waiting for 15 minutes...')
            #sleep 15 minutes after 180 requests
            time.sleep(905)
            print('finished waiting')
        r = api.request('users/show', {'screen_name': query})
        data = (json.loads(r.text))
        # print(data)
        sample = {
            'name': data['name'],
            'followers_count': data['followers_count'],
            'friends_count':data['friends_count'],
            'listed_count':data['listed_count'],
            'statuses_count':data['statuses_count'],
            'tweets': []}
        print('connecting to '+str(data['name'].encode("ascii", "ignore"))+' || request # '+str(request_num))
        tweet_list = get_tweets(query,today)
        i = 0
        for tweet_data in tweet_list:
            sample['tweets'].append({
                'tweetID': tweet_data['tweetID'],
                'created_at': tweet_data['created_at'],
                'text': tweet_data['text'],
                'textblob': tweet_data['textblob'],
                'NLTK': tweet_data['NLTK'],
                'RT': tweet_data['RT'],
                'others': tweet_data['others']
            })
        jata[query]=sample
        i += 1

    f_today = datetime.datetime.today()
    file_date = str(f_today.year)+'_'+str(f_today.month)+'_'+str(f_today.day)
    print(file_date)
    with open('data/'+file_date+'.json','w') as f:
        f.write(json.dumps(jata))
        tweet_mail.tweet_mail()


start()
