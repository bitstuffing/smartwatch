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
        # Line drawing function.  Will draw a single pixel wide line starting at
        # x0, y0 and ending at x1, y1.
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2
        ystep = 0
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        while x0 <= x1:
            if steep:
                self.oled.pixel(int(y0), int(x0), 1)
            else:
                self.oled.pixel(int(x0), int(y0), 1)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

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
