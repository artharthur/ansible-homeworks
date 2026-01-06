#!/usr/bin/python

# Copyright: (c) 2025, Arthur
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Creates a text file with specified content

version_added: "1.0.0"

description:
    - This module creates a text file on the remote host.
    - The file path and content are specified as parameters.
    - Module is idempotent - it only changes the file if content differs.

options:
    path:
        description: Path to the file to be created.
        required: true
        type: str
    content:
        description: Content to write to the file.
        required: true
        type: str

author:
    - Arthur (@artharthur)
'''

EXAMPLES = r'''
# Create a simple text file
- name: Create test file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/test.txt
    content: "Hello, Netology!"

# Create a config file
- name: Create config
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /etc/myapp/config.txt
    content: |
      setting1=value1
      setting2=value2
'''

RETURN = r'''
path:
    description: Path to the created file.
    type: str
    returned: always
    sample: '/tmp/test.txt'
content:
    description: Content written to the file.
    type: str
    returned: always
    sample: 'Hello, Netology!'
changed:
    description: Whether the file was changed.
    type: bool
    returned: always
    sample: true
'''

import os
import hashlib
from ansible.module_utils.basic import AnsibleModule


def get_file_hash(path):
    """Calculate MD5 hash of file content."""
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return hashlib.md5(f.read().encode()).hexdigest()


def get_content_hash(content):
    """Calculate MD5 hash of string content."""
    return hashlib.md5(content.encode()).hexdigest()


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    # Check if file exists and compare content
    existing_hash = get_file_hash(path)
    new_hash = get_content_hash(content)

    if existing_hash == new_hash:
        # File exists with same content - no changes needed
        result['changed'] = False
        module.exit_json(**result)

    # File doesn't exist or content differs - need to change
    result['changed'] = True

    if module.check_mode:
        module.exit_json(**result)

    # Create directory if it doesn't exist
    dir_path = os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e:
            module.fail_json(msg=f'Failed to create directory {dir_path}: {e}', **result)

    # Write content to file
    try:
        with open(path, 'w') as f:
            f.write(content)
    except IOError as e:
        module.fail_json(msg=f'Failed to write file {path}: {e}', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
