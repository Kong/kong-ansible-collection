from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest import TestCase
from ansible_collections.kong.kong.plugins.modules import inso_run_test

# Tests Module Arguments onlys
class TestInsoRunTestArgs(TestCase):

    def test_identifier(self):
        spec = inso_run_test.arguments()["identifier"]

        self.assertTrue(spec["type"] == "str")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == True)

    def test_bail(self):
        spec = inso_run_test.arguments()["bail"]

        self.assertTrue(spec["type"] == "bool")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == False)

    def test_disable_cert_validation(self):
        spec = inso_run_test.arguments()["disable_cert_validation"]

        self.assertTrue(spec["type"] == "bool")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == False)

    def test_env(self):
        spec = inso_run_test.arguments()["env"]

        self.assertTrue(spec["type"] == "str")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == False)

    def test_keep_file(self):
        spec = inso_run_test.arguments()["keep_file"]

        self.assertTrue(spec["type"] == "bool")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == False)

    def test_reporter(self):
        spec = inso_run_test.arguments()["reporter"]

        self.assertTrue(spec["type"] == "str")
        self.assertEquals(spec["choices"], ["dot", "list", "spec", "min", "progress"])

        self.assertTrue(spec["required"] == False)
    
    def test_test_name_pattern(self):
        spec = inso_run_test.arguments()["test_name_pattern"]

        self.assertTrue(spec["type"] == "str")
        
        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == False)