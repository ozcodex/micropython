import machine
from time import sleep
import st7789 as colors
import tft_config
import vga1_bold_16x32 as font
from micropython import schedule

#initialization
Pin = machine.Pin
active = False
tim = machine.Timer(0)
i2c = machine.SoftI2C(sda=Pin(21),scl=Pin(22))
tft = tft_config.config(0)
tft.init()
tft.off()

def get_time():
    s, m, h = i2c.readfrom_mem(81, 2, 3)
    now = "%d%d:%d%d" % ((h>>4)&3, h&0xF, (m>>4)&7, m&0xF)
    return now

def get_battery():
    value = i2c.readfrom_mem(53, 0xB9, 1)
    percent = "%d%%" % int.from_bytes(value, "big")
    return percent

def draw_screen():
    tft.on()
    tft.fill(colors.BLACK)
    tft.text(font,get_time(),80,80,colors.WHITE)
    tft.text(font,get_battery(),100,110,colors.RED)
    sleep(2)
    tft.off()
    
def toogle(x=0):
    global active
    active = not active

def handle_interrupt(pin):
    if(active):
        return
    toogle()
    draw_screen()
    tim.init(mode=machine.Timer.ONE_SHOT, period=1000, callback=toogle)

#define interruption
pir = machine.Pin(38, machine.Pin.IN, machine.Pin.PULL_UP)
pir.irq(trigger=machine.Pin.IRQ_RISING, handler=lambda p:schedule(handle_interrupt,p))

print("Hello World")
#machine.lightsleep(5000)
sleep(2)
print("Woke")


