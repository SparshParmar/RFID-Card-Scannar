# from Project import *
import client_mixed as client
import the_databse as create_db
import s_frontend as server_front


def choose_client_or_server():
    """
    Function for choosing which kind of application we want to run: client or server
    """
    options = "Choose application mode:\n 1) Client \n 2) Server"

    while True:
        print("""Choose application mode:
                     1) Client 
                     2) Server""")
        chosen = input("Your choice: ")
        print("___________________________________________________________________________________")
        if chosen == "1":
           client.run_sender()
        elif chosen == "2":
            server_front.run_receiver()
        else:
            print("Incorrect choice. Try again")
            print("___________________________________________________________________________________")

if __name__ == "__main__":
    create_db.create_db()

    # server_back.
    choose_client_or_server()
