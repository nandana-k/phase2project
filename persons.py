from flask import Flask, abort
import csv
import json

app = Flask(__name__)

if __name__ == '__main__':
	app.run(port=8080)

with app.app_context():
	with open('persons.csv', 'r') as file:
		csv_reader = csv.DictReader(file)
		data = []
		ids = []
		for row in csv_reader:

			# Id Validation
			if row["Id"] == "":
				continue
			if row["Id"] in ids:
				continue
			ids.append(row["Id"])

			# First_Name and Last_Name Validation
			if not row["First_Name"].isalpha() or not row["Last_Name"].isalpha():
				continue
			firstNameFirstLetter = row["First_Name"][0].isupper()
			lastNameFirstLetter = row["Last_Name"][0].isupper()
			firstNameLowercase = row["First_Name"][1:len(row["First_Name"])].islower()
			lastNameLowercase = row["Last_Name"][1:len(row["Last_Name"])].islower()
			if  not firstNameFirstLetter or  not lastNameFirstLetter or not firstNameLowercase or not lastNameLowercase:
				continue

			# Email Validation
			email = row["Email"]
			specialChars = ['.', '-', '_', '@']
			validEmail = True
			if len(email) > 320 or email.count('@') != 1:
				continue
			if not email[0].isalnum() or not email[len(email)-1].isalpha():
				continue
			for i in range(1,len(email)):
				if email[i].isalnum():
					continue
				elif email[i] in specialChars:
					if email[i+1] in specialChars:
						validEmail = False
						break
					if email[i] == '@':
						domain = email[i+1:len(email)]
						local = email[0:i]
						if len(domain) > 255 or len(local) > 64:
							validEmail = False
							break
					continue
				else:
					validEmail = False
					break

			if not validEmail:
				continue
			if '.' not in domain:
				continue
			periodIndex = domain.index('.')
			tld = domain[periodIndex+1:len(domain)]
			if len(tld) < 2:
				continue

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
