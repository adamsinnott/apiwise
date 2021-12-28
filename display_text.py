from peripherals import play_error_sound

def print_errors(magtag, endpoint_errors, error_screen_start, max_string_width, screen_lines):
  if len(endpoint_errors) > 0:
    if len(endpoint_errors) == 1:
      magtag.set_text(
        "There is an error",
        index=error_screen_start,
        auto_refresh=False,
      )
    else:
      magtag.set_text(
        "There are " + str(len(endpoint_errors)) + " errors",
        index=error_screen_start,
        auto_refresh=False,
      )
    for index, error in enumerate(endpoint_errors):
      if index + error_screen_start < screen_lines:
        error_endpoint_name = error["endpoint_name"]
        magtag.set_text(
          error_endpoint_name[:max_string_width]
          + ": "
          + str(error["status_code"]),
          index=index + error_screen_start,
          auto_refresh=False,
        )
    magtag.refresh()