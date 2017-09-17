import geocoder
import json

def latLong ():
  g = geocoder.ip('me')
  return g.json