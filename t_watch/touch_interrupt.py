import machine
from time import sleep
import st7789 as colors
import tft_config
import vga1_bold_16x32 as font
Pin = machine.Pin

buzzer = Pin(4,Pin.OUT)
backlight = Pin(12,Pin.OUT)

tft = tft_config.config(0)
tft.init()
tft.fill(colors.BLACK)
tft.text(font,"Hello",80,80,colors.WHITE)
sleep(1)
tft.off()

i0 = machine.SoftI2C(sda=Pin(21),scl=Pin(22))
display_on = False

def handle_interrupt(pin):
    global display_on
    if (display_on):
        return
    display_on = True
    s, m, h = i0.readfrom_mem(81, 2, 3)
    now = "%d%d:%d%d" % ((h>>4)&3, h&0xF, (m>>4)&7, m&0xF)
    tft.on()
    tft.text(font,now,80,80,colors.WHITE)
    sleep(2)
    tft.off()
    display_on = False

pir = Pin(38, Pin.IN, Pin.PULL_UP)
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

