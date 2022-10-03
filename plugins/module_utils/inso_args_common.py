
from __future__ import absolute_import, division, print_function

from ansible.module_utils.six import string_types

__metaclass__ = type

# may not need func
def list_dict_str(value):
    if isinstance(value, (list, dict, string_types)):
        return value
    raise TypeError

COMMON_ARG_SPEC = {
    "binary_path": {"type": "path", "default": "inso"},
    "config": {"type": "path", "required": False},
    "working_dir": {"type": "path", "required": False},
    "src": {"type": "path", "required": False}
}
