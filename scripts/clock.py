import math

class Clock():

    def getTickPosition(self, tick=0, radio=32, originx=64, originy=32):
        # The cos() and sin()
        tick -= 15

        # ensure that tick is between 0 and 60
        tick = tick % 60

        tick = 60 - tick

        # the argument to sin() or cos() needs to range between 0 and 2 * math.pi
        # Since tick is always between 0 and 60, (tick / 60.0) will always be between 0.0 and 1.0
        # The (tick / 60.0) lets us break up the range between 0 and 2 * math.pi into 60 increments.
        x = math.cos(2 * math.pi * (tick / 60.0))
        y = -1 * math.sin(2 * math.pi * (tick / 60.0)) # "-1 *" because in Pygame, the y coordinates increase going down (the opposite of how they normally go in mathematics)

        # sin() and cos() return a number between -1.0 and 1.0, so multiply to stretch it out.
        x *= radio
        y *= radio

        # Then do the translation (i.e. sliding) of the x and y points.
        # NOTE: Always do the translation addition AFTER doing the stretch.
        x += originx
        y += originy

        return x, y

    def displayClock(self,screen,hours=0,minutes=0,seconds=0,ratio=32,originx=64,originy=32):
        hours = hours % 12
        x, y = self.getTickPosition(tick=hours,radio=int(ratio/2),originx=originx,originy=originy)
        x2, y2 = self.getTickPosition(tick=minutes,radio=int(ratio*2/3),originx=originx,originy=originy)
        x3, y3 = self.getTickPosition(tick=seconds,radio=ratio,originx=originx,originy=originy)
        screen.draw_circle(originx,originy,ratio)
        screen.draw_line(originx,originy,x,y)
        screen.draw_line(originx,originy,x2,y2)
        screen.draw_line(originx,originy,x3,y3)
        screen.oled.show()
