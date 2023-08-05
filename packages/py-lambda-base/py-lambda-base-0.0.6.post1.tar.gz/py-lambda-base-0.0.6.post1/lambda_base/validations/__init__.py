from dpath.util import get
from functools import wraps
from .route_holder import RouteHolder

def _no_blank(value):
  """must not be blank"""
  return value == ''

_VALIDATIONS_FAILS = {
  'no-blank': _no_blank
}

def _required_source_param(req_key, error_stub, param_path, *, field_name, validations):
  def decorator_wrapper(func):
    @wraps(func)
    def func_wrapper(req, *, respondent, **kwArgs):
      public_name = param_path.split('/')[-1]
      if field_name is not None:
        public_name = field_name
      try:
        value = str(get(getattr(req, req_key), param_path))
      except KeyError:
        respondent.set_error("Missing required {} {}".format(error_stub, public_name))
        respondent.set_status(400)
        return

      for validation_type in validations:
        if validation_type in _VALIDATIONS_FAILS:
          if _VALIDATIONS_FAILS[validation_type](value):
            respondent.set_error("{cap_error_stub} '{field_name}' {explanation}".format(
              cap_error_stub=error_stub.capitalize(),
              field_name=public_name,
              explanation=_VALIDATIONS_FAILS[validation_type].__doc__
            ))
            respondent.set_status(400)
            return

      return func(*args, **kwArgs)
    return func_wrapper
  return decorator_wrapper


def requires_body_param(param_path, field_name=None, validations=[]):
  return _required_source_param('body', 'field', param_path, field_name=field_name, validations=validations)

def requires_data_param(param_path, field_name=None, validations=[]):
  return _required_source_param('data', 'field', param_path, field_name=field_name, validations=validations)
