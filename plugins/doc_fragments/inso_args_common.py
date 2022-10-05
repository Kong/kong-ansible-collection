# Copyright: Kong Inc.
# SPDX-License-Identifier: Apache-2.0

class ModuleDocFragment(object):

    DOCUMENTATION = r"""
options:
  binary_path:
    description:
    - The path of a 'inso' CLI to use. 
    type: path
  config:
    description:
    - Path to 'inso' configuration file.
    type: path
  src:
    description:
    - Sets the 'inso' app data source < file | dir >
    type: path
  working_dir:
    description:
    - Sets the 'inso' working directory
    type: path

requirements:
- "inso (https://docs.insomnia.rest/inso-cli/install)"
    """