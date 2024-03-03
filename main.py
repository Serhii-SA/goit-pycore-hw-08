#  ДЗ 07
from collections import UserDict
from datetime import datetime , date , timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value): 
        self.value = value

class Phone(Field):
		pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phone: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}"

    def add_phone(self,ph_num_to_add):
        if len(ph_num_to_add)== 10:
            self.phones.append(Phone(ph_num_to_add))
        else:
            print("Phonenumber has invalid format")
            raise TypeError

    def add_birthday(self,b_day):
         self.birthday=Birthday(b_day)

    def find_phone(self,str_nb):
        for n in self.phones:
            if n.value == str_nb:
                return str_nb                  
        print(f"Contact {self.name} doesn`t consists {str_nb}")
    
class AddressBook(UserDict):
    def add_record(self,cont):
            self.data.update([(cont.name,cont)])

    def show_all(self):
        if self.data == {}:
            return print("\nContacts list is empty.\n")
        for name, record in self.data.items():
            print(record)  

    def find(self,nm):
        for name, record in self.data.items():
            if name.value == nm :
                return record
        print(f"No < {nm} > contact in the phonebook")
        raise TypeError
                
    def delete(self,nm):
        for name, record in self.data.items():                
            if name.value == nm :
                n_del = name
        try:         
            self.data.pop(n_del)
        except Exception:
            print(f"No < {nm} > contact in the phonebook") 

    def get_upcoming_birthdays(self):
        dt_tday=datetime.today().date()  #сьог.дата
        prg_out = [] # порожн.список в який засунемо вихідні словники  (ключ name) та дату привітання (ключ congratulation_date, дані якого у форматі рядка 'рік.місяць.дата'). 
        for name, record in self.data.items():
            if record.birthday != None: # Виключаємо контакти без ДР
                crnt_us_nm = name.value

                user_brday = record.birthday.value #зі словника витягає ДР клієнта та робить об.дататайм
                user_brday_crn_year=user_brday.replace(year=dt_tday.year) # замінюєм рік в ДР на поточн.

                delta = user_brday_crn_year.toordinal()-dt_tday.toordinal() # визначаємо різницю в дн.між ДР та поточн.датою знак(-) -ДР вже був
               
                if 0<= delta < 8 : # якщо ДР клієнта в найближчі 7днів
                    week_d = user_brday_crn_year.weekday() # визначаємо день тижня
                  
                    if 0<= week_d<5 : # якщо ДР у робочий день
                        cr_lst_conday =[crnt_us_nm,user_brday_crn_year.strftime("%Y.%m.%d")]

                    elif week_d==5: # якщо ДР у сб
                        us_bdsd_repl = user_brday_crn_year + timedelta(days=2)
                        cr_lst_conday =[crnt_us_nm,us_bdsd_repl.strftime("%Y.%m.%d")]

                    else: # решта тоді ДР у нд
                        us_bdsd_repl = user_brday_crn_year + timedelta(days=1)
                        cr_lst_conday =[crnt_us_nm, us_bdsd_repl.strftime("%Y.%m.%d")]
                    prg_out.append(cr_lst_conday)

                elif delta < 0: # якщо ДР вже минув
                    us_bdsd_repl = user_brday_crn_year.replace(year=dt_tday.year+1) # додаємо 1рік до дня привітання
                    cr_lst_conday =[crnt_us_nm, us_bdsd_repl.strftime("%Y.%m.%d")]
                    prg_out.append(cr_lst_conday)
        return prg_out

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return print("You didn't attached the Name and phone nbr or attached too many arg-s(or wrong format).\nGive me correct imput, please.")
        except KeyError:
            nm = args[0]
            return print(f"No user with name - {nm[0]}")
        except IndexError:
            return print("Недостатньо аргументів")
        except Exception:
            return print("Something wrong :( ")
    return inner

