#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

# common inso command options
from ansible_collections.kong.kong.plugins.module_utils.inso_args_common import (
    COMMON_ARG_SPEC,
    build_base_cmd
)

import copy

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
        version_added: "1.2.0"
        type: str
        choices: [ yaml, json ]
        default: yaml
        required: false
    identifier:
        description: 
        - A specification name, or id, or a file path.
        version_added: "1.2.0"
        type: str
        required: true
    output:
        description:
        - Save the generated config to a file
        version_added: "1.2.0"
        type: path
        required: false
    tags:
        description:
        - List of tags to apply to each entity
        version_added: "1.2.0"
        type: list
        required: false
    type:
        description:
        - Type of configuration to generate
        version_added: "1.2.0"
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

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

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


def build_cfg_gen_cmd(module):
    cmd = []

    # --format
    if module.params["format"]:
        cmd.append("--format")
        cmd.append(module.params["format"])
    
    # --output
    if module.params["output"]:
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

    # identifier needs to be last
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

    if module.check_mode:
        module.exit_json(**result)

    cmd = build_base_cmd(module) + build_cfg_gen_cmd(module)

    # inject sub-commands
    cmd.insert(1, "generate")
    cmd.insert(2, "config")

    result["cmd"] = cmd

    result["rc"], result["stdout"], result["stderr"] = module.run_command(
        args=cmd,
        use_unsafe_shell=False
    )

    if result["rc"] == 0:
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
