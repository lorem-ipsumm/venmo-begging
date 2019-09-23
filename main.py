import requests
import os
import time
# import email_config
# import imaplib
# import email
# import base64
import sys
import json

# amount to charge people
AMOUNT = None

# message to send
MESSAGE = None

# number of charges sent per run
CHARGE_COUNT = 0

# amount charged per run
AMOUNT_CHARGED = 0


def send_charge(target):

    # use global variables
    global AMOUNT, MESSAGE, CHARGE_COUNT, AMOUNT_CHARGED

    # start of command
    base = 'venmo charge @'

    # message to send to target
    # message = ' "it\'s your lucky day"'

    # construct command
    command = (base + target + " " + str(AMOUNT) + " \"" + MESSAGE + "\"")

    # increment charge count
    CHARGE_COUNT = CHARGE_COUNT + 1

    # calculate total amount charged
    AMOUNT_CHARGED = CHARGE_COUNT * AMOUNT

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
                    time.sleep(1)

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


def handle_arguments():

    # use global variables
    global AMOUNT, MESSAGE

    # check num of arguments
    if (len(sys.argv) < 3):
        print("usage: main.py [charge_amount] [message]\n")
        sys.exit()

    # check to see if first argument is a num
    try:
        # attempt to set amount
        AMOUNT = float(sys.argv[1])
    except ValueError:
        # user didn't pass number
        print("first argument must be a number\n")

        # exit
        sys.exit()

    # set the message
    MESSAGE = sys.argv[2]


def update_config():

    # open config file
    with open('config.json', "r+") as config:

        # load config data
        data = json.load(config)

        # get the number of charges
        # config_count = data["charge_count"]

        # seek to beginning of file before truncate
        config.seek(0)

        # get the old charge count
        old_charge_count = data['data'][0]['charge_count']

        # get amount charged
        old_amount_charged = data['data'][0]['amount_charged']

        # update values
        data['data'][0]['charge_count'] = old_charge_count + CHARGE_COUNT
        data['data'][0]['amount_charged'] = old_amount_charged + AMOUNT_CHARGED

        # clear file
        config.truncate(0)

        # data = {}
        # data["charge_count"] = 5
        # data["data"].append({})

        # output file
        json.dump(data, config, ensure_ascii=True, indent=4)


# program start
handle_arguments()
start()
update_config()


'''
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_config.email, email_config.password)
mail.select()

typ, msg_numbers = mail.search(None, 'ALL')

for num in msg_numbers[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    print(data)
    # data1 = base64.b64decode(data[0][1])
    # print('message %s\n%s\n' %(num, data1))
'''
