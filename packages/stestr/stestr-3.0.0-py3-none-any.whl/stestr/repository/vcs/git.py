# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Interact with git repos."""

import subprocess

def is_repo():
    cmd = ['git', 'rev-parse', '--is-inside-work-tree']
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    proc.communicate()
    if proc.returncode > 0:
        return False
    return True

def get_revision():
    cmd = ['git', 'rev-list', '-1', 'HEAD']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    sha1, _ = proc.communicate()
    return sha1.decode('utf8')
