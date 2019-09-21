import requests
import os
import time

# amount to charge people
# this is subject to change:
amount = 0.25


def send_charge(target):

    # use global amount varaible
    global amount

    # start of command
    base = 'venmo charge @'

    # message to send to target
    message = ' "social experiment"'

    command = (base + target + " " + str(amount) + message)

    # print(target)
    # execute terminal command
    os.system(command)
    # print(command)


def get_transactions(history, data):

    # iterate through transactions
    for transaction in data:

        # get the 'actor' of the transaction
        # actor = transaction["actor"]["username"]

        # grab the transaction type
        trans_type = transaction["type"]

        # create target variable
        target = None

        # check the history file
        with open('history') as history_file:

            # check if the type is payment or charge
            if trans_type == "payment":
                # set target to the recipient
                target = transaction["transactions"][0]["target"]["username"]

                # add the actor to the history file
                history.write(target)

                # check if the target is in the history file
                if target not in history_file.read():

                    # send the charge
                    send_charge(target)

                    # sleep for a bit to not blow up the API
                    time.sleep(5)

            elif trans_type == "charge":
                # don't deal with charges
                # because we don't know if the payment
                # was completed
                continue


def start():

    # it's show time
    os.system("notify-send 'commencing digital-age begging'")

    # get the venmo public api url
    url = 'https://venmo.com/api/v5/public'

    # make a request
    resp = requests.get(url=url)

    # get the json data
    data = resp.json()["data"]

    # open the charge history file for read/write
    history = open("history", "a+")

    # get the transactions
    get_transactions(history, data)

    # close the history file
    history.close()


# begin the program
start()
