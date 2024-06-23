# class FacadeNewsletter:
#     def __init__(self, users_system, email_system) -> None:
#         self._users_system = users_system
#         self._email_system = email_system

#     def sending(self) -> str:
#         users = self._users_system.get_users()
#         male, female = self._users_system.separate_users(users)
#         text_for_male = self._email_system.get_text_email("male")
#         text_for_female = self._email_system.get_text_email("female")
#         self._email_system.send_emails(male, text_for_male)
#         self._email_system.send_emails(female, text_for_female)
#         return "Done"


# class UsersSystem:
#     def get_users(self) -> list:
#         users = [
#             {
#                 "name": "Allen Raymond",
#                 "email": "nulla.ante@vestibul.co.uk",
#                 "gender": "male",
#             },
#             {
#                 "name": "Chaim Lewis",
#                 "email": "dui.in@egetlacus.ca",
#                 "gender": "male",
#             },
#             {
#                 "name": "Kennedy Lane",
#                 "email": "mattis.Cras@nonenimMauris.net",
#                 "gender": "female",
#             },
#             {
#                 "name": "Wylie Pope",
#                 "email": "est@utquamvel.net",
#                 "gender": "female",
#             },
#         ]
#         return users

#     def separate_users(self, users) -> tuple:
#         male = []
#         female = []
#         for person in users:
#             if person.get("gender", None) == "male":
#                 male.append(person)
#             else:
#                 female.append(person)
#         return male, female


# class EmailSystem:
#     def get_text_email(self, gender) -> str:
#         text = "Default text"
#         if gender == "male":
#             text = "Male text email"
#         if gender == "female":
#             text = "Female text email"

#         return text

#     def send_emails(self, users, text) -> str:
#         for person in users:
#             print(f"Send {person.get('name')} email: {text}")
#         return "Done"


# def client_code(newsletter) -> None:
#     print(newsletter.sending(), end="")


# if __name__ == "__main__":
#     facade = FacadeNewsletter(UsersSystem(), EmailSystem())
#     client_code(facade)


# from threading import Thread
# import logging
# from time import sleep


# def example_work(params):
#     sleep(params)
#     logging.debug('Wake up!')


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
#     logging.debug('Start program')
#     threads = []
#     for i in range(5):
#         thread = Thread(target=example_work, args=(i,))
#         thread.start()
#         threads.append(thread)

#     [el.join() for el in threads]

#     logging.debug('End program')


# from threading import Timer
# import logging
# from time import sleep


# def example_work():
#     logging.debug('Start!')


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

#     first = Timer(0.5, example_work)
#     first.name = 'First thread'
#     second = Timer(0.7, example_work)
#     second.name = 'Second thread'
#     logging.debug('Start timers')
#     first.start()
#     second.start()
#     sleep(0.6)
#     second.cancel()

#     logging.debug('End program')

# from threading import Thread, Condition
# import logging
# from time import sleep


# def worker(condition: Condition):
#     logging.debug('Worker ready to work')
#     with condition:
#         condition.wait()
#         logging.debug('The worker can do the work')


# def master(condition: Condition):
#     logging.debug('Master doing some work')
#     sleep(2)
#     with condition:
#         logging.debug('Informing that workers can do the work')
#         condition.notify()
#         condition.notify()


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
#     condition = Condition()
#     master = Thread(name='master', target=master, args=(condition,))

#     worker_one = Thread(name='worker_one', target=worker, args=(condition, ))
#     worker_two = Thread(name='worker_two', target=worker, args=(condition,))
#     worker_one.start()
#     worker_two.start()
#     master.start()

#     logging.debug('End program')

# import concurrent.futures
# import math


# PRIMES = [
#     401,
#     112582705942171,
#     112272535095293,
#     115280095190773,
#     115797848077099,
#    111111111111111 ]


# def is_prime(n):
#     if n < 2:
#         return False
#     if n == 2:
#         return True
#     if n % 2 == 0:
#         return False

#     sqrt_n = int(math.floor(math.sqrt(n)))
#     for i in range(3, sqrt_n + 1, 2):
#         if n % i == 0:
#             return False
#     return True


# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor(4) as executor:
#         for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
#             print('%d is prime: %s' % (number, prime))

# from threading import Thread
# from time import sleep
# from http import client
# from http.server import HTTPServer, BaseHTTPRequestHandler


# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b'Hello, world!')

#     def do_POST(self):
#         pass


# httpd = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
# server = Thread(target=httpd.serve_forever)
# server.start()
# sleep(0.5)

# h1 = client.HTTPConnection('localhost', 8001)
# h1.request("GET", "/")

# res = h1.getresponse()
# print(res.status, res.reason)
# data = res.read()
# print(data)

# httpd.shutdown()
# from jinja2 import Template

# name = 'Bill'
# age = 28

# tm = Template("My name is {{ name }} and I am {{ age }}")
# msg = tm.render(name=name, age=age)

# print(msg)  # My name is Bill and I am 28
# finally

# from http.server import HTTPServer, BaseHTTPRequestHandler
# import urllib.parse


# class HttpHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         pr_url = urllib.parse.urlparse(self.path)
#         if pr_url.path == '/':
#             self.send_html_file('index.html')
#         elif pr_url.path == '/contact':
#             self.send_html_file('contact.html')
#         else:
#             self.send_html_file('error.html', 404)

#     def send_html_file(self, filename, status=200):
#         self.send_response(status)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         with open(filename, 'rb') as fd:
#             self.wfile.write(fd.read())


# def run(server_class=HTTPServer, handler_class=HttpHandler):
#     server_address = ('', 8000)
#     http = 
#           server_class
#           (server_address, handler_class)
#     try:
#         http.serve_forever()
#     except KeyboardInterrupt:
#         http.server_close()


# if __name__ == '__main__':
# #     run()

# dict =  {"this" : "a", "kielki": "b"}

# value = dict.get("kielki")




# # print(value)
# from faker import Faker

# fake = Faker()

# names = []

# for _ in range(10):
#     name = fake.name()
#     names.append(name)


# print(names)

tasks = []

def add_task(task):
    tasks.append(task)

def list_tasks():
    for idx, task in enumerate(tasks):
        print(f"{idx}. {task}")

add_task("Learn Python")
add_task("Build a project")
list_tasks()


student = {"name": "Alice", "age": 25}
student["grade"] = "A"
for key, value in student.items():
    print(key, value)

class Node():
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list as None

    def append(self, data):
        new_node = Node(data)  # Create a new node with the given data
        if not self.head:  # If the list is empty, make the new node the head
            self.head = new_node
            return
        last = self.head
        while last.next:  # Traverse to the end of the list
            last = last.next
        last.next = new_node  # Append the new node at the end

    def display(self):
        current = self.head
        while current:  # Traverse through the list
            print(current.data, end=" -> ")
            current = current.next
        print("None")

# Create a linked list
ll = LinkedList()

# Append elements to the linked list
ll.append(10)
ll.append(20)
ll.append(30)

# Display the linked list
ll.display()
