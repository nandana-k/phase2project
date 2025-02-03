# Phase 2 Project

This project creates an API server that reads a CSV file containing 100 person records. It stores valid records in memory (and skips invalid records) and provides two HTTP endpoints to retrieve this data. This program can be used to read CSV files and validate personal information including UUID v4 IDs, first and last names, emails, and salaries. The HTTP endpoints can be used to retrieve 10 person records and look up a person by their ID.

## Installation

It is necessary to install pip and Flask to use this project.

## Usage

Upon application start, the server will start up and read the CSV file (persons.csv). It will check each record and store them in memory as JSON if they are valid or skip them if they are invalid. All valid records are stored in the lists data and persons_list in memory. The server listens on port 8080.

### Validation

The following descriptions explain the validation process for each piece of information in the CSV file.

#### Id Validation

The Id validation process includes checking if an Id is non-empty, unique, and follows UUID v4 format. The program first validates that the Id is not an empty string, and then checks that it is not the same Id as anyone else's (unique). This is done by storing valid Ids in the list ids and checking that the current Id has not already been added to the list. To check for valid UUID v4 format, the program sees if the length of the Id is 36, the appropriate indices contain the '-' character, and that only valid letters and numbers are included in the Id. If an Id has these specifications, it is added to the ids list.

#### First_Name and Last_Name Validation

To validate first and last names, the program first checks if all the characters in the names are alphabetical characters. Then, it checks to see if the first letter of the first and last names is uppercase. Finally, it checks that the remaining letters in the first and last names are lowercase.

#### Email Validation

To validate emails, the program first checks if the length of the email is at most 320 characters and that it only contains one '@' symbol. Then, it checks that the first character is alphanumeric and that the last character is an alphabetical character. Next, it loops through the characters of the email and checks that each character is either alphanumeric or a special character contained in the list specialChars. It makes sure that special characters are not next to each other and that the local and domain parts of the email are appropriate lengths (maximum of 64 and 255 characters, respectively). Finally, it checks to see if there is a period ('.') in the domain portion of the email and that the top-level domain (TLD) that comes after the period is an appropriate length (two characters or more).

#### Salary Validation

To validate salary, it is first checked that there is exactly one period ('.') in the string. Then, the program checks that if the first character is '0', the second character must be the period ('.'), because otherwise a number like 040000.00 could be considered valid. Then, the program loops through the salary string and ensures that the characters are either numeric or the period ('.'). It also checks that the string does not start with the period ('.') or have a length that is not equal to the index of the period plus 3 (this ensures that the salary goes to 2 decimal points). Finally, if the salary meets the correct specifications, it is converted to a float value.

### API Endpoints

#### GET /persons

When a request is sent to the /persons endpoint, it will return the first 10 person records in JSON format. The status code is 200. One record looks like this, for example:

```json
[
 {
    "Id": "7b0a853a-740a-4118-97e0-ed592b5379e7",
    "First_Name": "Preston",
    "Last_Name": "Lozano",
    "Email": "vmata@colon.com",
    "Salary": 271896.64
 }
]
```

#### GET /persons/\<id\>

When a request is sent to the persons/\<id\> endpoint, if the given id is found, the person with that id's record will be returned in JSON format (the same format as shown above). The status code is 200. If the id is not found, a 404 error ("Person not found") will be returned.

## Error Handling

As mentioned above, a 404 error is returned when an id is not found/recognized. A 500 error ("Internal Server Error") is returned when the program is met with unexpected issues. For CSV errors, rows with invalid information are skipped.
