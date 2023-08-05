class Dispatcher:
    """A generic and simple event dispatcher"""
    _listeners = dict

    def __init__(self):
        self._listeners = {}

    def attach(self, event_name, listener: callable):
        if event_name not in self._listeners:
            self._listeners[event_name] = []

        self._listeners[event_name].append(listener)

    def emit(self, event_name, *args, **kwargs):
        if event_name not in self._listeners:
            return

        for callback in self._listeners[event_name]:
            callback(*args, **kwargs)

    def remove(self, event_name, listener_to_remove: callable):
        if event_name not in self._listeners:
            return

        for key, listener in enumerate(self._listeners[event_name]):
            if listener == listener_to_remove:
                del self._listeners[event_name][key]