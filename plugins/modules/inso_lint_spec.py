#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Kong Inc.
# SPDX-License-Identifier: Apache-2.0

DOCUMENTATION = r'''
---
module: inso_lint_spec

short_description: Validates your OpenAPI specification.

version_added: "1.2.0"

description:
- The inso_lint_spec module lints and validates your OpenAPI specification with the 'inso' CLI.
- Lint results will be returned in the module's results.
- Inso CLI will exit with a non-zero exit code if linting fails, and the module run will fail.

options:
    identifier:
        description: 
        - A specification name, or id, or a file path.
        type: str
        required: true

extends_documentation_fragment:
    - kong.kong.inso_args_common

author:
    - Andrew J. Huffman (https://github.com/ahuffman)
'''

EXAMPLES = r'''
# Lint an OpenAPI specification
- name: "Lint OpenAPI specification"
  kong.kong.inso_lint_spec:
    identifier: "/path/to/my/oapi_spec.json"

# Lint OpenAPI specification and register results
- name: "Lint OpenAPI specification and register results"
  kong.kong.inso_lint_spec:
    identifier: "/path/to/my/oapi_spec.json"
  register: "openapi_lint_results"

- name: "View the OpenAPI linting results"
  ansible.builtin.debug:
    var: "openapi_lint_results"
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
    
    spec["identifier"] = {
        "type": "str",
        "required": True
    }

    return spec


def build_lint_spec_cmd(module):
    cmd = []

    cmd.append(module.params["identifier"])

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
    cmd = build_base_cmd(module) + build_lint_spec_cmd(module)

    # inject sub-commands into command
    cmd.insert(1, "lint")
    cmd.insert(2, "spec")

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
