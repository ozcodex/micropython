import machine
import esp32
from time import sleep
import st7789 as colors
import pcf8563
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
rtc = pcf8563.PCF8563(i2c)
machine.PWM(machine.Pin(12), freq=100, duty=200)

def get_time():
    now = "%02d:%02d:%02d" % (rtc.hours(), rtc.minutes(), rtc.seconds())
    return now

def get_date():
    now = "%02d/%02d/%02d" % (rtc.year(), rtc.month(), rtc.date())
    return now

def get_battery():
    value = i2c.readfrom_mem(53, 0xB9, 1)
    percent = "%d%%" % int.from_bytes(value, "big")
    return percent

def draw_screen():
    tft.fill(colors.BLACK)
    tft.on()
    for x in range(3):
        tft.text(font,get_time(),50,80,colors.WHITE,colors.BLACK)
        tft.text(font,get_date(),50,110,colors.GREEN,colors.BLACK)
        tft.text(font,get_battery(),100,140,colors.RED,colors.BLACK)
        sleep(1.1)
    tft.off()
    
def toogle(x=0):
    global active
    active = not active
    
def handle_interrupt(pin):
    if(active):
        return
    sleep(0.1)
    toogle()
    draw_screen()
    tim.init(mode=machine.Timer.ONE_SHOT, period=500, callback=toogle)

# called each 10 seconds
def sleep_mode(x):
    print("going into sleep mode!")
    sleep(0.1)
    machine.lightsleep()
    sleep(0.1)
    print("woke up!")
        

#define interruption
pir = machine.Pin(38, machine.Pin.IN, machine.Pin.PULL_UP)
pir.irq(trigger=machine.Pin.IRQ_RISING, handler=lambda p:schedule(handle_interrupt,p))
esp32.wake_on_ext1(pins = [pir], level = esp32.WAKEUP_ALL_LOW)

