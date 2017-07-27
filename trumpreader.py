"""
Read Trump
"""
import os
import sys
import json
import nltk

"""
Get all of Trump's tweets from here:
https://github.com/bpb27/trump_tweet_data_archive
"""

dir = sys.path[0]
files = [os.path.join(dir, 'trump_tweets\\master_{}.json').format(2017 - i) for i in range(1)]
raw_data = []

for f_num, f in enumerate(files):
    with open(f, 'r') as file:
        tweets = json.load(file)

    for tweet in tweets:
        if 'text' in tweet.keys():
            tokenized = nltk.word_tokenize(tweet['text'])
            raw_data.append(tokenized)

data = raw_data
tokens = [item for sublist in data for item in sublist]


if __name__ == '__main__':
    # print(nltk.word_tokenize('How does this thing work??'))
    print('There are %d tokens in %d tweets' % (len(tokens), len(raw_data)))
