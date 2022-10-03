from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r"""
options:
  binary_path:
    description:
    - The path of a 'inso' CLI to use. 
    version_added: "1.2.0"
    default: "inso"
    type: path
  config:
    description:
    - Path to 'inso' configuration file.
    version_added: "1.2.0"
    type: path
  src:
    description:
    - Sets the 'inso' app data source < file | dir >
    version_added: "1.2.0"
    type: path
  working_dir:
    description:
    - Sets the 'inso' working directory
    version_added: "1.2.0"
    type: path

requirements:
- "inso (https://docs.insomnia.rest/inso-cli/install)"
    """