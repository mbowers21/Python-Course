#Starting Practices
#String
name="John"
print(name)
#Integer
age=30
print(age)
#Float
height = 5.9
print(height)
#Boolean
is_student = True
print(is_student)
print (name, age, height, is_student)
#Basic Arithmetic
a = 10
b = 3
sum = a + b
difference = a - b
product = a * b
quotient = a / b
print("Sum:", sum, "Difference:", difference, "Product:", product, "Quotient:", quotient)
#Integer Quotient and Remainder
integer_quotient = a // b
remainder = a % b
power = a ** b
print("Integer Quotient:", integer_quotient, "Remainder:", remainder, "Power:", power)
#String Concatenation
first_name = "John"
middle_name = "Doe"
last_name = "Smith"
full_name = last_name + "," + first_name + middle_name
print("Full Name:", full_name)
#F String
f_string = f"My name is {first_name} {last_name} and I can add {a} and {b} to get {sum}."
print(f_string)
#Lists, Dictionaries, and Sets
#List
fruits = ["apple", "banana", "cherry"]
print(fruits[0])  # Accessing the first element
fruits.append("orange")  # Adding an element to the list
print(fruits)
fruits.remove("apple") # Removing an element from the list
print(fruits[0])
len(fruits) # Length of the list
print(len(fruits))
#Dictionary
person = {"name": "John", "age": 30, "city": "New York"}
print(person["name"])  # Accessing a value by key
person["height"] = 5.9  # Adding a new key-value pair
print(person)
#Sets
unique_numbers = {1, 2, 3, 4, 5}
unique_numbers_b = {1, 1, 3, 4, 5}
print(unique_numbers, unique_numbers_b)
#Conditionals
age = 100
if age < 18:
    print("You are a minor.")
    print("You cannot vote.")
    is_minor = True
elif age < 65:
    print("You are an adult.")
    is_minor = False
elif age < 80:
    print("You are an old adult.")
else:
    print("You are an ancient individual.")
#Loops
#For Loop
for i in range(5):
    print(range(5)[i])
print (range(3))
#While Loop
count = 10
while count > 0:
    print(count)
    count -= 1
for fruit in fruits:
    print(fruit)
#Functions
def testfunction():
    print("This is a test function with no inputs.")

testfunction()
def greet(name):
    print(f"Hello, {name}!")
greet("Alice")
name = "Bob"
greet("Alice")
greet(name)

name_integer = 123
greet(name_integer)

def add(a, b):
    return a + b
print(add(5, 3))
print(add("Hello, ", str(3)))