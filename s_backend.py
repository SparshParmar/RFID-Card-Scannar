#!/usr/bin/env python3
import sqlite3
import tkinter
from tkinter import messagebox

import paho.mqtt.client as mqtt
import time

# The broker name or IP address.
broker = "LAPTOP-S89GAF8M"
port = 8883
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()


def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    messagebox.showinfo("Message from the Server", message_decoded)
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    # Print message to console.
    if message_decoded[0] != "Client connected" and message_decoded[0] != "Client disconnected":
        print(time.ctime() + ", " + message_decoded[0] + " used the RFID card.")
        # Save to sqlite database.
        cursor.execute("INSERT INTO workers_log VALUES (?,?,?,?)",
                       (time.ctime(), message_decoded[0], message_decoded[1], message_decoded[2]))

    if message_decoded[0] == "Client connected" or message_decoded[0] == "Client disconnected":
        print(message_decoded[0] + " : " + message_decoded[1] + " on " + message_decoded[2])
        # Save to sqlite database.
        cursor.execute("INSERT INTO workers_log VALUES (?,?,?,?)",
                       (time.ctime(), message_decoded[0], message_decoded[1], message_decoded[2]))
    connection.commit()
    connection.close()


def print_report(guid):
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM workers_log where workers_log.worker_guid=? """, (int(guid),))
    log_entrys = cursor.fetchall()
    # print(log_entrys)
    labels_log_entry = []
    print_log_window = tkinter.Tk()
    for log_entry in log_entrys:
        labels_log_entry.append(tkinter.Label(print_log_window, text=(
                "On %s, %s: %s used the terminal  %s" % (log_entry[0], log_entry[1], log_entry[2], log_entry[3]))))
    for label in labels_log_entry:
        label.pack(side="top")
    connection.commit()
    connection.close()
    # Display this window.
    print_log_window.mainloop()


def print_log_to_window():
    connetion = sqlite3.connect("client_db.db")
    cursor = connetion.cursor()
    cursor.execute("SELECT * FROM workers_log")
    log_entrys = cursor.fetchall()
    labels_log_entry = []
    print_log_window = tkinter.Tk()

    for log_entry in log_entrys:
        labels_log_entry.append(tkinter.Label(print_log_window, text=(
                "On %s, %s: %s used the terminal %s" % (log_entry[0], log_entry[1], log_entry[2], log_entry[3]))))

    for label in labels_log_entry:
        label.pack(side="top")

    connetion.commit()
    connetion.close()

    # Display this window.
    print_log_window.mainloop()


def connect_to_broker():
    # Setting TLS
    client.tls_set("ca.crt")  # provide path to certification
    # Authenticate
    client.username_pw_set(username='client', password='password')
    # Connect to the broker.
    client.connect(broker, port)  # modify connect call by adding port

    # Send message about connection.
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("worker/name")


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()


if __name__ == "__main__":
    run_receiver()
