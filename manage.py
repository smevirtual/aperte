#!/usr/bin/env python
# Copyright 2018 SME Virtual Network Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Django management entry point.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

    try:
        from configurations.management import execute_from_command_line
    except ImportError:
        try:
            import django # pylint: disable=W0611
        except ImportError:
            raise ImportError(
                'Django cannot be imported.'
            )

        raise

    execute_from_command_line(sys.argv)
