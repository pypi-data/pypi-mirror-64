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
"""Common layers."""

import delta.compat as tf

from delta.data.feat import speech_ops
from delta.layers.common_layers import linear
#pylint: disable=invalid-name


def splice_layer(x, name, context):
  '''
  Splice a tensor along the last dimension with context.
  e.g.:
  t = [[[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]]
  splice_tensor(t, [0, 1]) =
      [[[1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9],
        [7, 8, 9, 7, 8, 9]]]

  Args:
    tensor: a tf.Tensor with shape (B, T, D) a.k.a. (N, H, W)
    context: a list of context offsets

  Returns:
    spliced tensor with shape (..., D * len(context))
  '''
  with tf.variable_scope(name):
    input_shape = tf.shape(x)
    B, T = input_shape[0], input_shape[1]
    context_len = len(context)
    array = tf.TensorArray(x.dtype, size=context_len)
    for idx, offset in enumerate(context):
      begin = offset
      end = T + offset
      if begin < 0:
        begin = 0
        sliced = x[:, begin:end, :]
        tiled = tf.tile(x[:, 0:1, :], [1, abs(offset), 1])
        final = tf.concat((tiled, sliced), axis=1)
      else:
        end = T
        sliced = x[:, begin:end, :]
        tiled = tf.tile(x[:, -1:, :], [1, abs(offset), 1])
        final = tf.concat((sliced, tiled), axis=1)
      array = array.write(idx, final)
    spliced = array.stack()
    spliced = tf.transpose(spliced, (1, 2, 0, 3))
    spliced = tf.reshape(spliced, (B, T, -1))
  return spliced


#pylint: disable=too-many-arguments
def tdnn(x,
         name,
         in_dim,
         context,
         out_dim,
         has_bias=True,
         method='splice_layer'):
  '''
  TDNN implementation.

  Args:
    context:
      a int of left and right context, or
      a list of context indexes, e.g. (-2, 0, 2).
    method:
      splice_layer: use column-first patch-based copy.
      splice_op: use row-first while_loop copy.
      conv1d: use conv1d as TDNN equivalence.
  '''
  if hasattr(context, '__iter__'):
    context_size = len(context)
    if method in ('splice_op', 'conv1d'):
      msg = 'Method splice_op and conv1d does not support context list.'
      raise ValueError(msg)
    context_list = context
  else:
    context_size = context * 2 + 1
    context_list = range(-context, context + 1)
  with tf.variable_scope(name):
    if method == 'splice_layer':
      x = splice_layer(x, 'splice', context_list)
      x = linear(
          x, 'linear', [in_dim * context_size, out_dim], has_bias=has_bias)
    elif method == 'splice_op':
      x = speech_ops.splice(x, context, context)
      x = linear(
          x, 'linear', [in_dim * context_size, out_dim], has_bias=has_bias)
    elif method == 'conv1d':
      kernel = tf.get_variable(
          name='DW',
          shape=[context, in_dim, out_dim],
          dtype=tf.float32,
          initializer=tf.glorot_uniform_initializer())
      x = tf.nn.conv1d(x, kernel, stride=1, padding='SAME')
      if has_bias:
        b = tf.get_variable(
            name='bias',
            shape=[out_dim],
            dtype=tf.float32,
            initializer=tf.constant_initializer(0.0))
        x = tf.nn.bias_add(x, b)
    else:
      raise ValueError('Unsupported method: %s.' % (method))
    return x
