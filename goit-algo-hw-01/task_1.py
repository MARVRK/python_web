from collections import UserDict
from datetime import datetime
from abc import ABC, abstractmethod
import datetime as dt
import pickle


class View(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass
    
    @abstractmethod
    def display_commands(self, commands):
        pass

class ConsoleView(View):
    def display_contacts(self, contacts):
        print("Contacts:")
        for contact in contacts:
            print(contact)

    def display_commands(self, commands):
        print("List of commands:")
        for command in commands:
            print(command)

class Field(ABC):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def new_contact(self, name: str)->None:
        self._name=name
              
class Phone(Field):
    def add_phone(self, cell_number: int)->None:
        cell_number_str = str(cell_number)    # Convert to string for length check
        if len(cell_number_str) != 10:         
            raise ValueError("Phone number must contain 10 digits!")
        self.number = cell_number_str

class Birthday(Field):
    def add_birth_d(self,date_str: str)-> None:
        try:
            self.value = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.name.new_contact(name)        # Call contact name to check if it's not none.
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: int):
        phone_field = Phone(phone_number)
        phone_field.add_phone(phone_number)  # Call number_validate method to validate the phone number (not less than 10 digits)
        self.phones.append(phone_field)

    def remove_phone(self, phone_number)-> None:
        for phone in self.phones:
            if phone.number == phone_number:
                self.phones.remove(phone)
    
    def edit_phone(self, new_phone_number: str)-> None:
        for phone in self.phones:
            if phone.number == new_phone_number:
                print("This phone already exist for this current contact.")
            else:
                self.phones.remove(phone)
                new_phone=Phone(new_phone_number)
                new_phone.add_phone(new_phone_number)
                self.phones.append(new_phone)
                print("Phone number updated successfully!")
                    
    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)      
        self.birthday.add_birth_d(birthday_str) # Call birthday to check the correct format

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        else: 
            return "No birthday found for this contact."
    def __str__(self):
            return f"Name: {self.name}, Phones: {[str(phone) for phone in self.phones]}, Birthday: {self.show_birthday()}"
          
class AddressBook(UserDict):
    def add_record(self,name,record):
       self.data[name] = record

    def phone(self, name):
        return self.data[name]

    def find(self,name):
        return self.data[name]

    def delete(self,name):
        del self.data[name]
    
    def show_birthday(self, name):
        if name in self.data:
            record = self.data[name]
            print(f"Name: {name}, Birthday: {record.birthday}")
        else:
            print(f"Name: {name} is not in the list of contacts")

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        current_date = dt.datetime.today()              
        for record in self.values():
            bdate = record.birthday.value
            birthday_this_year = dt.datetime(current_date.year, bdate.month, bdate.day)
            days_until_birthday = (birthday_this_year - current_date).days
            if 0 <= days_until_birthday <=7:
                upcoming_birthdays.append(record)
        return upcoming_birthdays
    
############# Data-Serialisation ##############   
    
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook() 
    
################## Parsing #######################   
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
    
def main():
    view = ConsoleView()
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("Hello! How can I help you?")

        elif command == "commands":
            commands = ["add","change","change","phone","close","exit","all","add-birthday","show-birthday","birthdays"]
            view.display_commands(commands)

        elif command == "add":
            try:
                if len(args) >= 2:
                    record = Record(args[0])
                    record.add_phone(args[1])
                    book.add_record(args[0], record)
                    print("Contact added successfully!")
                else:
                    print("Insufficient arguments. Please provide name and phone.")
            except (IndexError, ValueError) as e:
                print(e)

        elif command == "change":
            try:
                record = book.find(args[0])
                record.edit_phone(args[1])
            except (IndexError, ValueError) as e:
                print (e)

        elif command == "phone":
            try:
                contact = book.find(args[0])
                if contact.phones:
                    for phone in contact.phones:
                        print(f"Phone number for {args[0]}: \n{phone}")
            except (IndexError, ValueError)as e:
                print(f"No contact found: {e}")

        elif command == "all":
            if not book:
                print("No contacts found in the bookaddress")
            view.display_contacts(book.values())

        elif command == "add-birthday":
            try:
                if len(args) >= 2:  
                    record = book.find(args[0]) 
                    record.add_birthday(args[1])
                    print("Birthday date added successfully!")
                else:
                    print("Insufficient arguments. Please provide name and birthday.")
            except (IndexError, ValueError) as e:
                print(e)

        elif command == "show-birthday":
            try:
                record = book.show_birthday(args[0])
            except (IndexError, ValueError,KeyError) as e:
                print(e)

        elif command == "birthdays":
            approaching_birthdays = book.get_upcoming_birthdays()
            if not approaching_birthdays:
                print("No upcoming birthdays found.")
            else:
                for record in approaching_birthdays:
                    print(f"Name: {record.name}, Birthday: {record.show_birthday()}")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()




