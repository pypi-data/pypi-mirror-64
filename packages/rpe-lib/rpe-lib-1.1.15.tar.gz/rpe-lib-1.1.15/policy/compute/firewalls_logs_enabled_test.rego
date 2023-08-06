# Copyright 2019 The resource-policy-evaluation-library Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


package gcp.compute.firewalls.policy.logs_enabled

test_logs_good_enabled {
  valid with input as {"logConfig": {"enable": true}}
}

test_logs_good_disabled {
  valid with input as {"logConfig": {"enable": true}, "disabled": "true"}
}

test_logs_bad_enabled {
  not valid with input as {"logConfig": {"enable": false}}
}

test_logs_bad_disabled {
  valid with input as {"logConfig": {"enable": false}, "disabled": "true"}
}
