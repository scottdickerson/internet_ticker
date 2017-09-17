import feedparser
import sys
sys.path.append("./lib")
import lcddriver
import threading
import time
import datetime

displayWidth = 20
layoutString = " " * displayWidth
exitFlag = 0
cursorPosition = 0

# initialize the lcd and clear
lcd = lcddriver.lcd()
lcd.lcd_clear()

google_trends_rss_url = "https://trends.google.com/trends/hottrends/atom/feed?pn=p1"

class feedReaderThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.rssIndex = 0
   def run(self):
      read_feed(self, 300)

def read_feed(self, delay):
   while 1:
      if exitFlag:
         self.name.exit()
      feed = feedparser.parse( google_trends_rss_url )
      global activeSource
      global activeFeed
      global feedPublished
      global cursorPosition
      activeSource = feed.feed.title
      activeFeed = ""
      feedPublished = datetime.datetime.now().time().isoformat().split(".")[0]
      cursorPosition = 0
      for idx, entry in enumerate(feed.entries):
        if idx != len(feed.entries) - 1:
          activeFeed += entry.title + " | "
        else:
          activeFeed += layoutString
      time.sleep(delay)

class displayPrintingThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      print_time(self, .05)

def print_time(self, delay):
   while 1:
      if exitFlag:
         self.name.exit()
      time.sleep(delay)
      global cursorPosition
      if 'activeSource' in globals():
        lcd.lcd_display_string(activeSource,1)
        if cursorPosition < len(activeFeed):
          if cursorPosition > displayWidth:
            offsetString = ""
            feedString = activeFeed[cursorPosition - displayWidth: cursorPosition]
          else:
            offsetString = layoutString[0:displayWidth-cursorPosition]
            feedString = activeFeed[0:cursorPosition]
          lcd.lcd_display_string(layoutString,2)
          lcd.lcd_display_string(offsetString + feedString,2)
          cursorPosition += 1
        else:
          cursorPosition = 0
        lcd.lcd_display_string(feedPublished,4)

# Create new threads
feedReader = feedReaderThread(1, "FeedReader")
displayPrinter = displayPrintingThread(1, "DisplayPrinter")

# Start new Threads
feedReader.start()
displayPrinter.start()

print ("Exiting Main Thread")  
