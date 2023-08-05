# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
"""Cloud Bigtable Client for TensorFlow.

This contrib package allows TensorFlow to interface directly with Cloud Bigtable
for high-speed data loading.

@@BigtableClient
@@BigtableTable

"""


from tensorflow.python.util.all_util import remove_undocumented
from tensorflow_io.bigtable.python.ops.bigtable_api import BigtableClient
from tensorflow_io.bigtable.python.ops.bigtable_api import BigtableTable

_allowed_symbols = [
    "BigtableClient",
    "BigtableTable",
]

remove_undocumented(__name__, allowed_exception_list=_allowed_symbols)
