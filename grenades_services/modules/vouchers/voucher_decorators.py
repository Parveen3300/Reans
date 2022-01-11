"""deprecated
Voucher helper class
"""

import warnings


class RemovedInOscar32Warning(DeprecationWarning):
    pass


def _deprecated_cls(cls, warn_cls=RemovedInOscar32Warning):
    class Deprecated(cls):
        def __init__(self, *args, **kwargs):
            message = "Class '%s' is deprecated and will be " \
                      "removed in the next version of django-oscar" \
                      % cls.__name__
            warnings.warn(message, warn_cls, stacklevel=2)
            super().__init__(*args, **kwargs)

    return Deprecated


def _deprecated_func(f, warn_cls=RemovedInOscar32Warning):
    def _deprecated(*args, **kwargs):
        message = "Method '%s' is deprecated and will be " \
                  "removed in the next version of django-oscar" \
                  % f.__name__
        warnings.warn(message, warn_cls, stacklevel=2)
        return f(*args, **kwargs)

    return _deprecated


def deprecated(obj):
    """deprecated
    This is a third party oscar level modules to handle to oscar basket and catalogue models
    return : _deprecated_cls with class objects and function objects
    """
    return (_deprecated_cls(cls=obj) 
            if isinstance(obj, type) else 
            _deprecated_func(f=obj))
