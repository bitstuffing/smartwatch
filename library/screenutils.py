import utime

class ScreenUtils(object):

    def __init__(self,oled):
        self.oled = oled

    def writeText(self,text,delay=False):
        self.oled.fill(0)
        maxlen = 13
        if len(text)>maxlen:
            i=0
            old=0
            for ind in range(0, len(text), maxlen):
                line = text[ind:ind+maxlen] #TODO change by maxlen if necessary
                height=i*10
                if old>0:
                    j=old
                else:
                    j=0
                for char in line:
                    self.oled.text(char,j,height)
                    if delay:
                        #utime.sleep_ms(5)
                        self.oled.show()
                    j+=10
                i+=1
        else:
            j=0
            height=0
            for char in text:
                self.oled.text(char,j,height)
                j+=10
                if delay:
                    #utime.sleep_ms(5)
                    self.oled.show()
        self.oled.show()

    def draw_line(self, x0, y0, x1, y1):
        deltax = x1 - x0
        deltay = y1 - y0
        error = -1.0
        if deltax is not 0: # Assume deltax != 0 (line is not vertical)
            deltaerr = abs(deltay / deltax)
            y = y0
            for x in range(int(x0), int(x1)-1):
                # plot(x,y)
                self.oled.pixel(x, y, 1)
                # print(x, y)
                error = error + deltaerr
                if error >= 0.0:
                    y = y + 1
                    error = error - 1.0
        else: #vertical line
            for y in range(int(y0), int(y1)-1):
                self.oled.pixel(x0, y, 1)
                y = y + 1

    def draw_circle(self, x0, y0, radius):
        x = radius
        y = 0
        err = 0

        while x >= y:
            self.oled.pixel(x0 + x, y0 + y, 1)
            self.oled.pixel(x0 + y, y0 + x, 1)
            self.oled.pixel(x0 - y, y0 + x, 1)
            self.oled.pixel(x0 - x, y0 + y, 1)
            self.oled.pixel(x0 - x, y0 - y, 1)
            self.oled.pixel(x0 - y, y0 - x, 1)
            self.oled.pixel(x0 + y, y0 - x, 1)
            self.oled.pixel(x0 + x, y0 - y, 1)

            y += 1
            err += 1 + 2*y
            if 2*(err-x) + 1 > 0:
                x -= 1
                err += 1 - 2*x
