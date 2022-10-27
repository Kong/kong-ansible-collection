from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils import basic
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from ansible_collections.kong.kong.plugins.modules import inso_run_test
from ansible_collections.kong.kong.tests.utils.ansible_module_mock import (
    AnsibleFailJson,
    AnsibleExitJson,
    exit_json,
    fail_json,
    get_bin_path,
    set_module_args,
)

class TestInsoRunTest(TestCase):

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
            inso_run_test.main()

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
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions', 'spc_46c5a4'], use_unsafe_shell=False)

# test env with suite name
    def test_env(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "env": '"OpenAPI env"',
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions','spc_46c5a4', '--env','"OpenAPI env"'], use_unsafe_shell=False)

    def test_test_name_pattern_and_env(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "test_name_pattern": "Math",
            "env": "env_env_ca046a"
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions','spc_46c5a4', '--env','env_env_ca046a', '--testNamePattern', 'Math'], use_unsafe_shell=False)
    
    def test_reporter(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "reporter": "progress",
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions','spc_46c5a4', '--reporter','progress'], use_unsafe_shell=False)

    def test_bail_false(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "bail": False,
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions','spc_46c5a4'], use_unsafe_shell=False)

    def test_bail_true(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "bail": True,
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions','spc_46c5a4', '--bail'], use_unsafe_shell=False)

    def test_keepfile_true(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "keep_file": True,
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed']) # ensure result has not changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions','spc_46c5a4', '--keepFile'], use_unsafe_shell=False)
    
# Test default command executed
    def test_rc_1_thrown(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = 'There was an error while generating configuration'
            rc = 1
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleFailJson) as result:
                inso_run_test.main()
            self.assertFalse(result.exception.args[0]['changed'])
            self.assertEqual(result.exception.args[0]['rc'], 1)
            
        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'run', 'test',
            '--ci', '--printOptions', 'spc_46c5a4'], use_unsafe_shell=False)