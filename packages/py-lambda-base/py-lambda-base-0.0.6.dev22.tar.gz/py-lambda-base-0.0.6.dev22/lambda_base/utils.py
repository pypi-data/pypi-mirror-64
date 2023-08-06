def fetch_header_from_event(event, header_name):
  header_name = header_name.lower()
  actual_key = next((header for header in event['headers'].keys() if header_name == header.lower()), None)
  if actual_key is None:
    return None
  return (actual_key, event['headers'][actual_key])
def fetch_header_value_from_event(event, header_name, return_string=False):
  result = fetch_header_from_event(event, header_name)
  if result is not None:
    return result[1]
  if return_string:
    return ''
  return None