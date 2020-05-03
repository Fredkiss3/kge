import kge
from kge.core.component import BaseComponent


class Behaviour(BaseComponent):
    """
    A behavior represents an element that can be added to an entity
    to add a « behaviour » to a game object (like moving the player for example).

    In order to to do so, we must use event handlers.

    Their signatures are :
    def on_{event_name}(self, event_type, dispatch_function):
        (your code goes here)

    Where :
        - event_name is the name of the event in snake_case
        - event_type is the event, you should use that, it contains a lot of important parameters
        - dispatch_function is a function to call in order to send messages, in practice, you won't use it so much

    Example of an event handler :

    >>> class PlayerMovement(Behaviour):
    >>>     def on_update(self, event, dispatch):
    >>>         print("Moving the player...")

    If you want to know a list of all events, you should see in module ``kge.core.events``
    """

    def __new__(cls, entity=None):
        inst = super().__new__(cls)

        if entity is not None:
            if not isinstance(entity, kge.Entity):
                raise TypeError("entity should be of type 'kge.Entity' or a subclass of 'kge.Entity'")
        inst.entity = entity

        # Used to Initialize component
        inst._initialized = False

        # Used to tell if the component is active
        inst.is_active = True

        return inst

    def __repr__(self):
        return f"behaviour {type(self).__name__} of entity '{self.entity}'"
