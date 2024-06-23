# ############## 1) Inheritance #############

# class Car():
#     def __init__(self, make: str, model: str, year: int, mileage: float):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.mileage = mileage


#     def spec(self):
#         return f"Make:{self.make}, Mode:{self.model}, Year:{self.year}, Mileage:{self.mileage}"

# car1 = Car("Royal", "Sedan", 2019, 13.000)
# car2 = Car("Toyota", "Universal", 2020, 10.000)
# print(car1.spec())
# print(car2.spec())

# ############## 2) Encapsulation #############

# class Car():
#     def __init__(self, make: str, model: str, year: int, mileage: float, is_driving: bool = False):
#         self.__make = make
#         self.__model = model
#         self.__year = year
#         self.__mileage = mileage
#         self.is_driving = is_driving


#     def spec(self):
#         return f"Make:{self.__make}, Mode:{self.__model}, Year:{self.__year}, Mileage:{self.__mileage}"
    
#     def start(self):
#         if self.is_driving:
#             print (f"Car:{self.__model} is driving")
#         else:
#             self.is_driving = False
#             print (f"Car:{self.__model} on Parking")
        

#     def drive(self,distance):
#         if self.is_driving:
#             self.__mileage += distance
#             print (f"Car:{self.__model} drove {distance} miles")
#         else:
#             print (f"Car:{self.__model} drove {distance} miles")

#     def stop(self):
#         if self.is_driving:
#             print (f"Car:{self.__model} stopped")
#         else:
#             print (f"Car:{self.__model} remain on Parking")

#     def get_millage(self):
#         print (f"Car:{self.__model} current mileage is {self.__mileage}")

# car1 = Car("Royal", "Sedan", 2019, 13.000,True)
# car2 = Car("Toyota", "Universal", 2020, 10.000)
# print(car1.spec())
# print(car2.spec())


# car1.start()
# car1.drive(20.000)
# car1.stop()
# car1.get_millage()
# print()
# car2.start()
# car2.drive(0)
# car2.stop()
# car2.get_millage()

# ############## 3) Inheritance and Polymorphism #############

# class Vehicle():
#     def __init__(self, make: str, model: str, year: int, mileage: float):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.mileage = mileage

#     def details(self):
#         return f"Make:{self.make}, Mode:{self.model}, Year:{self.year}, Mileage:{self.mileage}"

# class Car(Vehicle):
#      def __init__(self, make: str, model: str, year: int, mileage: float, doors: int, fuel: str):
#         super().__init__(make,model,year,mileage)
#         self.doors = doors
#         self.fuel = fuel
   
#      def details(self):
#         return f"{super().details()}, Nb.of doors:{self.doors}, Fuel type:{self.fuel}"
    

#      def drive(self):
#         print(f"Car: {self.model} is driving")
    
# car1 = Vehicle("Steel", "Shitsler", 2019, 13.000)
# car2 = Car("Titan", "Toyota", 2020, 10.000, 5, "diesel")
# print(car1.details())
# print(car2.details())
# car2.drive()



# ############# 4) Composition #############

# class Engine():
#     def __init__(self, fuel_type: str, horsepower : str, manufacturer: str):
#         self.fuel_type = fuel_type
#         self.horsepower = horsepower
#         self.manufacturer = manufacturer

#     def details(self):
#         return f"Manufacturer: {self.manufacturer}, Horesower:{self.horsepower},Fuel: {self.fuel_type}"

# class Car(Engine):
#     def __init__(self, make: str, model: str, year: int, mileage: float, engine : Engine):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.mileage = mileage
#         self.engine = engine

#     def details(self):
#         return f"Make:{self.make}, Mode:{self.model}, Year:{self.year}, Mileage:{self.mileage},Engine: {self.engine.details()}"

# car_engine = Engine("Diesel", 200, "Lexus")
# print(car_engine.details())
# car1 = Car("Titan", "Toyota", 2020, 10.000,car_engine)
# print(car1.details())
    
# ############# 5) Abstraction #############
# from abc import ABC, abstractmethod
# from math import pi

# class Shape(ABC):
#     @abstractmethod
#     def calculate_area(self) -> float:
#         pass

# class Rectangle(Shape):
#     def __init__(self, width: float, length: float):
#         self.width = width
#         self.length = length

#     def calculate_area(self) -> float:
#         return self.width * self.length

# class Circle(Shape):
#     def __init__(self, radius: float):
#         self.radius = radius

#     def calculate_area(self) -> float:
#         return self.radius ** 2 * pi

# # Creating instances of Rectangle and Circle
# rectangle = Rectangle(4, 5)
# print(rectangle.calculate_area())  # Output: 20

# circle = Circle(4)
# print(circle.calculate_area())  # Output: 50.26548245743669

############# 6) Setter and getter Method #############

# class Car():
#     def __init__(self):
#         self.__make = "Japan"
#         self.__model = "Toyota"
#         self.__year = 2022
#         self.__milege = 10000

#     @property
#     def info(self):
#         print("getter called")
#         return self.__make,self.__model,self.__year, self.__milege
    
#     @info.setter
#     def info(self,data):
#         print("setter method called")
#         self.__make,self.__model,self.__year, self.__milege = data
        

# car = Car()
# car.info="Germany","VW",2019,23000
# print(car.info)


############# 7) Operator Overloading Method #############



# list = []
# a = 110
# list.append(a**2)
# list2 = [1,3,4]
# list2.extend(list)

# print(list2)


def foo (table: list[str] | str, src: list | None =None)-> list:
    if src is None:
        src =[]
    if isinstance(table,list):
        src.extend(table)
    else:
        src.append(table)
    return src

x1=foo(["test1"])
print(x1)
x=foo(["test2"],x1)
print(x)
x2=foo(["test3"])
print(x2)