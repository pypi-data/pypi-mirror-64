import json_api_doc
from .route_parser import parse_route_for_path

class EnhancedRequest:
  def __init__(self, event, route):
    self.event = event
    self.route = route
    self.body = {}
    self.data = {}

    params = {}
    if event['queryStringParameters']:
      params = {**params, **event['queryStringParameters']}
    if event['multiValueQueryStringParameters']:
      params = {**params, **event['multiValueQueryStringParameters']}
    params = {**params, **event['pathParameters']}
    if event['body']:
      params['raw_body'] = event['body']
      params['parsed_body'] = {}
      if re.search('json', event['headers'].get('content-type', ''), re.IGNORECASE):
        try:
          parsed_body = json.loads(event['body'])
          params['parsed_body'] = {**parsed_body}
          params = {**params, **parsed_body}
          self.body = parsed_body
        except json.JSONDecodeError:
          pass
      if route['jsonapi'] and 'data' in self.body:
        self.data = json_api_doc.deserialize(self.body['data'])

    params = {**params, **parse_route_for_path(route['route'], event['pathParameters'].get('proxy', ''))}
    self.params = params
  
  @property
  def params(self):
    return self.params

  @property
  def body(self):
    return self.body

  @property
  def data(self):
    return self.data

  @property
  def event(self):
    return self.event

  @property
  def route(self):
    return self.route