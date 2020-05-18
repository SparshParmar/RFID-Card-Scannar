import s_backend as server_back
import the_databse as create_db
import tkinter
from tkinter.simpledialog import askstring
import sqlite3
import time

# Thw main window.
window = tkinter.Tk()


def add_terminal():
    GUID = askstring("Create Terminal:", "Enter Terminal GUID: ")
    Name = askstring("Create Terminal:", "Enter Terminal Name: ")
    create_db.insertT(time.ctime(), Name, GUID)
    print("Terminal : " + Name + " " + GUID + " Added")


def remove_terminal():
    GUID = askstring("Remove Terminal:", "Enter Terminal GUID: ")
    con = sqlite3.connect('client_db.db')
    cur = con.cursor()
    cur.execute("select terminal_id  from terminals")
    data = cur.fetchall()
    Existing = False
    for item in data:
        if item[0] == GUID:
            Existing = True
    if Existing:
        create_db.deleteT(GUID)
        print("Terminal : " + GUID + " Removed")
        con.commit()
        con.close()
    else:
        print("Non Existing Terminal " + GUID)


def add_worker():
    Guid = askstring("ADD Worker:", "Enter Worker GUID: ")
    Name = askstring("Create Name :", "Enter Worker First Name: ")
    Surname = askstring("Create Surname :", "Enter Worker Surname: ")
    card = askstring("ADD Card Guid:", "choose your Card GUID: ")

    create_db.insertW(Guid, Name, Surname, card)
    print("Terminal : " + Name + " " + Surname + " " + Guid + " " + card + " Added")


def remove_worker():
    GUID = askstring("Remove Worker:", "Enter Worker GUID: ")
    con = sqlite3.connect('client_db.db')
    cur = con.cursor()
    cur.execute("select worker_guid  from workers")
    data = cur.fetchall()
    Existing = False
    for item in data:
        if item[0] == int(GUID):
            Existing = True
    if Existing:
        create_db.deleteW(GUID)
        print("Worker : " + GUID + " Removed")
        con.commit()
        con.close()
    else:
        print("Non Existing worker " + GUID)


def add_card():
    GUID = askstring("ADD Card:", "Enter Worker GUID: ")
    con = sqlite3.connect('client_db.db')
    cur = con.cursor()
    cur.execute("""SELECT worker_guid FROM workers """)
    user = cur.fetchall()
    exist = False
    for item in user:
        if int(item[0]) == int(GUID) | int(item[0]) == int(GUID):
            exist = True
            card = askstring("ADD Card Guid:", "choose your Card GUID: ")
            create_db.add_card(GUID, card)
            print("card added to user : " + GUID)
    if not exist:
        print("Worker with GUID: " + GUID + " doesn't not exist")
    cur.close()
    con.commit()
    con.close()


def remove_card():
    card = askstring("Remove Card Guid:", "Enter Card GUID: ")
    con = sqlite3.connect('client_db.db')
    cur = con.cursor()
    cur.execute("""SELECT Card_guid FROM workers """)
    user = cur.fetchall()
    exist = False
    for item in user:
        if int(item[0]) == int(card) | int(item[0]) == int(card):
            exist = True
            create_db.remove_card(card)
            print("Removed card :" + card)
    if not exist:
        print("Worker with card GUID: " + card + " doesn't not exist")
    cur.close()
    con.commit()
    con.close()


def generate_report():
    GUID = askstring("Worker Guid:", "Enter Worker GUID: ")
    con = sqlite3.connect('client_db.db')
    cur = con.cursor()
    cur.execute("select worker_guid  from workers")
    data = cur.fetchall()
    Existing = False
    for item in data:
        if item[0] == int(GUID):
            Existing = True
    if Existing:
        create_db.print_report(GUID)
        con.commit()
        con.close()
    else:
        print("Non Existing Worker " + GUID)


def print_workers_database():
    connetion = sqlite3.connect("client_db.db")
    cursor = connetion.cursor()
    cursor.execute("select worker_guid, First_Name, Surname, Card_guid from workers")
    log_entrys = cursor.fetchall()
    labels_log_entry = []
    print_log_window = tkinter.Tk()

    for log_entry in log_entrys:
        labels_log_entry.append(tkinter.Label(print_log_window, text=(
                "Employee\n---Guid : %s :%s  %s ---Card Guid :%s" % (
            log_entry[0], log_entry[1], log_entry[2], log_entry[3]))))

    for label in labels_log_entry:
        label.pack(side="top")

    connetion.commit()
    connetion.close()

    # Display this window.
    print_log_window.mainloop()


def print_terminals():
    connetion = sqlite3.connect("client_db.db")
    cursor = connetion.cursor()
    cursor.execute("select Time, terminal_id, terminal_name  from terminals")
    log_entrys = cursor.fetchall()
    labels_log_entry = []
    print_log_window = tkinter.Tk()

    for log_entry in log_entrys:
        labels_log_entry.append(tkinter.Label(print_log_window, text=(
                "Terminal\n---Created on : %s : %s : %s" % (log_entry[0], log_entry[1], log_entry[2]))))

    for label in labels_log_entry:
        label.pack(side="top")

    connetion.commit()
    connetion.close()
    # Display this window.
    print_log_window.mainloop()


def create_main_window():
    window.geometry("360x200")
    window.title("Server")
    label = tkinter.Label(window, text="Choose option bellow: ")
    label.grid(row=0, column=0)
    button_1 = tkinter.Button(window, text="Add new terminal",
                              command=lambda: add_terminal())
    button_1.grid(row=2, column=0)
    button_2 = tkinter.Button(window, text=" Remove terminal",
                              command=lambda: remove_terminal())
    button_2.grid(row=3, column=0)
    button_3 = tkinter.Button(window, text="Add worker",
                              command=lambda: add_worker())
    button_3.grid(row=4, column=0)
    button_4 = tkinter.Button(window, text="Remove worker",
                              command=lambda: remove_worker())
    button_4.grid(row=5, column=0)
    button_5 = tkinter.Button(window, text="Add card",
                              command=lambda: add_card())
    button_5.grid(row=6, column=0)
    button_6 = tkinter.Button(window, text="Remove card",
                              command=lambda: remove_card())
    button_6.grid(row=2, column=1)
    button_7 = tkinter.Button(window, text=" Print workers database",
                              command=lambda: print_workers_database())
    button_7.grid(row=3, column=1)

    button_8 = tkinter.Button(window, text="Print terminals saved in database",
                              command=lambda: print_terminals())
    button_8.grid(row=4, column=1)
    button_9 = tkinter.Button(window, text=" Generate Report for employee",
                              command=lambda: generate_report())
    button_9.grid(row=5, column=1)
    hello_button = tkinter.Button(window, text="Hello from the server", command=lambda:
    server_back.client.publish("worker/name", "Hello from the server")).grid(row=7, column=0)

    exit_button = tkinter.Button(window, text="Quit", command=window.quit).grid(row=7, column=1)
    print_log_button = tkinter.Button(
        window, text="Print log", command=server_back.print_log_to_window).grid(row=6, column=1)


def run_receiver():
    server_back.run_receiver()
    create_main_window()
    # Start to display window (It will stay here until window is displayed)

    window.mainloop()
    server_back.disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
