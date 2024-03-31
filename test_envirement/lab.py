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

