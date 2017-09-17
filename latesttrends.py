class LatestTrends:
    def __init__(self, title, trends):
        self.title = title
        self.trends = trends

def make_trends(title, trends):
  return LatestTrends(title, trends)