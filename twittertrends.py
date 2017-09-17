import tweepy
import json
import latlong
import latesttrends

consumer_key = 'VfyBgjsefrC7JofxaZpNLlgG5'
consumer_secret = '7tkJzThPNuCdVWM4QmPqztsOe5vDh2IuMKGbPcSpgOw0moMMAB'
access_token = '14659192-4J5anvi8hZepjFO6wJw2sRdbAFFQBhIXakVBvjKb8'
access_token_secret = 'OYk7JP0dSZEjPw81VsdLhKbiYvu4x5DLkb4cJx4Vtyb9K'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

location = latlong.latLong()
api = tweepy.API(auth)
available_trend_locations = api.trends_closest(location['lat'], location['lng'])

def getLocalTrends():
  local_trends = api.trends_place(available_trend_locations[0]['woeid'])
  trends = []
  for trend in local_trends[0]['trends']:
    trends.append(trend['name'])
  return latesttrends.make_trends("Local Tweets", trends)

def getWorldwideTrends():
  worldwide_trends = api.trends_place(1)
  trends = []
  for trend in worldwide_trends[0]['trends']:
    trends.append(trend['name'])
  return latesttrends.make_trends("Worldwide Tweets", trends)