import tensorflow as tf
# Simple hello world using TensorFlow

# Create a Constant op
# The op is added as a node to the default graph.
#
# The value returned by the constructor represents the output
# of the Constant op.

data = tf.zeros([3, 8, 128])

g1 = tf.gather(data, axis=0, indices=[0, 2])
print(g1.shape)

g2 = tf.gather(data, axis=1, indices=[0, 1, 2, 3])
print(g2.shape)
