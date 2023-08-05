# Copyright (c) 2019-2020 SAP SE or an SAP affiliate company. All rights reserved. This file is
# licensed under the Apache Software License, v. 2 except as noted otherwise in the LICENSE file
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import ci.util
import product.model


def current_product_descriptor():
    component_descriptor = os.path.join(
        ci.util.check_env('COMPONENT_DESCRIPTOR_DIR'),
        'component_descriptor',
    )
    return product.model.ComponentDescriptor.from_dict(
        ci.util.parse_yaml_file(component_descriptor),
    )
