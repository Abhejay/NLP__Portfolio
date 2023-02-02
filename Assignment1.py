# Assignment: Homework 1
# Name: Abhejay Murali
# Date Due: 2-4-2023

import sys
import pathlib
import re
import pickle


#Person class for Employee
class Person:

    #Person attributes
    def __init__(self, first, last, mi, id, phone):
        self.first = first
        self.last = last
        self.mi = mi
        self.id = id
        self.phone = phone

    #Display employee information
    def display(self):
        space = ' '
        print('Employee id:', self.id)
        print(space*7, self.first + ' ' + self.mi + ' ' + self.last)
        print(space*7, self.phone)
        print()


#Process the text input
def process_lines(text_input):

    #Dictionary of Employees
    employees = {}

    #Loop through input data
    for splitted in text_input:

        #Split input data into each individual person
        individual = splitted.split(',')

        #first and last name capitalized
        lastName = individual[0].capitalize()
        firstName = individual[1].capitalize()

        #middle initial
        if individual[2] == '':
            middleName = 'X'
        else:
            middleName = individual[2].capitalize()

        #Modify ID using Regex (Format: XX4444)
        idPattern = '^\D\D\d\d\d\d$'
        identification = individual[3]
        idResult = re.match(idPattern, identification)
        if not idResult:
            print('ID invalid:', identification)
            print('ID is two letters followed by 4 digits')
            identification = input('Please enter a valid id: ')

        #Modify Phone Number using Regex (Format: 444-444-4444)
        phonePattern = '^\d\d\d[-]\d\d\d[.]\d\d\d\d'
        phoneNumber = individual[4]
        phoneResult = re.match(phonePattern, phoneNumber)
        if phoneResult:
            print('Phone', phoneNumber + ' is invalid')
            print('Enter phone number in form 123-456-7890')
            phoneNumber = input('Enter phone number: ')
        else:
            phoneNumber = phoneNumber.replace(' ', '')
            phoneNumber = phoneNumber.replace('.', '')
            phoneNumber = '{}-{}-{}'.format(phoneNumber[:3], phoneNumber[3:6], phoneNumber[6:])

        #Create Person Object and add to Dictionary of Employees
        person = Person(firstName, lastName, middleName, identification, phoneNumber)
        employees[identification] = person

    #Return Dict of Employees
    return employees



if __name__ == '__main__':

    #Sysarg set up for filename
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read().splitlines()

    #Call process_lines and exclude first title row from data
    employees = process_lines(text_in[1:])

    #Pickle the employees and read the pickle back in
    pickle.dump(employees, open('employees.pickle', 'wb'))
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    #Output Employees
    print('\r\nEmployee list:\n')
    for emp_id in employees_in.keys():
        employees_in[emp_id].display()
