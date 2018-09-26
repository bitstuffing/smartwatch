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
