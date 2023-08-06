from ap.topical.topical_event_payload import TopicalEventPayload

def topical_event(fn):
    def wrapper(payload:TopicalEventPayload, *args, **kwargs):
        payload.accessed_by(fn.__name__)

        return fn(payload, *args, **kwargs)

    return wrapper
