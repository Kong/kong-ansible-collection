from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils import basic
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from ansible_collections.kong.kong.plugins.modules import inso_generate_config
from ansible_collections.kong.kong.tests.utils.ansible_module_mock import (
    AnsibleFailJson,
    AnsibleExitJson,
    exit_json,
    fail_json,
    get_bin_path,
    set_module_args,
)

class TestInsoGenerateConfig(TestCase):
    
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
            inso_generate_config.main()
    
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
                inso_generate_config.main()
            self.assertTrue(result.exception.args[0]['changed']) # ensure result is changed
            self.assertEqual(result.exception.args[0]['rc'], 0)

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'generate', 'config', 
            '--ci', '--printOptions', 'spc_46c5a4'], use_unsafe_shell=False)

#this test is throwing a index out of range when stdout is not at least 2 lines
    def test_type_command(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "type" : "declarative"
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_generate_config.main()
            self.assertTrue(result.exception.args[0]['changed']) # ensure result is changed

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'generate', 'config', 
            '--ci', '--printOptions', '--type', 'declarative' ,'spc_46c5a4'], use_unsafe_shell=False)

#when the output is defined, the logic on line 304 of the module breaks.
    def test_output_format(self):
        set_module_args({
            "identifier": "spc_46c5a4", 
            "output" : "output.json", 
            "format" : "json"
        })

        with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
            stdout = 'configuration updated \n second line \n third line \n'
            stderr = ''
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as result:
                inso_generate_config.main()
            self.assertTrue(result.exception.args[0]['changed']) # ensure result is changed

        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'generate', 'config', 
            '--ci', '--printOptions', '--format', 'json', '--output', 'output.json' ,'spc_46c5a4'], use_unsafe_shell=False)

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
                inso_generate_config.main()
            self.assertFalse(result.exception.args[0]['changed'])
            self.assertEqual(result.exception.args[0]['rc'], 1)
            
        mock_run_command.assert_called_once_with(args=['/usr/bin/inso', 'generate', 'config', 
            '--ci', '--printOptions', 'spc_46c5a4'], use_unsafe_shell=False)