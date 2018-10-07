import network
import utime
import sys
import ntptime
import machine
from scripts.menu import Menu
from library.screenutils import ScreenUtils
from scripts.clock import Clock

class Welcome(object):

    def __init__(self,oled):
        self.screen = ScreenUtils(oled)
        self.welcome()
        try:
            self.checkConnection()
            self.synchronizeTime()
            self.menu = False
            pin = machine.Pin(13, machine.Pin.IN,machine.Pin.PULL_UP)
            pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.menuButton)
            while not self.menu:
                self.getTime(analog=True)
                utime.sleep_ms(500)
        except Exception as e:
            print("Something goes wrong!"+str(e))
            sys.print_exception(e)
            pass

    def menuButton(self,pin):
        self.menu = True
        Menu().displayMenu(self)

    def getTime(self,analog=True):
        #year, month, day, hour, minute, second, ms, dayinyear = utime.localtime()
        #timezone issues, convert
        year = utime.localtime()[0] #get current year
        #calculate last sunday of march and october
        HHMarch = utime.mktime((year,3 ,(27-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of March change to Sumer
        HHOctober = utime.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to Winter
        #then calculate and convert
        now=utime.time()
        SUMMER = 3600 #+1h in summer
        TIMEZONE = 3600 #TODO configure this parameter
        if now < HHMarch: # WINTER
            dst=utime.localtime(now+TIMEZONE)
        elif now < HHOctober : # SUMMER
            dst=utime.localtime(now+TIMEZONE+SUMMER)
        else: # WINTER
            dst=utime.localtime(now+TIMEZONE)
        year, month, day, hour, minute, second, ms, dayinyear = dst
        if not analog:
            localtime = "{:0>2d}".format(hour)+":"+"{:0>2d}".format(minute)+":"+"{:0>2d}".format(second)+"     "+"{:0>2d}".format(day)+"/"+"{:0>2d}".format(month)+"/"+str(year)
            self.screen.writeText(text=localtime)
        else:
            self.screen.oled.fill(0)
            Clock().displayClock(screen=self.screen,hours=hour,minutes=minute,seconds=second)


    def synchronizeTime(self):
        #first set utc time
        ntptime.settime()

    def welcome(self):
        #oled.poweroff()
        self.screen.oled.poweron()
        self.screen.oled.init_display()
        self.screen.oled.fill(1)
        self.screen.oled.show()
        utime.sleep_ms(50)
        #oled.init_display()
        self.screen.oled.fill(0)
        self.screen.oled.show()

    def checkConnection(self):
        sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
        text = 'Connecting'
        self.screen.writeText(text=text,delay=False)
        while not sta_if.isconnected():
            utime.sleep_ms(250)
            text+="."
            self.screen.writeText(text=text,delay=False)
        self.screen.writeText(text='Connected with ip '+str(sta_if.ifconfig()),delay=False)
