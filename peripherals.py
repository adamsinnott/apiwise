def set_lights(magtag, colour, brightness=0.01):
  magtag.peripherals.neopixel_disable = False
  magtag.peripherals.neopixels.brightness = brightness
  if colour == "purple":
    # Purple
    magtag.peripherals.neopixels.fill((180, 0, 255))
  if colour == "red":
    # Red
    magtag.peripherals.neopixels.fill((255, 0, 0))
  if colour == "yellow":
    # Yellow
    magtag.peripherals.neopixels.fill((255, 255, 0))
  if colour == "turquoise":
    # Turquoise
    magtag.peripherals.neopixels.fill((0, 255, 255))
  if colour == "green":
    # Green
    magtag.peripherals.neopixels.fill((0, 255, 0))
  if colour == "clear":
    # Clear
    magtag.peripherals.neopixels.fill((0, 0, 0))
    magtag.peripherals.neopixels.brightness = 0

def play_error_sound(magtag, type):
  if type == "error":
    magtag.peripherals.play_tone(2093, 0.25)
    magtag.peripherals.play_tone(2093, 0.25)
