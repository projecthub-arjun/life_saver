# Library for using delay
import time

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

# Home screen
def home_screen(screen):
    screen.clear()
    screen.display((7, 10), "Monitoring")
    screen.display((40 ,30), "Car")

# Screen to be displayed, when accident is detected
def accident_detected_screen(screen):
    screen.clear()
    screen.display((7, 10), "Emergency")
    screen.display((7, 30), "Broadcast")

# Screen to display countdown
def countdown_screen(screen):
    countdown = 10
    while(countdown >= 0):
        screen.clear()
        screen.display((48,0), str(countdown))
        countdown -= 1
        time.sleep(1)

# Screen that displays Calling for help
def calling_help_screen(screen):
    screen.clear()
    screen.display((7, 0), "Calling")
    screen.display((7, 20), "For")
    screen.display((7, 40), "Help !!!")

# Screen displayed after successfull broadcast
def calling_help_success_screen(screen):
    screen.clear()
    screen.display((7, 0), "Help Will")
    screen.display((7, 20), "Arrive")
    screen.display((7, 40), "Shortly...")

def main():
    general_profile = OLED(font_type = '/home/pi/life_saver/Starjedi.ttf', font_size = 18)
    countdown_profile = OLED(font_type = '/home/pi/life_saver/Starjedi.ttf', font_size = 40)
    home_screen(general_profile)
    time.sleep(2)
    countdown_screen(countdown_profile)
    calling_help_screen(general_profile)
    time.sleep(2)
    calling_help_success_screen(general_profile)
    time.sleep(2)

# Start of execution
if __name__ == '__main__':
    main()
