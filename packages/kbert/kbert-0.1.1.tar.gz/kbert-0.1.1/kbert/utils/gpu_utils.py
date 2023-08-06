import tensorflow as tf
import os


def config_gpu():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)


def test_gpu():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    if tf.test.gpu_device_name():
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
        print('Your tensorflow-gpu is available')
    else:
        print('Your tensorflow-gpu is not available')
        print("Please install GPU version of TF")

if __name__ == '__main__':
    config_gpu()
    # test_gpu()
