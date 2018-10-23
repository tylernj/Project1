import os
import filecmp
#from dateutil.relativedelta import *
from datetime import date
import csv


def getData(file):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows

	new_file = open(file, 'r')
	new_list = []
	lines = new_file.readlines()
	first_row = lines[0]
	first_row = first_row.rstrip()
	first_row = first_row.split(",")

	for line in lines[1:]:
		count = 0
		new_dict = {}
		split_line = line.split(",")
		for item in split_line:
			if first_row[count] not in new_dict:
				new_dict[first_row[count]] = item
			count += 1
		new_list.append(new_dict)
	new_file.close()


	return new_list


def mySort(data,col):
# Sort based on key/column
#Input: list of dictionaries and col (key) to sort on
#Output: Return the first item in the sorted list as a string of just: firstName lastName

	sorted_data = sorted(data, key = lambda x: x[col])

	first_name = sorted_data[0]["First"]
	last_name = sorted_data[0]["Last"]

	return first_name + " " + last_name


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

		class_size = {}

		for dictionary in data:
			if dictionary["Class"] in class_size:
				class_size[dictionary["Class"]] += 1
			else:
				class_size[dictionary["Class"]] = 1



		list_of_tuples = []
		for item in class_size:
			list_of_tuples.append((item, class_size[item]))

		return sorted(list_of_tuples, key = lambda x: x[1], reverse = True)



def findMonth(a):
# Find the most common birth month form this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data
	dict_of_months = {}

	for dictionary in a:
		birth_day = dictionary["DOB"]
		if birth_day[1] == "/":
			birth_month = birth_day[0]
			if birth_month in dict_of_months:
				dict_of_months[birth_month] += 1
			else:
				dict_of_months[birth_month] = 1
		else:
			birth_month = birth_day[:2]
			if birth_month in dict_of_months:
				dict_of_months[birth_month] += 1
			else:
				dict_of_months[birth_month] = 1

	month_list = list(dict_of_months.keys())
	sorted_values = sorted(month_list, key = lambda x: dict_of_months[x], reverse = True)

	most_month = sorted_values[0]
	return int(most_month)



def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as fist,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written

	sorted_data = sorted(a, key = lambda x: x[col])




	open_file = open(fileName, "w")



	for item in sorted_data:
		first_name = item["First"]
		last_name = item["Last"]
		email = item["Email"]
		row = first_name + "," + last_name + "," + email + "\n"
		open_file.write(row)






	open_file.close()




def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.

	ages_list = []
	b_days = []

	for d in a:
		month = int(d["DOB"].split('/')[0])
		day = int(d["DOB"].split("/")[1])
		if month > 10 and day > 23:
			ages_list.append(2017 - int(d['DOB'].split('/')[-1].strip('\n')))
		else:
			ages_list.append(2018 - int(d['DOB'].split('/')[-1].strip('\n')))

	return round(sum(ages_list)/len(ages_list))






################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
