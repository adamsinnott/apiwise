# from peripherals import set_lights

def api_check(magtag, requests, endpoint_base, endpoints):
  endpoint_errors = []
  # set_lights(magtag, "green", 0.01)
  for index, endpoint in enumerate(endpoints):
    print("endpoint")
    print(endpoint)
    try:
      response = requests.get(str(endpoint_base + endpoint))
      if response.status_code > 399:
        error_object = {
          "endpoint_name": endpoint,
          "status_code": response.status_code,
        }
        endpoint_errors.append(error_object)
        response.close()
    except AssertionError as error:
      pass
  # set_lights(magtag, "clear")
  return endpoint_errors
