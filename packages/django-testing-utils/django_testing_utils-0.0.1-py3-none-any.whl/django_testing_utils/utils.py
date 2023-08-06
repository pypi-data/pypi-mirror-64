from types import ModuleType
from typing import Union
from unittest import mock

from django.test.utils import TestContextDecorator

class override_defaults(TestContextDecorator):
    """
    A tool for convenient override default values in config files

    Act as either a decorator or a context manager. If it's a decorator, take a
    function and return a wrapped function. If it's a contextmanager, use it
    with the ``with`` statement. In either event, entering/exiting are called
    before and after, respectively, the function/block is executed.
    """
    enable_exception = None

    def __init__(self, settings_file: Union[ModuleType, str], **kwargs):
        """ Save initial parameters.

        :param settings_file: the name or reference on setting file
        :param kwargs: settings file attributes and values to override
        """
        if isinstance(settings_file, str):
            self.module = settings_file
        else:
            self.module = settings_file.__name__
        self.settings = kwargs
        self.patchers = []
        super().__init__()

    def enable(self):
        """ Create patchers, start save and start them. """
        for settings, value in self.settings.items():
            patcher = mock.patch(f'{self.module}.{settings}', value)
            self.patchers.append(patcher)
            patcher.start()

    def disable(self):
        """ Stop patchers. """
        for patcher in self.patchers:
            patcher.stop()

