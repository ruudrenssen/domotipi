class Event(object):
    def __init__(self, doc=None):
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return EventHandler(self, obj)

    def __set__(self, obj, value):
        pass


class EventHandler(object):
    def __init__(self, event, obj):
        self.event = event
        self.obj = obj

    def _get_function_list(self):
        """(internal use) """
        try:
            event_handler = self.obj.__event_handler__
        except AttributeError:
            event_handler = self.obj.__event_handler__ = {}
        return event_handler.setdefault(self.event, [])

    def add(self, func):
        """Add new event handler function.
        Event handler function must be defined like func(sender, earg).
        You can add handler also by using '+=' operator.
        """
        self._get_function_list().append(func)
        return self

    def remove(self, func):
        """Remove existing event handler function.
        You can remove handler also by using '-=' operator.
        """
        self._get_function_list().remove(func)
        return self

    def fire(self, earg=None):
        """Fire event and call all handler functions
        You can call EventHandler object itself like e(earg) instead of
        e.fire(earg).
        """
        for func in self._get_function_list():
            func(self.obj, earg)
    __iadd__ = add
    __isub__ = remove
    __call__ = fire
