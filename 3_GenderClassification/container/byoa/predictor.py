# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import json
import pickle
from io import StringIO
import sys
import signal
import traceback

import numpy as np

# TODO: Import necessary libraries

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ScoringService(object):
    model_type = None           # Where we keep the model type, qualified by hyperparameters used during training
    model = None                # Where we keep the model when it's loaded
    graph = None
    indices = None              # Where we keep the indices of Alphabet when it's loaded
    
   # TODO : Optional - Any other artefacts necessary to format data (if saved after training completed)

    @classmethod
    def get_model(cls):
        if cls.model == None:
            #TODO: Get the model object for this instance, loading it if it's not already loaded

        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        
        #TODO: Get model object for this instance

        if mod == None:
            print("Model not loaded.")
        else:

            #TODO: Pass the input data to the model, and return prediction response

        return result

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    #Determine if the container is working and healthy.
    # Declare it healthy if we can load the model successfully.
    health = ScoringService.get_model() is not None and ScoringService.get_indices() is not None
    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    #Do an inference on a single batch of data
    data = None

    # Convert from CSV to pandas
    if flask.request.content_type == 'text/csv':
        data = flask.request.data.decode('utf-8')
    else:
        return flask.Response(response='This predictor only supports CSV data', status=415, mimetype='text/plain')

    print('Invoked with {} records'.format(data.count(",")+1))

    # Do the prediction
    predictions = ScoringService.predict(data)

    result = ""
    for prediction in predictions:
        result = result + prediction

    return flask.Response(response=result, status=200, mimetype='text/csv')
