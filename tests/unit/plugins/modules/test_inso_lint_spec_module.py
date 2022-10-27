from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils import basic
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from ansible_collections.kong.kong.plugins.modules import inso_lint_spec
from ansible_collections.kong.kong.tests.utils.ansible_module_mock import (
    AnsibleFailJson,
    AnsibleExitJson,
    exit_json,
    fail_json,
    get_bin_path,
    set_module_args,
)

class TestInsoLintSpec(TestCase):
    
    def setUp(self):
        self.mock_module_helper = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
            get_bin_path=get_bin_path,
        )
        self.mock_module_helper.start()

        self.addCleanup(self.mock_module_helper.stop)
    
    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            inso_lint_spec.main()

    def test_default_command(self):
        set_module_args({
            "identifier": "spc_46c5a4"
        })       

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_lint_spec.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'lint', 'spec',
            '--ci', '--printOptions', 'spc_46c5a4'], use_unsafe_shell=False)

# Test default command executed, but return a 
    def test_rc_1_thrown(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 1
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleFailJson) as result:
                inso_lint_spec.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 1)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'lint', 'spec',
            '--ci', '--printOptions', 'spc_46c5a4'], use_unsafe_shell=False)
