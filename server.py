#!/usr/bin/env python3
import socket



SERVER_ADDRESS = '127.0.0.1'

SERVER_PORT = 22224

sock_listen = socket.socket()

sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))

sock_listen.listen(5)

print("Server in ascolto su %s." % str((SERVER_ADDRESS, SERVER_PORT)))


while True:
    sock_service, addr_client = sock_listen.accept()
    print("\nConnessione ricevuta da " + str(addr_client))
    print("\nAspetto di ricevere i dati ")
    while True:
        dati = sock_service.recv(2048)
        if not dati:
            print("Fine dati dal client. Reset")
            break
        
        dati = dati.decode()#decodifichiamo da file binario a file testo
        print("Ricevuto: '%s'" % dati)
        if dati=='0':
            print("Chiudo la connessione con " + str(addr_client))
            break

        op, num1, num2 = dati.split(";")#assegna a 3 variabili i tre valori separati dal punto e virgola nella variabile dati
        #dobbiamo trasformare in float le variabili che sono stringhe per svolgere le operazioni
        if(op == "più"):
            print(float(num1) + float(num2))
        elif(op == "meno"):
            print(float(num1) - float(num2))
        elif(op == "per"):
            print(float(num1) * float(num2))
        elif(op == "diviso"):
            print(float(num1) / float(num2))

        dati = dati.encode()#trasformiamo ancora in file binario per ri-inviarlo al client

        sock_service.send(dati)

sock_service.close()