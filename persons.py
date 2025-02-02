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
			id = row["Id"]
			idLetters = ['a','b','c','d','e','f','A','B','C','D','E','F']
			validId = True
			if id == "":
				continue
			if id in ids:
				continue
			if len(id) != 36:
				continue
			if id[8] != '-' or id[13] != '-' or id[18] != '-' or id[23] != '-':
				continue
			for i in range(len(id)):
				if id[i].isnumeric() or id[i] in idLetters or id[i] == '-':
					continue
				else:
					validId = False
					break

			if not validId:
				continue
			ids.append(id)

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

			# Salary Validation
			salary = row["Salary"]
			validSalary = True
			if salary.count('.') != 1:
				continue
			if salary[0] == '0' and salary[1] != '.':
				continue
			for i in range(len(salary)):
				if salary[i].isnumeric():
					continue
				elif salary[i] == '.':
					if i == 0 or len(salary) != i+3:
						validSalary = False
						break
				else:
					validSalary = False
					break

			if not validSalary:
				continue
			row["Salary"] = float(salary)

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
