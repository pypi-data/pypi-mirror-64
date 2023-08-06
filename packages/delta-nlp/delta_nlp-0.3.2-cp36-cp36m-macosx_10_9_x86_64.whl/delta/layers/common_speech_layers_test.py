# Copyright (C) 2017 Beijing Didi Infinity Technology and Development Co.,Ltd.
# All rights reserved.
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
"""Common layers test."""

import delta.compat as tf
from absl import logging

import common_speech_layers as cl


class LossUtilTest(tf.test.TestCase):
  ''' common layer unittest '''

  def test_splice_layer(self):
    '''test splice layer'''
    inputs = tf.reshape(tf.range(15), shape=[1, 5, 3])
    context = [0, 1]
    output = cl.splice_layer(inputs, 'splice', context)
    output_true = tf.constant([[[0, 1, 2, 3, 4, 5], [3, 4, 5, 6, 7, 8],
                                [6, 7, 8, 9, 10, 11], [9, 10, 11, 12, 13, 14],
                                [12, 13, 14, 12, 13, 14]]])
    self.assertAllEqual(output, output_true)

    context = [-1, 0, 1]
    output = cl.splice_layer(inputs, 'splice', context)
    output_true = tf.constant([[[0, 1, 2, 0, 1, 2, 3, 4, 5],
                                [0, 1, 2, 3, 4, 5, 6, 7, 8],
                                [3, 4, 5, 6, 7, 8, 9, 10, 11],
                                [6, 7, 8, 9, 10, 11, 12, 13, 14],
                                [9, 10, 11, 12, 13, 14, 12, 13, 14]]])
    self.assertAllEqual(output, output_true)

    context = [0, 1, 3]
    output = cl.splice_layer(inputs, 'splice', context)
    output_true = tf.constant([[[0, 1, 2, 3, 4, 5, 9, 10, 11],
                                [3, 4, 5, 6, 7, 8, 12, 13, 14],
                                [6, 7, 8, 9, 10, 11, 12, 13, 14],
                                [9, 10, 11, 12, 13, 14, 12, 13, 14],
                                [12, 13, 14, 12, 13, 14, 12, 13, 14]]])
    self.assertAllEqual(output, output_true)

    context = [1, 3]
    output = cl.splice_layer(inputs, 'splice', context)
    output_true = tf.constant([[[3, 4, 5, 9, 10, 11], [6, 7, 8, 12, 13, 14],
                                [9, 10, 11, 12, 13, 14],
                                [12, 13, 14, 12, 13, 14],
                                [12, 13, 14, 12, 13, 14]]])
    self.assertAllEqual(output, output_true)

    context = [1, 2, 3]
    output = cl.splice_layer(inputs, 'splice', context)
    output_true = tf.constant([[[3, 4, 5, 6, 7, 8, 9, 10, 11],
                                [6, 7, 8, 9, 10, 11, 12, 13, 14],
                                [9, 10, 11, 12, 13, 14, 12, 13, 14],
                                [12, 13, 14, 12, 13, 14, 12, 13, 14],
                                [12, 13, 14, 12, 13, 14, 12, 13, 14]]])
    self.assertAllEqual(output, output_true)

  def test_tdnn(self):
    '''test tdnn'''
    #A 3D Tensor [batch, in_width, in_channels]
    inputs = tf.random_uniform(shape=[2, 5, 3], dtype=tf.float32, maxval=1.0)
    in_dim = inputs.get_shape().as_list()[2]
    out_dim = 4
    context = [-2, -1, 0, 1, 2]
    output = cl.tdnn(
        inputs, 'test_tdnn0', in_dim, context, out_dim, method='splice_layer')
    out_shape = [2, 5, 4]
    self.assertAllEqual(tf.shape(output), out_shape)

    context = 2
    #output = cl.tdnn(inputs, 'test_tdnn1', in_dim, context, out_dim, method='splice_op')
    #self.assertAllEqual(tf.shape(output), out_shape)

    output = cl.tdnn(
        inputs, 'test_tdnn2', in_dim, context, out_dim, method='conv1d')
    self.assertAllEqual(tf.shape(output), out_shape)

if __name__ == '__main__':
  logging.set_verbosity(logging.INFO)
  tf.test.main()
