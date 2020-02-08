import sys, subprocess, time

from PIL import Image
import ST7789 as ST7789

print("""
heat.py - Display heat on the LCD.
If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the rear slot.
""")

size =  (32, 24)

if len(sys.argv) < 1:
    print("Usage: {}".format(sys.argv[0]))
    sys.exit(1)

def _get_capture_proc(fps):
  fps = fps
  return subprocess.Popen(['/home/pi/mlx90640-library/examples/rawrgb', '{}'.format(fps)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000
)

WIDTH = disp.width
HEIGHT = disp.height

fps = 6

# Initialize display.
disp.begin()

# Load an image.
print('Starting heat cam:...')

# Resize the image
#image = image.resize((WIDTH, HEIGHT))

camera = _get_capture_proc(fps)

sleep_time = 1.0 / fps

# Draw the image on the display hardware.
print('Starting video')
while (True):
    
  time.sleep(sleep_time)

  frame = camera.stdout.read(size[0] * size[1] * 3)
    
  print(frame)
  
  image = Image.frombytes('RGB', size, frame)
  
  image = image.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
  
  disp.display(image)



