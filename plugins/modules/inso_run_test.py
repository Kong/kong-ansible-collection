#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Kong Inc.
# SPDX-License-Identifier: Apache-2.0

DOCUMENTATION = r'''
---
module: inso_run_test

short_description: Run Insomnia unit test suites

version_added: "1.2.0"

description:
- The 'inso_run_test' module enables you to execute unit tests written inside Insomnia from Ansible.
- On execution, results from Inso CLI will report test results, and exit with an exit code.
- Inso CLI will exit with a non-zero exit code if linting fails.

options:
    bail:
        description:
        - Abort (“bail”) after the first test failure
        type: bool
        required: false
    disable_cert_validation:
        description:
        - Disable certificate validation for requests with SSL
        type: bool
        required: false
    env:
        description:
        - the environment to use - an environment name or id
        type: str
        required: false
    identifier:
        description: 
        - A specification name, or id, or a file path.
        type: str
        required: true
    keep_file:
        description:
        - Do not delete the generated test file (useful for debugging)
        type: bool
        required: false
    reporter:
        description:
        - reporter to use.
        - Options are dot, list, spec, min and progress 
        default: spec
        choices: [dot, list, spec, min, progress]
        required: false
    test_name_pattern:
        description:
        - Run tests that match the regex
        type: str
        required: false

extends_documentation_fragment:
    - kong.kong.inso_args_common

author:
    - Andrew J. Huffman (https://github.com/ahuffman)
'''

EXAMPLES = r'''

'''


RETURN = r'''
changed:
    description: Whether the module made a change to the system, this will always return 'False'
    returned: always
    type: bool
cmd:
    description: The 'inso' CLI command and arguments that were run.
    returned: always
    type: list
    elements: str
    sample: '["/usr/local/bin/inso", "lint", "spec", "--ci", "--printOptions", "my identifier"]'
failed:
    description: Whether the module failed or not
    returned: always
    type: bool
log:
    description: Dictionary containing log output from the 'inso' CLI run.
    returned: success
    type: complex
    contains:
        options:
            description: The 'inso' CLI stdout log of options the command was run with
            returned: always
            sample: "[log] Loaded options { ci: true, printOptions: true }"
            type: str
        results:
            description:
            - The 'inso' CLI stdout log of the lint operation.
            - If the lint operation fails, the problems in the OpenAPI specification will be reported.
            returned: always
            sample: "[log] No linting errors. Yay!"
            type: str
rc:
    description: Return code of the 'inso' CLI run.
    returned: always
    type: int
stderr:
    description: Raw standard error (stderr) output from the 'inso' CLI run.
    returned: always
    type: str
stderr_lines:
    description: Standard error output (stderr) from the 'inso' CLI run in list format.
    returned: always
    type: list
    elements: str
stdout:
    description: Raw standard output (stdout) from the 'inso' CLI run.
    returned: always
    type: str
stdout_lines:
    description: Standard output (stdout) from the 'inso' CLI run in list format.
    returned: always
    type: list
    elements: str
'''

from ansible.module_utils.basic import AnsibleModule

# common inso command options
from ansible_collections.kong.kong.plugins.module_utils.inso_args_common import (
    COMMON_ARG_SPEC,
    build_base_cmd
)

import copy


def arguments():
    # Extending the base command and global (common) arguments
    ## these are imported from the module util
    spec = copy.deepcopy(COMMON_ARG_SPEC)
    spec["bail"] = {
        "type": "bool",
        "requried": False
    }

    spec["disable_cert_validation"] = {
        "type": "bool",
        "required": False
    }

    spec["env"] = {
        "type": "str",
        "required": False
    }

    spec["identifier"] = {
        "type": "str",
        "required": True
    }

    spec["keep_file"] = {
        "type": "bool",
        "required": False
    }

    spec["reporter"] = {
        "type": "str",
        "required": False,
        "choices": ["dot", "list", "spec", "min", "progress"]
    }

    spec["test_name_pattern"] = {
        "type": "str",
        "required": False
    }

    return spec


def build_run_test_cmd(module):
    cmd = []

    # identifier
    cmd.append(module.params["identifier"])

    # --bail
    if module.params["bail"]:
        cmd.append("--bail")

    # --disableCertValidation
    if module.params["disable_cert_validation"]:
        cmd.append("--disableCertValidation")

    # --env
    if module.params["env"]:
        cmd.append("--env")
        cmd.append(module.params["env"])

    # --keepFile
    if module.params["keep_file"]:
        cmd.append("--keepFile")

    # --reporter
    if module.params["reporter"]:
        cmd.append("--reporter")
        cmd.append(module.params["reporter"])

    # --testNamePattern
    if module.params["test_name_pattern"]:
        cmd.append("--testNamePattern")
        cmd.append(module.params["test_name_pattern"])

    return cmd


def run_module():
    result = {
        "changed": False
    }

    module = AnsibleModule(
        argument_spec=arguments(),
        supports_check_mode=True
    )

    # build command args list
    cmd = build_base_cmd(module) + build_run_test_cmd(module)

    # inject sub-commands into command
    cmd.insert(1, "run")
    cmd.insert(2, "test")

    # return command args in result
    result["cmd"] = cmd
    result["rc"], result["stdout"], result["stderr"] = module.run_command(
        args=cmd,
        use_unsafe_shell=False
    )

    result["log"] = {}

    # setup return output
    stdout_lines = result["stdout"].split("\n")
    result["log"]["options"] = stdout_lines[0]
    result["log"]["results"] = stdout_lines[2:]
    
    if result["rc"] != 0:
        module.fail_json(
            msg="Non-zero return-code from 'inso' command",
            **result
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

