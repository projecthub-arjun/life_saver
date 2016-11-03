import RPi.GPIO as GPIO
import time
import os
import sys
import subprocess


# Libraries for communicating with OLED display
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# Libraries for creating the image and text to be
# displayed on OLED
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Class for handling OLED display
class OLED:
    # Constructor to initalize the OLED display
    def __init__(self, rst_pin = 24, bit_depth = 1, font_type = '', font_size = 18):
        # Initalize the Adafruit SSD1306 library
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst = rst_pin)
        self.disp.begin()

        # Get the dimesnsions of the OLED display
        self.width = self.disp.width
        self.height = self.disp.height

        # Create an image instance
        # Since it is a monochrome display bit depth is 1
        self.image = Image.new(str(bit_depth), (self.width, self.height))

        # Clear the display
        self.disp.clear()
        self.disp.display()

        # Set the font type and size, if specified
        if(font_type):
            self.font = ImageFont.truetype(font_type, font_size)
        else:
            self.font = ImageFont.load_default()

        # Create the draw instance, used to draw on the OLED display
        self.draw = ImageDraw.Draw(self.image)

    # Function to clear the OLED screen
    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline = 0, fill = 0)

    # Function to display text on the OLED screen
    def display(self, pos, text, alpha = 255):
        self.draw.text(pos, text, font = self.font, fill = alpha)
        self.disp.image(self.image)
        self.disp.display()

    def __del__(self):
        # Clear the display
        self.disp.clear()
        self.disp.display()

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

process = None
process = subprocess.Popen(['python', '/home/pi/life_saver/life_saver.py'])
general_profile = OLED(font_type = '/home/pi/life_saver/Starjedi.ttf', font_size = 18)

# Screen displayed after successfull broadcast
def restarting_screen(screen):
    screen.clear()
    screen.display((7, 20), "Restarting")
    time.sleep(1)

while True:
    input_state = GPIO.input(26)
    if input_state == False:
        restarting_screen(general_profile)
        print('Killing')
        process.kill()
        time.sleep(5)
        print "Starting"
        process = subprocess.Popen(['python', '/home/pi/life_saver/life_saver.py'])



