# Copyright (c) 2017 Huawei Technologies Co., Ltd.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_policy import policy

from karbor.policies import base


CREATE_POLICY = 'copy:create'

copies_policies = [
    policy.DocumentedRuleDefault(
        name=CREATE_POLICY,
        check_str=base.RULE_ADMIN_OR_OWNER,
        description='Create a copy.',
        operations=[
            {
                'method': 'POST',
                'path': '/{project_id}/providers/{provider_id}/'
                        'checkpoints/action'
            }
        ]),
]


def list_rules():
    return copies_policies
