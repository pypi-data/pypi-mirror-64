from .topical_manager import TopicalManager
from functools import wraps

topical = TopicalManager()

def topical_event_decorator(event):
    def wrapper(fn):
        topical.subscribe(event, fn)

        @wraps(fn)
        def wrapped(*args, **kwargs):
            fn(*args, **kwargs)
        return wrapped
    return wrapper

topical.event = topical_event_decorator
