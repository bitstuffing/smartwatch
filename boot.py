# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(machine.UART(0, 115200), 1)
import gc
import webrepl
webrepl.start()
gc.collect()
try:
    from welcome import Welcome
    import ssd1306
    import machine
    i2c = machine.I2C(-1, machine.Pin(0), machine.Pin(16))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    Welcome(oled)
except Exception as e1:
    print("something goes wrong with welcome file: "+str(e1))
    import sys
    sys.print_exception(e1)
    pass
