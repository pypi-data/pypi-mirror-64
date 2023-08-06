import tensorflow as tf


class BertSquadLogitsLayer(tf.keras.layers.Layer):
    """Returns a layer that computes custom logits for BERT squad model."""

    def __init__(self, initializer=None, float_type=tf.float32, **kwargs):
        super(BertSquadLogitsLayer, self).__init__(**kwargs)
        self.initializer = initializer
        self.float_type = float_type

    def build(self, unused_input_shapes):
        """Implements build() for the layer."""
        self.final_dense = tf.keras.layers.Dense(
            units=2, kernel_initializer=self.initializer, name='final_dense')
        super(BertSquadLogitsLayer, self).build(unused_input_shapes)

    def call(self, inputs):
        """Implements call() for the layer."""
        sequence_output = inputs

        input_shape = sequence_output.shape.as_list()
        sequence_length = input_shape[1]
        num_hidden_units = input_shape[2]

        final_hidden_input = tf.keras.backend.reshape(sequence_output,
                                                      [-1, num_hidden_units])
        logits = self.final_dense(final_hidden_input)
        logits = tf.keras.backend.reshape(logits, [-1, sequence_length, 2])
        logits = tf.transpose(logits, [2, 0, 1])
        unstacked_logits = tf.unstack(logits, axis=0)
        if self.float_type == tf.float16:
            unstacked_logits = tf.cast(unstacked_logits, tf.float32)
        return unstacked_logits[0], unstacked_logits[1]


def squad_model(bert_config, max_seq_length, float_type, initializer=None):
    """Returns BERT Squad model along with core BERT model to import weights.
  Args:
    bert_config: BertConfig, the config defines the core Bert model.
    max_seq_length: integer, the maximum input sequence length.
    float_type: tf.dtype, tf.float32 or tf.bfloat16.
    initializer: Initializer for weights in BertSquadLogitsLayer.
  Returns:
    Two tensors, start logits and end logits, [batch x sequence length].
  """
    unique_ids = tf.keras.layers.Input(
        shape=(1,), dtype=tf.int32, name='unique_ids')
    input_word_ids = tf.keras.layers.Input(
        shape=(max_seq_length,), dtype=tf.int32, name='input_ids')
    input_mask = tf.keras.layers.Input(
        shape=(max_seq_length,), dtype=tf.int32, name='input_mask')
    input_type_ids = tf.keras.layers.Input(
        shape=(max_seq_length,), dtype=tf.int32, name='segment_ids')

    core_model = modeling.get_bert_model(
        input_word_ids,
        input_mask,
        input_type_ids,
        config=bert_config,
        name='bert_model',
        float_type=float_type)

    # `BertSquadModel` only uses the sequnce_output which
    # has dimensionality (batch_size, sequence_length, num_hidden).
    sequence_output = core_model.outputs[1]

    if initializer is None:
        initializer = tf.keras.initializers.TruncatedNormal(
            stddev=bert_config.initializer_range)
    squad_logits_layer = BertSquadLogitsLayer(
        initializer=initializer, float_type=float_type, name='squad_logits')
    start_logits, end_logits = squad_logits_layer(sequence_output)

    squad = tf.keras.Model(
        inputs={
            'unique_ids': unique_ids,
            'input_ids': input_word_ids,
            'input_mask': input_mask,
            'segment_ids': input_type_ids,
        },
        outputs=[unique_ids, start_logits, end_logits],
        name='squad_model')
    return squad, core_model

