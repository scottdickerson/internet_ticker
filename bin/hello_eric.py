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
lcd.lcd_display_string("   Hello Eric !", 1)
lcd.lcd_display_string(" Would you like to ", 2)
lcd.lcd_display_string("     play a", 3)
lcd.lcd_display_string("     GAME????", 4)
