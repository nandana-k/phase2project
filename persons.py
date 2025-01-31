from flask import Flask, abort
import csv
import json

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

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

@app.route("/persons/<id>")
def persons_id(id):
	for person in data:
		person_id = person["Id"]
		if person_id == id:
			return json.dumps(person, indent=4)
	return abort(404, description="Person not found")
