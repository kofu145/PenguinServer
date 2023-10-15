from flask import Flask, jsonify, request, send_file, send_from_directory
from werkzeug.utils import secure_filename
import json
import uuid
import os
import copy
from tesseract_analyzer import TextAnalyzer
from invalidusage import InvalidUsage
import shutil

app = Flask('app')
local_url = "http://traptrixden.ddns.net:5698/"

textAnalyzer = TextAnalyzer()

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


@app.route("/", methods=["GET", "POST"])
def hello_world():
	return jsonify({"message": "hello world!"})

@app.route("/image", methods=["POST"])
def process_image():
	# byte file
	print(request.files)
	print(request.form)
	"""
	file = request.files['image'].read()
	npimg = np.fromstring(file, np.uint8)
	img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
	if os.path.exists("./results"):
		shutil.rmtree("./results")
	trashAnalyzer.process_image(img)"""
	f = request.files['image']
	filename = "analyze" + os.path.splitext(f.filename)[1]
	print(secure_filename(filename))
	f.save(secure_filename(filename))
	msg = textAnalyzer.analyze_text(filename)
	print(msg)
	print(filename)
	return jsonify({"message": "{}".format(msg)}), 200

app.run(host='0.0.0.0', port=5698) #ssl_context="adhoc")