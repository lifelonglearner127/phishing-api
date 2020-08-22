from flask import Flask, request,flash, jsonify, render_template,redirect, url_for,Blueprint
from flask_cors import CORS
import warnings
import json
import os
import time
import json
from flask_swagger_ui import get_swaggerui_blueprint
warnings.filterwarnings("ignore")
import logging
from tensorflow import keras
import numpy as np
from extract import extract_features
from extract_v2 import extract_features as extract_features_v2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)
logger_handler = logging.FileHandler('logs.log')
logger.addHandler(logger_handler)

REQUEST_API = Blueprint('endpoint', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


model = keras.models.load_model("url_phishing.h5")


def predict(data):
    return list(list(np.round(model.predict(np.array([np.array([data]).reshape((91, 1))])))[0]))


@REQUEST_API.route("/url", methods=['POST'])
def url():
    data = request.get_json()
    url = data['url']
    features = extract_features(url)
    prediction = predict(features)
    print(f"{url}: {prediction}")
    return jsonify(
        {
            'url': f'{url}',
            'prediction': f'{prediction}'
        }
    )


@REQUEST_API.route("/api_readiness", methods=['GET'])
def api_readiness():
    return jsonify({'status': 'ready'})
