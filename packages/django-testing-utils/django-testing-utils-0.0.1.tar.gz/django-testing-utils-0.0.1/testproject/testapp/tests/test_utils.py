from django.test import SimpleTestCase

from django_testing_utils.utils import (override_defaults)
from testproject.testapp.tests import default_settings


class OverrideDefaultsTests(SimpleTestCase):
    """ override_defaults test case. """

    def test_original_value(self):
        """ Check the original setting value. """
        self.assertEqual('original', default_settings.setting_1)

    @override_defaults('testproject.testapp.tests.default_settings',
                       setting_1='changed')
    def test_decorator_using_module_name(self):
        """ Check the setting value overridden using the module name. """
        self.assertEqual('changed', default_settings.setting_1)

    @override_defaults(default_settings, setting_1='changed')
    def test_decorator_using_module_ref(self):
        """ Check the setting value overridden using the module reference. """
        self.assertEqual('changed', default_settings.setting_1)

    def test_context_manager_using_module_name(self):
        """ Check the setting value overridden using the module name. """
        self.assertEqual('original', default_settings.setting_1)
        with override_defaults('testproject.testapp.tests.default_settings',
                               setting_1='changed'):
            self.assertEqual('changed', default_settings.setting_1)
        self.assertEqual('original', default_settings.setting_1)

    def test_context_manager_using_module_ref(self):
        """ Check the setting value overridden using the module reference. """
        self.assertEqual('original', default_settings.setting_1)

        with override_defaults(default_settings, setting_1='changed'):
            self.assertEqual('changed', default_settings.setting_1)

        self.assertEqual('original', default_settings.setting_1)
