# ### Draft  ####

# while True:
#     operation =  input(f"Choose operation as *,/,+,- or choose exit to quit :")
#     if operation == "exit":
#         break
#     second_value = float(input(f"Put second number: "))
#     first_value = float(input(f"Put first number: ")) 
    
#     if operation == "+":
#         result = first_value + second_value
#         print(result)
#     elif operation == "-":
#         result = first_value - second_value
#         print(result)
#     elif operation == "*":
#         result = first_value * second_value
#         print(result)
#     elif operation == "/":
#         result = first_value / second_value
#         print(result)


#### Refactoring ####

def error(func):
    def wrapper(value1,value2):
        try:
            result = func(value1, value2)
            return result
        except ZeroDivisionError:
            print ("cannot divide by zerooooo!")
    return wrapper        
             
def add(value1: float, value2: float) -> float:
    return (value1 + value2)

def substract(value1: float, value2: float) -> float:
    return (value1 - value2)
@error
def divine(value1: float, value2: float) -> float:
    return (value1 / value2)

def multiply(value1: float, value2: float) -> float:
    return (value1 * value2)

while True:
    try: 
        operation =  input(f"Choose operation as *,/,+,- or choose exit to quit :")
        if operation == "exit":
            break   

        first_value = float(input(f"Put first number: "))
        second_value = float(input(f"Put second number: "))    

      
        if operation == "+":
            print(add(first_value,second_value))
        elif operation == "-":
            print(substract(first_value,second_value))
        elif operation == "/":
            print(divine(first_value,second_value))
        elif operation == "*":
            print(multiply(first_value,second_value))
        else:
            print("Incorrect operation!: *,/,+,- or choose exit to quit")
            
    except ValueError:
        print("strings are forbidden!")

    