

import machine
import utime

class Menu():

    def displayMenu(self,welcome):
        self.welcome = welcome
        self.welcome.screen.writeText(text='Menu',delay=False)
        quitPin = machine.Pin(10, machine.Pin.IN,machine.Pin.PULL_UP)
        quitPin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.exitButton)
        menuPin = machine.Pin(13, machine.Pin.IN,machine.Pin.PULL_UP)
        menuPin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.menuButton)
        upPin = machine.Pin(5, machine.Pin.IN,machine.Pin.PULL_UP)
        upPin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.nextButton)
        downPin = machine.Pin(4, machine.Pin.IN,machine.Pin.PULL_UP)
        downPin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.beforeButton)

        utime.sleep_ms(50)
        self.welcome.screen.writeText(text='waiting event...',delay=False)

    def menuButton(self,pin):
        self.welcome.screen.writeText(text='menu button',delay=False)

    def exitButton(self,pin):
        self.welcome.screen.writeText(text='button exit',delay=False)
        self.welcome.menu = False

    def nextButton(self,pin):
        self.welcome.screen.writeText(text='pushed next',delay=False)

    def beforeButton(self,pin):
        self.welcome.screen.writeText(text='pushed before',delay=False)
