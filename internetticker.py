import sys
import threading
import time
import datetime
import argparse
import string
import googletrends
import twittertrends

parser = argparse.ArgumentParser(description='Get the news from the internet')
parser.add_argument('--lcd',  action='store_true',
                    help='whether to export to real display')
args = parser.parse_args()

if args.lcd:
  sys.path.append("./lib")
  import lcddriver
  # initialize the lcd and clear
  lcd = lcddriver.lcd()
  lcd.lcd_clear()

displayWidth = 20
layoutString = " " * displayWidth
exitFlag = 0
cursorPosition = 0
trendProviders = [twittertrends.getWorldwideTrends, googletrends.getTrends, twittertrends.getLocalTrends]

def isEnglish(s):
    newString = s.encode("ascii", errors="ignore").decode()
    return len(newString) == len(s)

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
      global activeSource
      global activeFeed
      global feedPublished
      global cursorPosition
      trends = trendProviders[self.rssIndex]()
      activeSource = trends.title
      activeFeed = ""
      feedPublished = datetime.datetime.now().time().isoformat().split(".")[0]
      cursorPosition = 0
      for idx, entry in enumerate(trends.trends):
        # Remove any non-english strings from worldwide since the LCD display can't display them
        if isEnglish(entry):
          if idx != len(trends.trends) - 1:
            activeFeed += entry + " | "
          else:
            activeFeed += layoutString
      time.sleep(delay)
      if self.rssIndex >= len(trendProviders) - 1:
        self.rssIndex = 0
      else:
        self.rssIndex += 1

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
        if args.lcd:
          if len(activeSource) < displayWidth:
            title = activeSource + layoutString[0:displayWidth-len(activeSource)]
          else:
            title = activeSource
          lcd.lcd_display_string(title,1)
        else:
          print(activeSource)
        if cursorPosition < len(activeFeed):
          if cursorPosition > displayWidth:
            offsetString = ""
            feedString = activeFeed[cursorPosition - displayWidth: cursorPosition]
          else:
            offsetString = layoutString[0:displayWidth-cursorPosition]
            feedString = activeFeed[0:cursorPosition]
          if args.lcd:
            lcd.lcd_display_string(layoutString,2)
            lcd.lcd_display_string(offsetString + feedString,2)
          else:
            print(offsetString + feedString)
          cursorPosition += 1
        else:
          cursorPosition = 0
        if args.lcd:
          lcd.lcd_display_string(feedPublished,4)
        else:
          print(feedPublished)

# Create new threads
feedReader = feedReaderThread(1, "FeedReader")
displayPrinter = displayPrintingThread(1, "DisplayPrinter")

# Start new Threads
feedReader.start()
displayPrinter.start()

print ("Exiting Main Thread")  
