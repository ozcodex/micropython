# This file is executed on every boot (including wake-boot from deepsleep)
import machine
#esp.osdebug(None)
#import webrepl
#webrepl.start()

machine.freq(80000000) # half speed