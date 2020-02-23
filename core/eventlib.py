"""
The event machinery
"""

import logging
import re
from typing import Callable

from kge.core.events import Event

__all__ = (
    'EventMixin', 'BadEventHandlerException',
)

boundaries_finder = re.compile('(.)([A-Z][a-z]+)')
boundaries_finder_2 = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(txt):
    s1 = boundaries_finder.sub(r'\1_\2', txt)
    return boundaries_finder_2.sub(r'\1_\2', s1).lower()


class BadEventHandlerException(TypeError):

    def __init__(self, instance, method, event):
        object_type = type(instance)
        event_type = type(event)
        o_name = object_type.__name__
        e_name = event_type.__name__
        article = ['a', 'an'][int(e_name.lower()[0] in "aeiou")]

        message = f"""
{o_name}.{method}() signature incorrect, it should accept {article} {e_name} object and a dispatch function.

{e_name} is a dataclass that represents an event. Its attributes 
tell you about the event.

The dispatch function is a function you can call that accepts an event instance
as its only parameter. Call it to add an event to the queue. You don't have to
use it, but it is a mandatory argument provided by kge.

It should look like this:

def {method}({e_name.lower()}_event: {e_name}, dispatch_function):
    (Your code goes here.)
"""
        super().__init__(message)


class EventMixin:
    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]) -> None:
        """
        Launch an event handler for this event

        :param event: the event to be processed
        :param dispatch: function for calling another event
        :return: None
        """
        elog = logging.getLogger('game.events')

        name = camel_to_snake(type(event).__name__)
        meth_name = 'on_' + name
        meth = getattr(self, meth_name, None)

        if callable(meth):
            try:
                elog.debug(f"Calling handler {meth} for {name}")
                meth(event, dispatch)
            except TypeError as ex:
                from inspect import signature
                sig = signature(meth)
                try:
                    sig.bind(event, dispatch)
                except TypeError:
                    raise BadEventHandlerException(self, meth_name, event) from ex
                else:
                    raise