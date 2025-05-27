import random
import pickle
import sys
logged_in=False
uid=0
pwd=''
class Train:
    def __init__(self,name,num,arr_time,dep_time,src,des,day,seats_1ac,seats_2ac,seats_sl,fare_1ac,fare_2ac,fare_sl):
        self.name,self.num,self.arr_time,self.dep_time,self.src,self.des,self.day=name,num,arr_time,dep_time,src,des,day
        self.seats={'1AC':seats_1ac,'2AC':seats_2ac,'SL':seats_sl}
        self.fare={'1AC':fare_1ac,'2AC':fare_2ac,'SL':fare_sl}
    def print_seats(self):
        for coach,seats in self.seats.items():
            print(f"No.of seats available in{coach}:{seats}")
    def check_availability(self,coach,tickets):
        return self.seats[coach]>=tickets if coach in self.seats else False
    def book_ticket(self,coach,tickets):
        self.seats[coach]-=tickets
class Ticket:
    def __init__(self,train,user,tickets,coach):
        self.pnr=f"{train.num}{user.uid}{random.randint(100,999)}"
        self.train_num,self.coach,self.uid,self.train_name,self.user_name,self.tickets=train.num,coach,user.uid,train.name,user.name,tickets
        user.history[self.pnr]=self
        ticket_dict[self.pnr]=self
class User:
    def __init__(self,uid,name,pwd):
        self.uid,self.name,self.pwd,self.history=uid,name,pwd,{}
def accept_input(prompt,validation):
    while True:
        value=input(prompt)
        if validation(value):
            return value
        print("Invalid input,try again.")
def book_ticket():
    if not logged_in:login()
    train_num=int(accept_input("Enter train number: ",lambda x: x.isdigit() and int(x) in trains))
    trains[train_num].print_seats()
    coach=accept_input("Enter coach (1AC/2AC/SL): ",lambda x: x.upper() in ['1AC','2AC','SL']).upper()
    tickets=int(accept_input("Enter number of tickets: ",lambda x: x.isdigit()))
    if trains[train_num].check_availability(coach,tickets):
        print(f"Amount to pay:{trains[train_num].fare[coach]*tickets}")
        if accept_input("Confirm?(y/n): ",lambda x: x.lower()in['y','n'])=='y':
            trains[train_num].book_ticket(coach,tickets)
            ticket=Ticket(trains[train_num],users[uid],tickets,coach)
            print(f"Booking successful! PNR:{ticket.pnr}")
    else:
        print("Tickets not available.")
    menu()
def cancel_ticket():
    pnr=accept_input("Enter PNR: ", lambda x:x in ticket_dict)
    if accept_input("Cancel ticket?(y/n): ",lambda x:x.lower() in ['y','n'])=='y':
        train_num,coach,tickets=ticket_dict[pnr].train_num,ticket_dict[pnr].coach,ticket_dict[pnr].tickets
        trains[train_num].seats[coach]+=tickets
        del users[ticket_dict[pnr].uid].history[pnr]
        del ticket_dict[pnr]
        print("Ticket cancelled.")
    menu()
def check_pnr():
    pnr=accept_input("Enter PNR: ",lambda x:x in ticket_dict)
    print(f"User:{ticket_dict[pnr].user_name},Train:{ticket_dict[pnr].train_name},Tickets:{ticket_dict[pnr].tickets}")
    menu()
def create_account():
    name,pwd=input("Enter name: "),input("Enter password: ")
    uid=random.randint(1000,9999)
    users[uid]=User(uid,name,pwd)
    print(f"Account created! UID:{uid}")
    menu()
def login():
    global logged_in, uid
    uid=int(accept_input("Enter UID: ",lambda x:x.isdigit() and int(x) in users))
    pwd=accept_input("Enter password: ",lambda x:x==users[uid].pwd)
    logged_in=True
    print(f"Welcome {users[uid].name}!")
    menu()
def menu():
    options={
        1:book_ticket,
        2:cancel_ticket,
        3:check_pnr,
        4:create_account,
        5:login,
        6:exit
    }
    choice=int(accept_input("Choose option(1-6): ",lambda x:x.isdigit() and int(x) in options))
    options[choice]()
trains={12345:Train('Thirumala_Express',12345,'17:45','22:12','ctc','kgp','FRI',30,23,43,2205,320,234)}
users={1111:User(1111,'ram','ram')}
ticket_dict={}

print("Welcome to Indian Railway Reservation Portal")
menu()