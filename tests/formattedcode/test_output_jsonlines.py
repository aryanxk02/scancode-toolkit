#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from collections import OrderedDict
import io
import json
import os

from commoncode.testcase import FileDrivenTesting
from scancode.cli_test_utils import check_jsonlines_scan
from scancode.cli_test_utils import run_scan_click

test_env = FileDrivenTesting()
test_env.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')


def test_jsonlines():
    test_dir = test_env.get_test_loc('json/simple')
    result_file = test_env.get_temp_file('jsonline')
    run_scan_click(['-i', test_dir, '--json-lines', result_file])
    expected = test_env.get_test_loc('json/simple-expected.jsonlines')
    check_jsonlines_scan(test_env.get_test_loc(expected), result_file, regen=False)


def test_jsonlines_with_timing():
    test_dir = test_env.get_test_loc('json/simple')
    result_file = test_env.get_temp_file('jsonline')
    run_scan_click(['-i', '--timing', test_dir, '--json-lines', result_file])

    with io.open(result_file, encoding='utf-8') as res:
        file_results = [json.loads(line, object_pairs_hook=OrderedDict) for line in res]

    first_line = True
    for res in file_results:
        if first_line:
            # skip header
            first_line = False
            continue
        scan_timings = res['files'][0]['scan_timings']

        if not res['files'][0]['type'] == 'file':
            # should be an empty dict for dirs
            assert not scan_timings
            continue

        assert scan_timings

        for scanner, timing in scan_timings.items():
            assert scanner in ('info',)
            assert timing
