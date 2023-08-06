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

"""
## Data scale introduction


"""

import os
import traceback
from absl import logging
from delta.data.datasets.base_dataset import BaseDataSet
from delta.data.datasets.utils import mock_data
from delta.utils.register import registers


@registers.dataset.register('mock_text_seq_label_data')
class MockTextSeqLabelData(BaseDataSet):
  """data class for mock seqlabel task."""

  def __init__(self, project_dir):
    super().__init__(project_dir)
    self.train_file = "train.txt"
    self.dev_file = "dev.txt"
    self.test_file = "test.txt"
    self.data_files = [self.train_file, self.dev_file, self.test_file]
    self.config_files = ['seq_label_mock.yml']
    self.download_files = []
    self.text_vocab = "text_vocab.txt"
    self.label_vocab = "label_vocab.txt"

    # samples with label
    self.samples = ["O O O O\ti feel good .",
               "O O B-ORG O O O O O O\tby stumps kent had reached 108 for three ."]
    self.text_vocab_list = ["<unk>\t0", "</s>\t1", "i\t2", "feel\t3", "good\t4",
                            ".\t5", "by\t6", "stumps\t7", "kent\t8", "had\t9",
                            "reached\t10", "108\t11", "for\t12", "three\t13"]
    self.label_vocab_list = ["O\t0", "B-PER\t1", "I-PER\t2", "B-LOC\t3", "I-LOC\t4",
                        "B-ORG\t5", "I-ORG\t6", "B-MISC\t7", "I-MISC\t8"]


  def download(self) -> bool:
    return True


  def after_download(self) -> bool:
    try:
      train_file_path = os.path.join(self.data_dir, self.train_file)
      dev_file_path = os.path.join(self.data_dir, self.dev_file)
      test_file_path = os.path.join(self.data_dir, self.test_file)

      text_vocab_file = os.path.join(self.data_dir, self.text_vocab)
      label_vocab_file = os.path.join(self.data_dir, self.label_vocab)

      mock_data(self.samples, train_file_path, dev_file_path, test_file_path,
                text_vocab_file, self.text_vocab_list, label_vocab_file, self.label_vocab_list)

    except Exception as e:
      logging.warning(traceback.format_exc())
      return False
    return True

