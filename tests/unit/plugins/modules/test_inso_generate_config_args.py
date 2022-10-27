from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest import TestCase
from ansible_collections.kong.kong.plugins.modules import inso_generate_config

# Tests Module Arguments onlys
class TestInsoGenerateConfig(TestCase):


    def test_format(self):
        spec = inso_generate_config.arguments()["format"]

        self.assertTrue(spec["type"] == "str")

        choices_expected = ["yaml", "json"]
        self.assertTrue(spec["choices"] == choices_expected)

        self.assertTrue(spec["required"] == False)

    def test_identifier(self):
        spec = inso_generate_config.arguments()["identifier"]

        self.assertTrue(spec["type"] == "str")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == True)

    def test_output(self):
        spec = inso_generate_config.arguments()["output"]

        self.assertTrue(spec["type"] == "path")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == False)

    def test_tags(self):
        spec = inso_generate_config.arguments()["tags"]

        self.assertTrue(spec["type"] == "list")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == False)

    def test_type(self):
        spec = inso_generate_config.arguments()["type"]

        self.assertTrue(spec["type"] == "str")

        choices_expected = ["declarative", "kubernetes"]
        self.assertTrue(spec["choices"] == choices_expected)

        self.assertTrue(spec["required"] == False)


