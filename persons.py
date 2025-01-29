from flask import Flask
import csv
import json

app = Flask(__name__)

with app.app_context():
	with open('persons.csv', 'r') as file:
		csv_reader = csv.DictReader(file)
		data = []
		for row in csv_reader:
			# validate row information
			data.append(row)
		persons_list = json.dumps(data, indent=4)

@app.route("/persons")
def persons():
	return json.dumps(data[0:10], indent=4)
