import adafruit_ssd1306
import busio
import board
import adafruit_framebuf
#https://docs.circuitpython.org/projects/framebuf/en/latest/api.html

from bytemap.numpad import numpad #bytearry

i2c = busio.I2C(board.GP1, board.GP0)

WIDTH = 128
HEIGHT = 64 #32 

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
fb = adafruit_framebuf.FrameBuffer(oled, WIDTH, HEIGHT, buf_format=0, stride=None)


#class Graphic():
#    def __init__(self, oled) -> None:
#        self.oled = oled
#        self.center_x = 63
#        self.center_y = 15
#        # how fast does it move in each direction
#        self.x_inc = 1
#        self.y_inc = 1
#        # what is the starting radius of the circle
#        self.radius = 8
#        
#        # start with a blank screen
#        self.oled.fill(0)
#        # we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
#        self.oled.show()    
#    
#    def draw_graphic(self, xpos0, ypos0, rad, col=1):
#        x = rad - 1
#        y = 0
#        dx = 1
#        dy = 1
#        err = dx - (rad << 1)
#        while x >= y:
#            self.oled.pixel(xpos0 + x, ypos0 + y, col)
#            self.oled.pixel(xpos0 + y, ypos0 + x, col)
#            self.oled.pixel(xpos0 - y, ypos0 + x, col)
#            self.oled.pixel(xpos0 - x, ypos0 + y, col)
#            self.oled.pixel(xpos0 - x, ypos0 - y, col)
#            self.oled.pixel(xpos0 - y, ypos0 - x, col)
#            self.oled.pixel(xpos0 + y, ypos0 - x, col)
#            self.oled.pixel(xpos0 + x, ypos0 - y, col)
#            if err <= 0:
#                y += 1
#                err += dy
#                dy += 2
#            if err > 0:
#                x -= 1
#                dx += 2
#                err += dx - (rad << 1)
#        
#
#    def update_graphic(self):
#        # undraw the previous circle
#        
#        self.draw_graphic(self.center_x, self.center_y, self.radius, col=0)
#
#        # if bouncing off right
#        if self.center_x + self.radius >= self.oled.width:
#            # start moving to the left
#            self.x_inc = -1
#        # if bouncing off left
#        elif self.center_x - self.radius < 0:
#            # start moving to the right
#            self.x_inc = 1
#
#        # if bouncing off top
#        if self.center_y + self.radius >= self.oled.height:
#            # start moving down
#            self.y_inc = -1
#        # if bouncing off bottom
#        elif self.center_y - self.radius < 0:
#            # start moving up
#            self.y_inc = 1
#
#        # go more in the current direction
#        self.center_x += self.x_inc
#        self.center_y += self.y_inc
#
#        # draw the new circle
#        self.draw_graphic(self.center_x, self.center_y, self.radius)
#        # show all the changes we just made
#        self.oled.show()
#
#
##TODO use OLED to display a high level picture of macro profile (right half of display)
# when a key is pressed used left half of display to show a list of most recent keys pressed 
