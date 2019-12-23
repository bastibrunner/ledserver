from flask import Flask
import time
import board
import neopixel
import _thread

app = Flask(__name__)

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.D21
 
# On a Raspberry pi, use this instead, not all pins are supported
#pixel_pin = board.D18
 
# The number of NeoPixels
num_pixels = 12

led_command="off"
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)
 
 
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
 
 
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def fadeinfadeout(waiton,waitoff,ontime,color):
    for i in range(255):
        pixels.fill([round(e*i/255) for e in color])
        pixels.show()
        time.sleep(waiton)
    time.sleep(ontime)
    for i in range(255):
        pixels.fill([round(e*(255-i)/255) for e in color])
        pixels.show()
        time.sleep(waiton)
 
def fadein(wait,steps,color):
    for i in range(steps):
        pixels.fill([round(e*i/steps) for e in color])
        pixels.show()

def fadeout(wait,steps,color):
    for i in range(255):
        pixels.fill([round(e*(steps-i)/steps) for e in color])
        pixels.show()
 

def ledthread( threadName, delay):
    j=0
    global led_command
    while True:
        if (led_command=="off"):
            pixels.fill((0,0,0))
            pixels.show()
        if (led_command=="white"):
            pixels.fill((255,255,255))
            pixels.show()
        if (led_command=="red"):
            pixels.fill((255,0,0))
            pixels.show()
        if (led_command=="blue"):
            pixels.fill((0,0,255))
            pixels.show()
        if (led_command=="rainbow"):
            j=(j+1) if (j<255) else 0
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(0.001)
        if (led_command=="circle"):
            for i in range(num_pixels):
                pixels.fill((0,0,0))
                pixels[i] = (255,0,0)
                pixels.show()
                time.sleep(0.2)
        if (led_command=="pinkflash"):
            fadein(0,20,(255,0,128))
            time.sleep(1)
            fadeout(0.01,255,(255,0,128))
            led_command="off"
        if (led_command=="purplepulse"):
            fadeinfadeout(0.01,0.01,1,(100,0,255))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    global led_command
    led_command=path
    return 'OK: %s' % path



if __name__=='__main__':
    _thread.start_new_thread( ledthread, ("Thread-1", 2, ) )
    app.run()


