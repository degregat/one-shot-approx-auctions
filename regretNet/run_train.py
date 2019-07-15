from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import itertools
import numpy as np
import pandas as pd
import tensorflow as tf

from nets import *
from cfgs import *
from data import *
from clip_ops.clip_ops import *
from trainer import *

print("Setting: %s"%(sys.argv[1]))
setting = sys.argv[1]

if setting == "additive_10x1_uniform_dp":
    cfg = additive_10x1_uniform_dp_config.cfg
    Net = additive_net.Net
    Generator = uniform_01_generator.Generator
    clip_op_lambda = (lambda x: clip_op_01(x))
    Trainer = trainer.Trainer
    
else:
    print("None selected")
    sys.exit(0)

def training(noise, clip):
        net = Net(cfg)
        generator = [Generator(cfg, 'train'), Generator(cfg, 'val')]
        m = Trainer(cfg, "train", net, clip_op_lambda, noise, clip)
        m.train(generator)
        tf.reset_default_graph()
    
def get_exp_dir(noise, clip):
    if (noise, clip) != (None, None):
        return(os.path.join('experiments', setting + '_noise_' + str(noise) + '_clip_' + str(clip)))
    else:
        return(os.path.join('experiments', setting))

noise_vals = [0.001, 0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.1, 1.2, 1.5, 2, 3]
clip_vals = [1, 10, 50, 100, 500]

# Do one experiment without differential privacy
training(None,None)

# Do several rounds with varying noise and clipping
for noise in noise_vals:
    for clip in clip_vals:
        training(noise,clip)
       
exp_dirs = [get_exp_dir(None,None)] + [get_exp_dir(noise, clip) for (noise, clip) in itertools.product(noise_vals, clip_vals)]

data = [ pd.read_csv(os.path.join(exp_dir, 'data.csv')) for exp_dir in exp_dirs ]
all_data = pd.concat(data, ignore_index=True)

all_data.to_csv(os.path.join('experiments','all_data.csv'))
