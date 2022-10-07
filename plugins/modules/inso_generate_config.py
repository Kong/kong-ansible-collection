#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Kong Inc.
# SPDX-License-Identifier: Apache-2.0

DOCUMENTATION = r'''
---
module: inso_generate_config

short_description: Generate Kong Gateway and Kong Ingress Controller configurations

version_added: "1.2.0"

description:
- Generates a configuration from an API specification by using openapi-2-kong.
- The command works similarly to generating a declarative configuration file or Kubernetes manifest from within Insomnia.

options:
    format:
        description:
        - Output format. This option only applies to type 'declarative', and will be ignored for type 'kubernetes'.
        type: str
        choices: [ yaml, json ]
        default: yaml
        required: false
    identifier:
        description: 
        - A specification name, or id, or a file path.
        type: str
        required: true
    output:
        description:
        - Save the generated config to a file
        type: path
        required: false
    tags:
        description:
        - List of tags to apply to each entity
        type: list
        required: false
    type:
        description:
        - Type of configuration to generate
        type: str
        choices: [ declarative, kubernetes ]
        default: declarative
        required: false

extends_documentation_fragment:
    - kong.kong.inso_args_common

author:
    - Andrew J. Huffman (https://github.com/ahuffman)
'''

EXAMPLES = r'''
# Generate a KIC config
- name: "Generate Kong Ingress Controller config"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
    type: "kubernetes"
    output: "/tmp/kic.yaml"
    tags:
      - dev
      - v2alpha1

# Generate a decK config in yaml format
- name: "Generate Kong Gateway declarative config | yaml"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
    output: "/tmp/deck.yaml"

# Generate a decK config in json format
- name: "Generate Kong Gateway declarative config | json"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
    output: "/tmp/deck.json"
    format: "json"

# Generate a decK config with no output file, store the result, and copy it to the Ansible control node
- name: "Generate Kong Gateway declarative | no output"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
  register: "deck_config"

- name: "Copy the config to localhost"
  ansible.builtin.copy:
    content: "{{ deck_config.output.configuration }}"
    dest: "/tmp/deck.yaml"
  delegate_to: "localhost"

# Generate a decK config with no output file, store the result, and view the result
- name: "Generate Kong Gateway declarative | no output"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
  register: "deck_config_out"

- name: "View the result of inso_generate_config"
  ansible.builtin.debug:
    var: "deck_config_out"

- name: "Set the configuration to a variable for further manipulation"
  ansible.builtin.set_fact:
    deck_config: "{{ deck_config_out.output.configuration | from_yaml }}"
'''

RETURN = r'''
changed:
    description: Whether the module made a change to the system
    returned: always
    type: bool
cmd:
    description: The 'inso' CLI command and arguments that were run.
    returned: always
    type: list
    elements: str
    sample: '["/usr/local/bin/inso", "generate", "config", "--ci", "--printOptions", "my identifier"]'
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
            returned: success
            sample: "[log] Loaded options { type: 'declarative', format: 'yaml', ci: true, printOptions: true }"
            type: str
        output_path:
            description:
            - The 'inso' CLI stdout log of the path the generated Configuration was output to.
            - If the 'output' parameter was not specificed, or run with check-mode, this will be marked as "stdout"
            returned: success
            sample: "[log] Configuration generated to \"/tmp/ansible_deck_output.yaml\""
            type: str
output:
    description:
    - When the 'output' parameter is not specified, or run in check-mode, this will be populated
    - with the raw configuration string from stdout as well as a list formatted version.
    - The stored configuration data could then be used without writing to disk.
    returned: success
    type: complex
    contains:
        configuration:
            description:
            - Raw configuration string from stdout generated by the 'inso' CLI.
            - This will only be returned if the module was run without the 'output' parameter or
            - if the module was run in check-mode.
            returned: success
            type: str
        configuration_lines:
            description:
            - Configuration from stdout generated by the 'inso' CLI.
            - This will only be returned if the module was run without the 'output' parameter or
            - if the module was run in check-mode.
            returned: success
            type: list
            elements: str
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
    spec = copy.deepcopy(COMMON_ARG_SPEC)
    
    spec["format"] = {
            "type": "str",
            "choices": ["yaml", "json"],
            "required": False
        }

    spec["identifier"] = {
            "type": "str",
            "required": True
        }

    spec["output"] = {
            "type": "path",
            "required": False
        }

    spec["tags"] = {
            "type": "list",
            "required": False
        }

    spec["type"] = {
            "type": "str",
            "choices": ["declarative", "kubernetes"],
            "required": False
        }

    return spec


def build_gen_cfg_cmd(module):
    cmd = []

    # --format
    if module.params["format"]:
        cmd.append("--format")
        cmd.append(module.params["format"])
    
    # --output
    if module.params["output"]:
        # omit output of config in check-mode
        if not module.check_mode:
            cmd.append("--output")
            cmd.append(module.params["output"])
    
    # --tags
    if module.params["tags"]:
        cmd.append("--tags")
        cmd.append(",".join(module.params["tags"]))
    
    # --type
    if module.params["type"]:
        cmd.append("--type")
        cmd.append(module.params["type"])

    # identifier needs to be last, and is a required parameter
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
    cmd = build_base_cmd(module) + build_gen_cfg_cmd(module)

    # inject sub-commands into command
    cmd.insert(1, "generate")
    cmd.insert(2, "config")

    # return command args in result
    result["cmd"] = cmd
    result["rc"], result["stdout"], result["stderr"] = module.run_command(
        args=cmd,
        use_unsafe_shell=False
    )
    result["log"] = {}
    result["output"] = {}

    # setup return output
    stdout_lines = result["stdout"].split("\n")
    # check-mode & output param not passed
    if "--output" not in cmd:
        result["log"]["options"] = stdout_lines[0]
        result["log"]["output_path"] = "stdout"
        # stdout output prefixes first line of config with "[log] "
        config_line = stdout_lines[2].split("[log] ")
        result["output"]["configuration_lines"] = config_line[1:] + stdout_lines[3:]
        result["output"]["configuration"] = "\n".join(result["output"]["configuration_lines"])
    # output param passed
    else:
        options = []
        for i in range(len(stdout_lines)):
            if stdout_lines[i] == "":
                result["log"]["output_path"] = stdout_lines[i + 1]
                break
            options.append(stdout_lines[i])
        result["log"]["options"] = "".join(options)
    
    # return changed if command successful
    if result["rc"] == 0:
        # no changes made if in check_mode
        if not module.check_mode:
            result["changed"] = True
    else:
        module.fail_json(
            msg="Non-zero return-code from 'inso' command",
            **result
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
