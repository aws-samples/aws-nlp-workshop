import numpy as np
import pandas as pd
from numpy import genfromtxt
import os
import tensorflow as tf
from tensorflow.python.estimator.export.export import build_raw_serving_input_receiver_fn
from tensorflow.python.estimator.export.export_output import PredictOutput
import json

INPUT_TENSOR_NAME = "inputs"
SIGNATURE_NAME = "serving_default"

def model_fn(features, labels, mode, params):
    """Model function for Estimator.
     # Logic to do the following:
     # 1. Configure the model via Keras functional api
     # 2. Define the loss function for training/evaluation using Tensorflow.
     # 3. Define the training operation/optimizer using Tensorflow operation/optimizer.
     # 4. Generate predictions as Tensorflow tensors.
     # 5. Generate necessary evaluation metrics.
     # 6. Return predictions/loss/train_op/eval_metric_ops in EstimatorSpec object"""

    # 1. Configure the model via Keras functional api

    first_hidden_layer = tf.keras.layers.LSTM(512, activation='relu', return_sequences=True,input_shape=(15,26), name='first-layer')(features[INPUT_TENSOR_NAME])
    #second_hidden_layer = tf.keras.layers.LSTM(512,activation='relu',return_sequences=True,)(first_hidden_layer)
    third_hidden_layer = tf.keras.layers.LSTM(512,activation='relu')(first_hidden_layer)
    output_layer = tf.keras.layers.Dense(1, activation='sigmoid')(third_hidden_layer)

    predictions = tf.reshape(output_layer, [-1])

    # Provide an estimator spec for `ModeKeys.PREDICT`.
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions={"Gender": predictions},
            export_outputs={SIGNATURE_NAME: PredictOutput({"Gender": predictions})})

    pred_2d = output_layer

    # 2. Define the loss function for training/evaluation using Tensorflow.
    loss = tf.losses.log_loss(labels, pred_2d)

    # 3. Define the training operation/optimizer using Tensorflow operation/optimizer.
    train_op = tf.contrib.layers.optimize_loss(
        loss=loss,
        global_step=tf.contrib.framework.get_global_step(),
        learning_rate=params["learning_rate"],
        optimizer="Adagrad")

    # 4. Generate predictions as Tensorflow tensors.
    predictions_dict = {"Gender": predictions}

    # 5. Generate necessary evaluation metrics.
    # Calculate root mean squared error as additional eval metric
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            tf.cast(labels, tf.float32), tf.cast(predictions,tf.float32))
    }

    # Provide an estimator spec for `ModeKeys.EVAL` and `ModeKeys.TRAIN` modes.
    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=loss,
        train_op=train_op,
        eval_metric_ops=eval_metric_ops)


def serving_input_fn(params):
    tensor = tf.placeholder(tf.float32, shape=[1, 15, 26])
    return build_raw_serving_input_receiver_fn({INPUT_TENSOR_NAME: tensor})()

def train_input_fn(training_dir, params):
    return _input_fn(training_dir, "train_names.csv")

def eval_input_fn(training_dir, params):
    return _input_fn(training_dir, "test_names.csv")

def _input_fn(training_dir, training_filename):
    filename = filename=os.path.join(training_dir, training_filename)
    df=pd.read_csv(filename, sep=',', names = ["Name", "Gender"])
    
    max_name_length = 15
    alphabet_size = 26
        
    #get list of names from the 'Name' column
    names = df['Name'].values
    
    train_count = df.shape[0]

    # get input X
    char_index = create_char_index()
    X = np.zeros((train_count, max_name_length, alphabet_size),dtype=np.float32)
    for i,name in enumerate(names):
        name = name.lower()
        for t, char in enumerate(name):
            X[i, t,char_index[char]] = 1

    # get list of genders <M,F> from the 'Gender' column
    Y = np.ones((train_count,1),dtype=np.float32)
    Y[df['Gender'] == 'M',0] = 0       
       
    return tf.estimator.inputs.numpy_input_fn(
        x={INPUT_TENSOR_NAME: X},
        y=Y,
        batch_size=64,
        num_epochs=None,
        shuffle=True)()

def input_fn(serialized_data, content_type):
    # assuming the input is in json
    obj = json.loads(serialized_data)
    name = obj['name']
    name = name.lower()
    char_index = create_char_index()
    data = np.zeros((1,15,26), dtype=np.float32)
    for t, char in enumerate(name):
        data[0,t,char_index[char]] = 1
    return tf.make_tensor_proto(values=np.asarray(data), shape=[1,15,26], dtype=tf.float32)
        
def create_char_index():
    return {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25}
