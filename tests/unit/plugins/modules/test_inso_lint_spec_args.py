from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest import TestCase
from ansible_collections.kong.kong.plugins.modules import inso_lint_spec

# Tests Module Arguments onlys
class TestInsoLintSpec(TestCase):

    def test_identifier(self):
        spec = inso_lint_spec.arguments()["identifier"]

        self.assertTrue(spec["type"] == "str")

        self.assertFalse("choices"in spec)

        self.assertTrue(spec["required"] == True)
