#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import mfrc522.MFRC522 as MFRC522
import signal, datetime
import json, time, threading, Queue
from display import i2c_lcd
from util import write_display, read_input, notification_daemon

TYPE_ADMIN = 'admin'
TYPE_USER = 'user'

#Objeto timer definido em escopo global
t = None

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

#Escreve as opções do administrador
def write_admin_options(options_set, lcd):
    global t

    if options_set == 0:
        lcd.clear()
        lcd.writeString('Digite a opcao:')

    if options_set%2 == 0:
        lcd.setPosition(2,0)
        lcd.writeString('1:Cadastrar us.')
    if options_set%2 == 1:
        lcd.setPosition(2,0)
        lcd.writeString('2: Remover us. ')

    t = threading.Timer(2, write_admin_options, args=((options_set+1),lcd))
    t.start()

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

    # Lê credenciais dos usuários
    #{tag_id: [password, account type, CPF, panic_password]}
    id_file = open("ids.txt")
    ids = json.loads(id_file.read())
    id_file.close()

    # Lê os destinatários das mensagens de emergência
    to_list = []
    notification_dest_file = open("notification_dest.txt", "r")
    for dest in notification_dest_file:
        to_list.append(dest)
    notification_dest_file.close()
    #Inicia o thread de envio de notificações
    q = Queue.Queue(10)
    bot_token = "132003418:AAH1QdnJyhVmOVY3_MJ4hKD1fqm_2ABocag"
    notification_thread = threading.Thread(target = notification_daemon, args=(bot_token, q, to_list))
    notification_thread.start()

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
                        t = threading.Timer(2, write_admin_options, args=(0,lcd))
                        t.start()
                        option = input()
                        t.cancel()

                        if option == 1:
                            write_display (lcd,'Aproxime novo cartao')
                            read_new_card = False
                            while not read_new_card:
                                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL) 
                                if status == MIFAREReader.MI_OK: 
                                    (status,uid) = MIFAREReader.MFRC522_Anticoll() 
                                    if status == MIFAREReader.MI_OK: 
                                        read_new_card = True
                                        uid_str = '.'.join([str(id_byte).zfill(3) for id_byte in uid[:4]]) #pega ID do novo cartao
                                        if uid_str in ids:
                                            write_display(lcd,"Cartao ja cadastrado")
                                            break
                                        write_display (lcd,'Digite nova senha: ')
                                        senha = raw_input()
                                        time.sleep(1)
                                        write_display (lcd,'Digite de novo a senha: ')
                                        senha2 = raw_input()
                                        if(senha == senha2): #checagem para evitar erros
                                            write_display (lcd,'Digite seu CPF')
                                            cpf = raw_input()
                                            ids.update({uid_str:(str(senha),TYPE_USER,cpf)}) #cadastra no dict
                                            id_file = open("ids.txt","w")
                                            json.dump(ids,id_file) #atualiza arquivo com novo objeto JSON
                                            print ids
                                            write_display (lcd,'Cadastro realizado.')
                                        else:
                                            write_display (lcd,'Falha no cadastro.')
                        elif option == 2:
                            write_display(lcd,'Digite CPF a ser removido')
                            cpf = raw_input()
                            flag = 0
                            for key in ids: #varre dicionario
                                if ids[key][1] == 'user' and (ids[key][2]==cpf): #deleta entrada correspondente a esse cpf
                                    flag= key #achou
                                    break
                            if(flag):
                                del ids[flag]
                                id_file = open("ids.txt","w")
                                json.dump(ids,id_file) #atualiza arquivo com novo objeto JSON
                                write_display (lcd,'Registros Atualizados')
                            else:
                                write_display (lcd,'CPF não encontrado')
                        else:
                            write_display(lcd,'Opcao inexistente')

                        time.sleep(1)
                        write_display(lcd, "Aproxime o cartao")

                #Se a senha digitada for incorreta, notifica o usuário, e aguarda nova leitura        
                else:
                    #FIXME: simular senha de pânico como sendo uma senha incorreta
                    msg = "{} - Senha de pânico inserida - CPF: {}".format(
                        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ids[uid_str][2])
                    q.put(msg)
                    write_display(lcd, "Senha incorreta")
                    time.sleep(3)
                    write_display(lcd, "Aproxime o cartao")
            
            #Se o cartão apresentado não for reconhecido, notifica o usuário e aguarda nova leitura
            else:
                write_display(lcd, "Cartao nao cadastrado")
                time.sleep(3)
                write_display(lcd, "Aproxime o cartao")



