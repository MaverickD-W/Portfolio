# LAB EXERCISE 02

# PROBLEM 01

fruits = ["banana", "apple", "orange"]
print(fruits)
fruits.append("grape")

# PROBLEM 02

def clean_empty(l_str):
	position = -1
	for i in l_str:
		position += 1		
		if i == "":
			l_str.remove("")
			l_str.insert(position, "0")
	l_int = [int(str) for str in l_str]
	return l_int

# PROBLEM 03

def count_ints(lst1, num):
	count = 0
	for a in lst1:
		for b in a:
			if b == num:
				count += 1
			else:
				count = count
	return count

# PROBLEM 04

def remove_duplicates(lst2):
	position = -1
	for a in lst2:
		position += 1
		if lst2.count(a) > 1:
			lst2.remove(a)
			lst2.insert(position, "m")
	while lst2.count("m") > 0:
		lst2.remove("m")
	return lst2