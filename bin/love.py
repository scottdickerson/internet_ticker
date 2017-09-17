# on importe le pilote
import sys
sys.path.append("./lib")
import lcddriver
from time import *

# on initialise le lcd
lcd = lcddriver.lcd()

# on reinitialise le lcd
lcd.lcd_clear()

# on affiche des caracteres sur chaque ligne
lcd.lcd_display_string("Angela, I love you ", 1)
lcd.lcd_display_string("and miss you ", 2)
lcd.lcd_display_string("very", 3)
lcd.lcd_display_string("MUCH", 4)
