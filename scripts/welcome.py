import network
import utime
import sys
import ntptime
import machine
from scripts.menu import Menu
from library.screenutils import ScreenUtils

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
                self.getTime()
                utime.sleep_ms(500)
        except Exception as e:
            print("Something goes wrong!"+str(e))
            sys.print_exception(e)
            pass

    def menuButton(self,pin):
        self.menu = True
        Menu().displayMenu(self)

    def getTime(self):
        year, month, day, hour, minute, second, ms, dayinyear = utime.localtime()
        localtime = "{:0>2d}".format(hour)+":"+"{:0>2d}".format(minute)+":"+"{:0>2d}".format(second)+"     "+"{:0>2d}".format(day)+"/"+"{:0>2d}".format(month)+"/"+str(year)
        self.screen.writeText(text=localtime)

    def synchronizeTime(self):
        ntptime.settime()
        pass

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
