 #!/usr/bin/env python3
# import Project.server_back as server_back
# import Project.server_front as server_front
# import Project.cli as ui
# from tkinter.messagebox import showerror
import sqlite3
from tkinter import messagebox

import paho.mqtt.client as mqtt
from tkinter.simpledialog import askstring
import time
import tkinter

# The broker name or IP address.
broker = "LAPTOP-S89GAF8M"
port = 8883
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()
# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()

def call_worker(worker_name, worker_guid, terminal_id):
    client.publish("worker/name", worker_name + "." + worker_guid+"." + terminal_id, )


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8")))
    messagebox.showinfo("Message from the Server", message_decoded)

def create_main_window(user,guid):
    window.geometry("170x130")
    window.title("SENDER")

    intro_label = tkinter.Label(window, text="Connected employee:")
    intro_label.grid(row=0, column=0)
    Label_User = tkinter.Label(window, text=str((user[1] + " " + user[2])))
    Label_User.grid(row=1, column=0)
    button_1 = tkinter.Button(window, text="Do Something",
                              command=lambda: call_worker(str(user[1]) + " " + str(user[2]), str(user[0]), guid))
    button_1.grid(row=2, column=0)
    button_stop = tkinter.Button(window, text="QUIT", command=window.quit)
    button_stop.grid(row=4, column=0)


def login_window():
    GUID = askstring("Terminal Guid Check:", "Enter Terminal GUID")
    con = sqlite3.connect('client_db.db')
    cur = con.cursor()
    cur.execute("""SELECT worker_guid, First_Name, Surname  
                                        FROM workers """)
    user = cur.fetchall()
    cur.execute("select terminal_id  from terminals")
    data = cur.fetchall()
    RFID = ""
    i = 0
    Existing = False
    Existing_worker = False
    for item in data:
        if item[i] == GUID:
            Existing = True
            RFID = askstring("Scanning Card", "Please scan your RFID Card")
            cur.execute("select worker_guid  from workers")
            data = cur.fetchall()
            j = 0
            for items in data:
                if int(items[j]) == int(RFID) | int(items[j]) == int(RFID):
                    Existing_worker = True
                    loggedIndex = 0
                    for el in range(len(user)):
                        index2 = 0
                        if user[el][index2] == int(RFID):
                            loggedIndex = el
                            index2 += 1
                    connect_to_broker(RFID, GUID)
                    print(time.ctime() + " : " + str(user[loggedIndex][0]) + " " + str(user[loggedIndex][1]) +
                          " " + str(user[loggedIndex][2]) + " connected !")
                    create_main_window(user[loggedIndex], GUID)
                    window.mainloop()
                    disconnect_from_broker(RFID, GUID)
                    print(time.ctime() + " : " + str(user[loggedIndex][0]) + " " + str(user[loggedIndex][1]) +
                          " " + str(user[loggedIndex][2]) + " Disconnected !")

    if (not Existing_worker) & Existing:
        print("Non Existing Worker saved " + RFID)
        connect_to_broker(RFID, GUID)
        unknown = [RFID, "unknown ", ""]
        create_main_window(unknown, GUID)
        window.mainloop()
        disconnect_from_broker(RFID, GUID)
        print(time.ctime() + " : " + str(unknown[0]) + " " + str(unknown[1]) +
              " " + str(unknown[2]) + " Disconnected !")
    if not Existing:
        print("Non Existing Terminal " + RFID)
    else:
        exit(0)


def connect_to_broker(worker_guid, guid):
    # Setting TLS
    client.tls_set("ca.crt")  # provide path to certification
    # Authenticate
    client.username_pw_set(username='client', password='password')

    # Connect to the broker.
    client.connect(broker, port)  # modify connect call by adding port

    # Send message about connection.
    client.on_message = process_message
    # Send message about connection.
    client.subscribe("server/name")
    call_worker("Client connected", worker_guid, guid)


def disconnect_from_broker(worker_guid, guid):
    # Send message about disconnection.
    call_worker("Client disconnected", worker_guid, guid)
    # Disconnect the client.
    client.disconnect()


def run_sender():
    # Call the login window
    login_window()


if __name__ == "__main__":
    run_sender()