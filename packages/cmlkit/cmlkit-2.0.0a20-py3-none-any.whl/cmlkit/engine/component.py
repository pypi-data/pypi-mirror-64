"""Component."""

from cmlkit import logger
from .config import Configurable


class Component(Configurable):
    """Base class for cmlkit components.

    Provides the mechanism for passing context to objects.
    (See explanation in readme!)

    All context variables must have a default value set in the `default_context`
    of the class. This is to ensure that passing an empty context will never
    result in an error.

    """

    # define this in subclass if certain context variables are required
    default_context = {}

    def __init__(self, context={}):  # pylint: disable=dangerous-default-value
        # import global context here so that it can be changed dynamically in a running session
        from cmlkit import default_context as global_default_context

        # special case: if context includes a sub-dict
        # under the key that is the name of this class,
        # use this context instead (important for nested instantiation)
        if self.get_kind() in context:
            # the context for this class is expanded into this
            # class' context, while retaining the full dict,
            # so if this component instantiates other components,
            # they get a shot at having some context passed to them
            # as well!
            context = {**context, **context[self.get_kind()]}

        self.context = {
            **global_default_context,
            **self.__class__.default_context,
            **context,
        }

        logger.debug(f"Context for {self.get_kind()} is {self.context}.")

        # you should probably also implement something more here
