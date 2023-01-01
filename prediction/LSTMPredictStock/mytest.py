import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import matplotlib as mpl
import numpy as np
import sklearn
import pandas as pd
import tensorflow as tf

b = tf.fill([2, 2], 2.)
a = tf.ones([2, 2])

print(a+b)


