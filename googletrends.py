import feedparser
import latesttrends

google_trends_rss_url = "https://trends.google.com/trends/hottrends/atom/feed?pn=p1"

def getTrends():
  feed = feedparser.parse( google_trends_rss_url )
  trends = []
  for entry in feed.entries:
    trends.append(entry.title)
  return latesttrends.make_trends(feed.feed.title, trends)