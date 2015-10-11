#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import mfrc522.MFRC522 as MFRC522
import signal
import json, time
from display import i2c_lcd
from util import write_display, read_input

TYPE_ADMIN = 'admin'
TYPE_USER = 'user'

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

if __name__ == "__main__":

    #Init display
    lcd = i2c_lcd(0x27,1, 2, 1, 0, 4, 5, 6, 7, 3)
    lcd.backLightOn()
    lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)

    continue_reading = True
    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    id_file = open("ids.txt")
    ids = json.loads(id_file.read())
    #{tag_id: [password, account type]}
    id_file.close()

    write_display(lcd, "Aproxime o cartao")
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

            #Se o ID lido consta no banco de dados, solicita a senha
            if uid_str in ids: 
                write_display(lcd, "Digite a senha: ")
                lcd.setPosition(2,0)
                password = read_input(lcd)
                #Se a senha digitada corresponde ao cartão, checa o tipo de usuário
                if password == ids[uid_str][0]:
                    print "{} autenticado".format(ids[uid_str][1])

                    #Usuário comum
                    if ids[uid_str][1] == TYPE_USER:
                        write_display(lcd, "Autorizado")
                        #Sinal de abertura
                        time.sleep(1)

                        write_display(lcd, "Aproxime o cartao")

                    #Administrador
                    elif ids[uid_str][1] == TYPE_ADMIN:
                        write_display(lcd, "admin")
                        #Cadsastro de novo cartão

                        time.sleep(1)
                        write_display(lcd, "Aproxime o cartao")

                #Se a senha digitada for incorreta, notifica o usuário, e aguarda nova leitura        
                else:
                    write_display(lcd, "Senha incorreta")
                    time.sleep(3)
                    write_display(lcd, "Aproxime o cartao")
            
            #Se o cartão apresentado não for reconhecido, notifica o usuário e aguarda nova leitura
            else:
                write_display(lcd, "Cartao nao cadastrado")
                time.sleep(3)
                write_display(lcd, "Aproxime o cartao")



