from adafruit_magtag.magtag import MagTag
import time
from endpoint import endpoint_list
from setup import splash_screen, display_setup, connect_to_wiFi, setup_requests, clear_screen, print_header
from peripherals import set_lights, play_error_sound
from api import api_check
from display_text import print_errors

# Globals
SCREEN_LINES=11
HEADER_SECTION_HEIGHT=3
ERROR_SECTION_HEIGHT=SCREEN_LINES - HEADER_SECTION_HEIGHT
API_CHECK_PERIOD=300
ERROR_CHECK_PERIOD=300
ERROR_LINE_HEADER_START=3
ERROR_LINE_START=4
ENPOINT_BASE="https://www.pickswise.com"
# ENPOINT_BASE=""
MAX_STRING_WIDTH=40
SCREEN_WIDTH=48
BACKGROUND_BMP="/bmps/apiwise.bmp"
CLEAR_BACKGROUND_BMP="/bmps/clear_background.bmp"

# Initialise variables
magtag = MagTag(default_bg=0xFFFFFF)
endpoint_errors = []
error_state = False
initialTime = time.monotonic()  # Time in seconds since power on
first_time = True


# Setup the screen, connect to WiFi, setup requests, draw initial lines
splash_screen(magtag, BACKGROUND_BMP, CLEAR_BACKGROUND_BMP)
display_setup(magtag, SCREEN_LINES)
wifi = connect_to_wiFi(magtag)
requests = setup_requests()
clear_screen(magtag, SCREEN_LINES)
print_header(magtag, endpoint_list, True)

# Main Loop
# If 30s has past since the last roundg et the API
# If errors then we are in an error state
# Play error sound once
# Flash Neopixels red
# Show errors to the screen
# Wait 5 minutes before checking again
# else
# wait 30s before checking API again
api_time_to_check = time.monotonic()  # Time in seconds since power on
error_time_to_check = time.monotonic()
while True:
  now = time.monotonic()
  # if we are not in error state, check the api every 30s
  if not error_state:
    if (now - api_time_to_check > API_CHECK_PERIOD) or first_time:
      # We are in a good position, set the lights green
      # and start checking enpoints
      set_lights(magtag, "green", 0.01)
      endpoint_errors = api_check(magtag, requests, ENPOINT_BASE, endpoint_list)
      # for now clear the lights and see how it works
      set_lights(magtag, "clear")

      # now check to see if there were any errors
      error_state = True if len(endpoint_errors) > 0 else False
      if error_state:
        play_error_sound(magtag, "error")
        set_lights(magtag, "red", 0.5)
        print_errors(magtag, endpoint_errors, ERROR_LINE_HEADER_START, MAX_STRING_WIDTH, SCREEN_LINES)

      # If we're not in an error state, indicate to the user that 
      # we're in standby mode and make the lights turn yellow
      if not error_state:
        set_lights(magtag,"yellow")

      # and lastly reset time so we can check again
      api_time_to_check = time.monotonic()

  # if we are in error state, only check the api every 300s
  elif error_state:
    if (now - api_time_to_check > ERROR_CHECK_PERIOD):
      endpoint_errors = api_check(magtag, requests, ENPOINT_BASE, endpoint_list)
      # now check to see if there were any errors
      error_state = True if len(endpoint_errors) > 0 else False

      if error_state:
        play_error_sound(magtag, "error")
        set_lights(magtag, "red", 0.5)
        print_errors(magtag, endpoint_errors, ERROR_LINE_HEADER_START, MAX_STRING_WIDTH, SCREEN_LINES)
      elif not error_state:
        error_state = False
        set_lights(magtag, "clear")

    # and lastly reset time so we can check again
    api_time_to_check = time.monotonic()

  # make sure first_time is set to False
  first_time = False
