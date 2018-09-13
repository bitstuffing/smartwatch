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
    Welcome()
except Exception as e1:
    print("something goes wrong with welcome file: "+str(e1))
    import sys
    sys.print_exception(e1)
    pass
