from django.test import TestCase

# Create your tests here.
while True:
    num = int(input("Enter number"))
    if num %2 == 0:
        print(f"{num} is an even number")
    else:
        print(f"{num} is an odd number")

    c = input("want to continue? [y/n]")
    if c == 'n':
        break