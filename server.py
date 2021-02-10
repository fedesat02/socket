#!/usr/bin/env python3
import socket


#lasciando il campo vuoto sarebbe la stessa cosa (localhost)
SERVER_ADDRESS = '127.0.0.1'
#numero di porta, deve essere <1024 perchè le altre sono riservate.
SERVER_PORT = 22224
#la funzione avvia_server crea un endpoint di ascolto(sock_listen) dal quale accettare connessioni in entrata
#la socket di ascolto viene passata alla funzione ricevi_comandi la quale accetta richieste di connessione
#e per ognuna crea una socket per i dati(sock_service) da cui ricevere le richieste e inviare le proposte
def ricevi_comandi(sock_listen):

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
                ris = str(float(num1) + float(num2))
            elif(op == "meno"):
                ris = str(float(num1) - float(num2))
            elif(op == "per"):
                ris = str(float(num1) * float(num2))
            elif(op == "diviso"):#if per assicurarsi che sia possibile la divisione
                if float(num2) == 0:
                    ris = "GNE GNE GNE"
                else:
                    ris = str(float(num1) / float(num2))

            ris = ris.encode()#trasformiamo ancora in file binario per ri-inviarlo al client

            sock_service.send(ris)

    sock_service.close()

def avvia_server(indirizzo, porta):

    sock_listen = socket.socket()

    sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))

    sock_listen.listen(5)

    print("Server in ascolto su %s." % str((SERVER_ADDRESS, SERVER_PORT)))

    ricevi_comandi(sock_listen)




if __name__ == '__main__':
    avvia_server(SERVER_ADDRESS, SERVER_PORT)