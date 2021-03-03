import socket
import sys
import random
import os
import time
import threading
import multiprocessing

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224
NUM_WORKERS=15

def genera_richieste(address,port):
    start_time_thread= time.time()
    print(f"Client PID: {os.getpid()}, Process Name: {multiprocessing.current_process().name}, Thread Name: {threading.current_thread().name}")
    try:
        s=socket.socket()
        s.connect((address,port)) #connette il socket al server
        print(f"{threading.current_thread().name} Connessione al server: {address}:{port}")
    except s.error as errore: # se c'è un errore esegue:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n{errore}")
        sys.exit() #esce dal programma
    comandi=['piu','meno','per','diviso']
    operazione=comandi[random.randint(0,3)]
    dati=str(operazione)+";"+str(random.randint(1,100))+";"+str(random.randint(1,100))
    dati=dati.encode() #traduce la stringa in una lista di byte
    s.send(dati) #manda dati codificati al server 
    dati=s.recv(2048) #legge risposta del server
    if not dati:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    dati=dati.decode() 
    print(f"{threading.current_thread().name}: Ricevuto dal server:")
    print(dati + '\n')
    dati="ko" #se non c'è risposta
    dati=dati.encode()
    s.send(dati)
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} execution time=", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time=time.time()
    for _ in range (0,NUM_WORKERS):
        genera_richieste(SERVER_ADDRESS, SERVER_PORT) #funzione in serie una dopo l'altra
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time) #tempo impiegato

    start_time=time.time()
    threads=[threading.Thread(target=genera_richieste, args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)] #lista di Thread
    [thread.start() for thread in threads] #avvia tutti i Thread
    [thread.join() for thread in threads] #aspetta che tutti i Thread abbiano finito
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    processes =[multiprocessing.Process(target=genera_richieste, args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [process.start() for process in processes]
    [process.join() for process in processes]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)