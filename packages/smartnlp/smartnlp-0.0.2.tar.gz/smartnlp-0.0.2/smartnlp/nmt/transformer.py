# coding=utf-8
# created by msgi on 2020/3/18 1:05 上午

import tensorflow as tf
from smartnlp.layers.encoder import Encoder
from smartnlp.layers.decoder import Decoder


class Transformer(tf.keras.Model):
    def __init__(self, n_layers, d_model, n_heads, diff,
                 input_vocab_size, target_vocab_size,
                 max_seq_len, drop_rate=0.1):
        super(Transformer, self).__init__()

        self.encoder = Encoder(n_layers, d_model, n_heads, diff,
                               input_vocab_size, max_seq_len, drop_rate)

        self.decoder = Decoder(n_layers, d_model, n_heads, diff,
                               target_vocab_size, max_seq_len, drop_rate)

        self.final_layer = tf.keras.layers.Dense(target_vocab_size)

    def call(self, inputs, targets, training, encode_padding_mask,
             look_ahead_mask, decode_padding_mask):
        encode_out = self.encoder(inputs, training, encode_padding_mask)
        print(encode_out.shape)
        decode_out, att_weights = self.decoder(targets, encode_out, training,
                                               look_ahead_mask, decode_padding_mask)
        print(decode_out.shape)
        final_out = self.final_layer(decode_out)

        return final_out, att_weights
