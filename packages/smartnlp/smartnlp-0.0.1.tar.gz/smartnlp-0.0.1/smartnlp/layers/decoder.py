# coding=utf-8
# created by msgi on 2020/3/18 12:55 上午

import tensorflow as tf
from smartnlp.layers.multi_head_attention import MultiHeadAttention
from smartnlp.layers.encoder import point_wise_feed_forward_network
from smartnlp.layers.layer_norm import LayerNormalization
from smartnlp.layers.position_encoding import *


class DecoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, drop_rate=0.1):
        super(DecoderLayer, self).__init__()

        self.mha1 = MultiHeadAttention(d_model, num_heads)
        self.mha2 = MultiHeadAttention(d_model, num_heads)

        self.ffn = point_wise_feed_forward_network(d_model, dff)

        self.layer_norm1 = LayerNormalization(epsilon=1e-6)
        self.layer_norm2 = LayerNormalization(epsilon=1e-6)
        self.layer_norm3 = LayerNormalization(epsilon=1e-6)

        self.dropout1 = tf.keras.layers.Dropout(drop_rate)
        self.dropout2 = tf.keras.layers.Dropout(drop_rate)
        self.dropout3 = tf.keras.layers.Dropout(drop_rate)

    def call(self, inputs, encode_out, training, look_ahead_mask, padding_mask):
        # masked multi-head attention
        att1, att_weight1 = self.mha1(inputs, inputs, inputs, look_ahead_mask)
        att1 = self.dropout1(att1, training=training)
        out1 = self.layer_norm1(inputs + att1)
        # multi-head attention
        att2, att_weight2 = self.mha2(encode_out, encode_out, inputs, padding_mask)
        att2 = self.dropout2(att2, training=training)
        out2 = self.layer_norm2(out1 + att2)

        ffn_out = self.ffn(out2)
        ffn_out = self.dropout3(ffn_out, training=training)
        out3 = self.layer_norm3(out2 + ffn_out)

        return out3, att_weight1, att_weight2


# import pdb
# pdb.set_trace()
class Decoder(tf.keras.layers.Layer):
    def __init__(self, n_layers, d_model, n_heads, ddf,
                 target_vocab_size, max_seq_len, drop_rate=0.1):
        super(Decoder, self).__init__()

        self.d_model = d_model
        self.n_layers = n_layers

        self.embedding = tf.keras.layers.Embedding(target_vocab_size, d_model)
        self.pos_embedding = positional_encoding(max_seq_len, d_model)

        self.decoder_layers = [DecoderLayer(d_model, n_heads, ddf, drop_rate)
                               for _ in range(n_layers)]

        self.dropout = tf.keras.layers.Dropout(drop_rate)

    def call(self, inputs, encoder_out, training, look_ahead_mark, padding_mark):
        seq_len = tf.shape(inputs)[1]
        attention_weights = {}
        h = self.embedding(inputs)
        h *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        h += self.pos_embedding[:, :seq_len, :]

        h = self.dropout(h, training=training)
        # print('--------------------\n',h, h.shape)
        # 叠加解码层
        for i in range(self.n_layers):
            h, att_w1, att_w2 = self.decoder_layers[i](h, encoder_out,
                                                       training, look_ahead_mark,
                                                       padding_mark)
            attention_weights['decoder_layer{}_att_w1'.format(i + 1)] = att_w1
            attention_weights['decoder_layer{}_att_w2'.format(i + 1)] = att_w2

        return h, attention_weights
