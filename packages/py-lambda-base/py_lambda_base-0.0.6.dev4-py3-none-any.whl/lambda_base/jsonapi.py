from functools import wraps
from .route_holder import RouteHolder

def jsonapi(reject_if_no_data=False):
  def decorator_wrapper(func):
    holder = RouteHolder()
    holder.add_route_partial(func, jsonapi=True)

    @wraps(func)
    def func_wrapper(req, *args, **kwArgs):
      if reject_if_no_data and not req.data:
        respondent.set_error("Body is not a valid JSONAPI object")
        respondent.set_status(400)
        return
        
      return func(*args, **kwArgs)
    return func_wrapper
  return decorator_wrapper
