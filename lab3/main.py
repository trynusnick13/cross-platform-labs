from math_ops import add, subtract, multiply

########## Correct Work ##########
print(add(1, 5))
print(subtract(4, 6))
print(multiply(4, 2))

########## Wrong arguments
print(add(1, "5")) # TypeError: in method 'add', argument 2 of type 'int'
print(add(1, 5.5)) # TypeError: in method 'add', argument 2 of type 'int'
