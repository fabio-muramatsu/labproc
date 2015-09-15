#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import mfrc522.MFRC522 as MFRC522
import signal
import json
from util import *


TYPE_ADMIN = 'admin'
TYPE_USER = 'user'

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

id_file = open("ids.txt")
ids = json.loads(id_file.read())
#{tag_id: [password, account type]}

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        uid_str = '.'.join([str(id_byte).zfill(3) for id_byte in uid[:4]])
        print "Card id: " + uid_str

        if uid_str in ids:
            print "Digite a senha: "
            senha = read_input()
            if senha == ids[uid_str][0]:
                print "{} autenticado".format(ids[uid_str][1])
            else:
                print "Senha incorreta"
        else:
            print "Cartão não cadastrado"