text= ''' 
Для даного Боту доступні нижчеперелічені команди :

"add <username> <phone>".

 За цією командою бот зберігає у пам'яті, 
новий контакт. Користувач вводить ім'я <username> та номер телефону <phone>, обов'язково через пробіл.

"change <username> <phone>"
За цією командою бот зберігає в пам'яті новий номер телефону <phone> для 
контакту <username>, що вже існує в записнику.

"phone <username>"
 За цією командою бот виводить у консоль номер телефону для зазначеного контакту <username>.

"all"
 За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.

 "add-birthday <username> <birthday date (Date format (DD.MM.YYYY)) >"
 За цією командою бот зберігає в пам'яті дату народження для контакту <username>.

 "show-birthday <username>"
 За цією командою бот виводить у консоль дату народження для зазначеного контакту <username>.

 "birthdays"
 За цією командою бот показує список користувачів, яких потрібно привітати по днях на наступному тижні
 та дати привітання(якщо дата привітання попадає на вих.день,привітання переноситься на пн.).

"close", "exit"
 за будь-якою з цих команд бот завершує свою роботу
 '''

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    nme, phone = args

    for n in contacts.data:
        if nme == n.value:
            return print(f"Contact with name {nme} is already exists.If you'd like to change it, use command 'change'")
        
    r=Record(nme)
    r.add_phone(phone)
    contacts.add_record(r)
    return print("Contact added.")


@input_error
def chng_contact(args, contacts):    
        nme, phone = args
        if len(phone)== 10:
            for n in contacts.data:
                if nme == n.value:
                    temp_rec=contacts.find(nme)
                    temp_bd=temp_rec.birthday
                    contacts.delete(nme)
                    r=Record(nme)
                    r.add_phone(phone)
                    if temp_bd != None:
                        r.add_birthday(temp_bd)
                    contacts.add_record(r)
                    return print(f"Contact {nme} phone changed")
            return print(f"Contact {nme} doesn`t exist.")
        else:
            print("Phonenumber has invalid format")
            raise TypeError 

@input_error
def usn_ph(args, contacts):
    nme = args[0]
    for n in contacts.data:
        if nme == n.value:
            return print(contacts.find(nme))
    print(f"No user with name - {nme}")

@input_error
def add_bd (args,contacts):#Date format (DD.MM.YYYY)
        if len(args[1])==10 and datetime.today()>datetime.strptime(args[1],'%d.%m.%Y'):
            b_dt = args[1]
            try:
                y=int(b_dt[6:10]); m=int(b_dt[3:5]); d=int(b_dt[0:2])
                user_date = date(y,m,d)
                temp_cont = contacts.find(args[0])
                temp_cont.add_birthday(user_date)
                print("Birthday date added")

            except Exception:
                print("Invalid date or format(use DD.MM.YYYY format)")
        else:
            print("Invalid date or format(use DD.MM.YYYY format)")
            raise TypeError
            
@input_error
def show_birthday(args,contacts):
        nme = args[0]
        for n in contacts.data:
            if nme == n.value:
                temp_bd = contacts.find(nme)
                return print(f"{nme} contact`s birthday is {temp_bd.birthday}(YYYY-MM-DD)")
        print(f"No user with name - {nme}")

@input_error
def birthdays(args,contacts):
    return contacts.get_upcoming_birthdays()

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

        
def main():
    contacts = load_data()

    print("Welcome to the assistant bot!\n(\"Help\"-for help)")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("\n Good bye! Your AddressBook is saved \n")
            save_data(contacts)
            break

        elif command == "hello":
            print("How can I help you?(\"Help\"-for help)")
        elif command == "add":
            add_contact(args, contacts)
        elif command == "all":
            contacts.show_all()
        elif command == "change":
            chng_contact(args, contacts)
        elif command == "phone":
            usn_ph(args, contacts) 
        elif command == "help":
            print(text)    
        elif command == "add-birthday":
            add_bd(args, contacts)
        elif command == "show-birthday":
            show_birthday(args, contacts)
        elif command == "birthdays":
            p =  birthdays(args, contacts)
            if p:
                for p_i in p:
                    print(f"Don`t forget to cong {p_i[0]} on day {p_i[1]}(YYYY-MM-DD)")
            else:
                print("На цьому тижні ДР немає")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

