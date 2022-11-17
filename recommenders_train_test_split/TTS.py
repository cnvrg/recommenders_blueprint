# Copyright (c) 2022 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT

import argparse
import pandas as pd
import psutil
import time
from cnvrg import Experiment
import os

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
tic=time.time()
parser = argparse.ArgumentParser(description="""Preprocessor""")
parser.add_argument('-f','--filename', action='store', dest='filename', default='/data/movies_rec_sys/ratings.csv', required=True, help="""string. csv topics data file""")
parser.add_argument('--project_dir', action='store', dest='project_dir',
                        help="""--- For inner use of cnvrg.io ---""")
parser.add_argument('--output_dir', action='store', dest='output_dir',
                        help="""--- For inner use of cnvrg.io ---""")
args = parser.parse_args()
#FILENAME = "/data/"+args.dataset_name+"/"+args.filename
FILENAME = args.filename
ratings = pd.read_csv(FILENAME)
#ratings = ratings.drop(['Unnamed: 0'], axis=1)
#ratings['user_id'] = ratings['user_id'].astype(int)
#ratings['item_id'] = ratings['item_id'].astype(int)
#print(len(ratings['user_id'].unique()))

#train_whole = pd.DataFrame(columns=['user_id','item_id','rating'])
#test_whole = pd.DataFrame(columns=['user_id','item_id','rating'])
train_whole = ratings.groupby('user_id', group_keys=False).apply(lambda x: x.sample(frac=0.75,random_state=1).drop_duplicates())

test_whole = ratings.merge(ratings.groupby('user_id', group_keys=False).apply(lambda x: x.sample(frac=0.75,random_state=1).drop_duplicates()), on =['user_id','item_id','rating'], how='left',indicator=True).query('`_merge` == "left_only"').drop('_merge', axis=1)

train_name = "train_whole.csv"
test_name = "test_whole.csv"

print('test dimensions are' + str(test_whole.shape[0]) + 'and train dimensions are ' + str(train_whole.shape[0]))
train_whole.to_csv(cnvrg_workdir + "/{}".format(train_name), index=False)
test_whole.to_csv(cnvrg_workdir + "/{}".format(test_name), index=False)

print('RAM GB used:', psutil.virtual_memory()[3]/(1024 * 1024 * 1024))
toc=time.time()
print("time taken:",toc-tic)
e = Experiment()
e.log_param("tts_ram", psutil.virtual_memory()[3]/(1024 * 1024 * 1024))
e.log_param("tts_time", toc-tic)