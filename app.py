from flask import Flask
from flask import request

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA # Import PCA for Feature Reduction
import xgboost as xgb # Import XGboost Classifier

import pickle

app = Flask(__name__)


@app.route("/api/v1/divorce/predict", methods=['POST'])
def hello_world():
	content = request.json
	print(content)

	model = pickle.load(open('divorce_xgbc', 'rb'))
	print("Model: {}", model)
	ll = content
	ll3 = [ll]
	print("ll3: {}", ll3)
	scaler = pickle.load(open('divorce_scaler', 'rb'))
	#ll2 = scaler.transform(ll3)
	ll2 = ll3
	print("ll2: {}", ll2)
	ll2 = pd.DataFrame(ll2)
	ll2 = reduce_features(ll2)
	prediction = model.predict(ll2)
	print("prediction: {}", prediction)
	prediction_result = int(prediction[0])
	return {
		"Divorce? ": prediction_result
	}

# Dimensionality reduction (reducing any less relavent columns)
def reduce_features(features):
	n_components = 8
	# n_components is no of dimensions to retain
	print("features_count: {}", features.shape[1])
	pca = pickle.load(open('divorce_pca', 'rb')) # Principal Component Analysis technique
	features_reduced = pd.DataFrame(pca.transform(features), index=features.index,
									columns=["PC" + str(i) for i in range(1, n_components + 1)])

	return features_reduced



if __name__ == "__main__":
	app.run(debug=True)
