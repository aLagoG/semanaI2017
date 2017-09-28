#!/usr/bin/env python
import tweepy
from urllib.parse import quote_plus
from time import sleep
import json

user_idx = 0
consumer_keys = ["ZB0SiXu0x4X9mMxTHy2Xnul2Q",
                 "CsD0PCj2JE4wc9nGPDWE2hDyg", "TzhWIG44kbyBgkOz4rYFauWWv", "wOsbo6A8gZiiwxwZ1YYew5E5N"]
consumer_secrets = ["cOdGBpjWFL4GvM9wpg4EHB3wFAbHkWrlrkxr7VwcG7HUVRQKjM",
                    "tYAAadaOZGlsCAzzKhl2yNAMKF3MzLxeSyNDwLmnZoLStRjHmE", "X0Ca6Lx3mw0HEPFU0zbdOD1JT9nkZC1Cbs2scXcIoHYVntf3c2", "8kMSC0LO7Yafevkpkj60AEQguBzKyZnV89EPe8rrfL1YKkByCe"]
access_tokens = ["270977393-CuknJGyA45XDS77Zcp9a92TGommj73tYvyJlYqM0",
                 "3355479132-b9e5utZDk2nCpFflbuuHQnlGCDpozEgcksFTTnn", "1155702312-9XAFrsQgonGJt90UXDkDpY7nP8ACfBTu4SL7YEM", "719111575-1yy35eH6Rc8o3QIyx45gK3WWzgXQFzUy4ufdA9qN"]
access_secrets = ["iSSdK4EjzImLC3bM8DbNEcpa6QcM2KGehe978tAggGTw5",
                  "MPjsZ3LfBsv5LQZR53SUL5rHHejHu9PYd6ADrjNXPow4u", "N2hbgBhS4cB9bxWBURb8ZQLQqVAhvepVaE15VfXoIOQKK", "Krf9w1Mm6EJcvQTKWvrbO0g4nAQytmcPFRBQAUQu9UqfX"]

auth = tweepy.OAuthHandler(consumer_keys[0], consumer_secrets[0])
auth.set_access_token(access_tokens[0], access_secrets[0])

api = tweepy.API(auth)

emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "☺", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙", "😖", "😫", "😩", "😤", "😠", "😡", "😶", "😐", "😑", "😯", "😦", "😧", "😮", "😲", "😵", "😳", "😱", "😨", "😰", "😢", "😥", "🤤", "😭", "😓", "😪", "😴", "🙄", "🤔", "🤥", "😬", "🤐", "🤢", "🤧", "😷", "🤒", "🤕", "😈", "👿", "😺", "😸", "😹", "👌", "👈", "👉",
          "👆", "👇", "☝", "✋", "🤚", "🖐", "🖖", "👋", "🤙", "💪", "🖕", "👀", "🤦‍♀", "🤷‍♂", "🤦‍♂", "🤷‍♀", "🙅", "❤", "💔", "🔥", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🙌", "👏", "🙏", "👍", "👎", "👊", "✊", "✌", "🤘", "👈", "👉", "👌", "😸", "🤝", "🤛", "🤜", "😚", "😋", "😜", "😝", "😛", "🤑", "🤗", "🤓", "😎", "🤡", "🤠", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹", "😣"]
query_all = ["windows"]

searched_tweets = []
tweet_ids = set()
rType = "mixed"
last_id = -1
size_of_chunk = len(emojis) // 6
no_change_times = 0
downloaded = 0
while len(searched_tweets) < 20000 and no_change_times < 6:
    # tpp = (600 - len(searched_tweets)) // 6
    tpp = 100
    # print("Size = " + str(tpp))
    for i in range(6):
        now = emojis[i * size_of_chunk:(i + 1) * size_of_chunk]
        query = quote_plus("({0}) ({1})".format(
            " OR ".join(query_all), " OR ".join(now)))
        # query = quote_plus("epn")
        # print(query)
        try:
            if last_id != -1:
                new_tweets = api.search(
                    q=query, result_type=rType, count=tpp, max_id=last_id - 1, tweet_mode='extended', lang="es")
            else:
                new_tweets = api.search(
                    q=query, result_type=rType, count=tpp, tweet_mode='extended', lang="es")
            if not new_tweets:
                no_change_times += 1
                continue
            no_change_times = 0
            downloaded += 100
            for tweet in new_tweets:
                if tweet._json["full_text"][0:2] == "RT":
                    continue
                if tweet.id not in tweet_ids:
                    tweet_ids.add(tweet.id)
                    searched_tweets.append(tweet)
            # searched_tweets.extend(new_tweets)
            print(len(searched_tweets))
        except tweepy.RateLimitError as e:
            # wait
            # print("Waiting for 15 min")
            # sleep(15 * 60)
            # print("Continuing")
            try:
                user_idx += 1
                if user_idx == len(access_secrets):
                    break
                print("Changing user to #" + str(user_idx))
                auth = tweepy.OAuthHandler(
                    consumer_keys[user_idx], consumer_secrets[user_idx])
                auth.set_access_token(
                    access_tokens[user_idx], access_secrets[user_idx])
                api = tweepy.API(auth)
            except Exception as e:
                print(e)
                break
        except tweepy.TweepError as e:
            # check of error code
            print(e)
            break
    if len(tweet_ids) > 0:
        last_id = min(tweet_ids)
print("Saving")

f = open('results_windows.json', 'w')
# f.writelines([str(x._json)+",\n" for x in searched_tweets])
to_file = {"tweets": []}
for tweet in searched_tweets:
    di = {}
    di['created_at'] = tweet._json['created_at']
    di['user'] = {'id': tweet._json['user']['id'],
                  'user_name': tweet._json['user']['screen_name']}
    di['id'] = tweet._json['id']
    di['text'] = tweet._json['full_text']
    to_file["tweets"].append(di)
    # f.write(str(di) + ",\n")

f.write(json.dumps(to_file))
print("Done")
print(downloaded)
