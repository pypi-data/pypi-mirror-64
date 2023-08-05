# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
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
"""Additional layers that conform to Keras API."""

from tensorflow_addons.layers.gelu import GELU
from tensorflow_addons.layers.maxout import Maxout
from tensorflow_addons.layers.multihead_attention import MultiHeadAttention
from tensorflow_addons.layers.normalizations import GroupNormalization
from tensorflow_addons.layers.normalizations import InstanceNormalization
from tensorflow_addons.layers.optical_flow import CorrelationCost
from tensorflow_addons.layers.poincare import PoincareNormalize
from tensorflow_addons.layers.polynomial import PolynomialCrossing
from tensorflow_addons.layers.sparsemax import Sparsemax
from tensorflow_addons.layers.tlu import TLU
from tensorflow_addons.layers.wrappers import WeightNormalization
