#!usr/bin/env/python
"""
Author: Shashi
Description: Launch tensorboard from stored model
"""
import tensorflow as tf
from tensorboard import main as tb
import os

def launch_tensorboard(path):
    """Launches tensorboard on localhost port 6006"""
    path = path +'/'+ os.listdir(path)[0]
    print("Loading model from '{}'".format(path))
    tf.flags.FLAGS.logdir = path
    tb.main()
    
if __name__ == '__main__':
    model_directory = '../tensorflow/logdir'
    launch_tensorboard(model_directory)
