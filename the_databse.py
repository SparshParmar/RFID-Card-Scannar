#!/usr/bin/env python3
import s_backend as server_back
import sqlite3
import time
import os


def insertT(x, y, z):
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO terminals VALUES (?,?,?)",
                   (x, y, z))
    cursor.close()
    connection.commit()
    connection.close()


def insertW(x, y, z, t):
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO workers VALUES (?,?,?,?)",
                   (x, y, z,t))
    cursor.close()
    connection.commit()
    connection.close()


def deleteT(y):
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    query = """Delete from terminals where terminals.terminal_id = ?"""
    cursor.execute(query, (y,))
    cursor.close()
    connection.commit()
    connection.close()


def deleteW(y):
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    query = """Delete from workers where workers.worker_guid = ?"""
    cursor.execute(query, (y,))
    cursor.close()
    connection.commit()
    connection.close()


def add_card(guid, card):
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    query = """UPDATE workers SET Card_guid = ? where workers.worker_guid = ?"""
    cursor.execute(query, (card, guid,))
    cursor.close()
    connection.commit()
    connection.close()


def remove_card(card):
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    query = """UPDATE workers SET Card_guid = NULL where workers.card_guid = ?"""
    cursor.execute(query, (card,))
    cursor.close()
    connection.commit()
    connection.close()


def print_report(guid):
    server_back.print_report(guid)


def create_db():
    if os.path.exists("client_db.db"):
        os.remove("client_db.db")
        print("Old database removed.")
    connection = sqlite3.connect("client_db.db")
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE workers_log (
        log_time text,
        worker text,
        worker_guid INTEGER,
        terminal_id text
    )""")
    cursor.execute(""" CREATE TABLE terminals(
           Time text,
           terminal_name text,
           terminal_id text
       )""")
    cursor.execute(""" CREATE TABLE workers(
        worker_guid INTEGER ,
        First_Name text,
        Surname text,
        Card_guid INTEGER 
          )""")

    # defaults terminals created
    insertT(time.ctime(), "Galeria Dominikanska", "T1")
    insertT(time.ctime(), "Pasaz Grunwaldzki", "T2")
    insertT(time.ctime(), "Politechnika Wroclawska", "T3")

    insertW("1", "Sparsh", " Parmar", 101)
    insertW("2", "Nayan", " Bhatt", 102)
    insertW("3", "Yashvi", " shah", 103)
    
    cursor.close()
    connection.commit()
    connection.close()
    print("The new database created.")


if __name__ == "__main__":
    create_db()
