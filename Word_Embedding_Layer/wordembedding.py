#Pre Req, in linux type these commands in console 
# wget http://nlp.stanford.edu/data/glove.6B.zip
# unzip glove.6B.zip

import numpy as np
import tensorflow as tf

embeddings_index = {}
with open('glove.6B.100d.txt') as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, "f", sep=" ")
        embeddings_index[word] = coefs
     
fixed_embedding_matrix = np.zeros((vocab_size, 100))
for i, word in enumerate(vocabulary):
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # Words not found in embedding index will be all-zeros.
        fixed_embedding_matrix[i] = embedding_vector
        
fixed_embedding = tf.keras.layers.Embedding(
    self.nli_voba_size,
    100,
    embeddings_initializer=tf.keras.initializers.Constant(fixed_embedding_matrix),
    trainable=False,
    mask_zero=True)