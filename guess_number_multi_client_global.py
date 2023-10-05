import socket
import random
import threading

number_to_guess = random.randrange(1, 9)
stop_threads = False
thread_name = ""


def client_driver(cl, ad, ev: threading.Event):
    global stop_threads
    global thread_name
    data = f"Connected with {ad}\n"
    cl.send(data.encode())
    cl.send(b"Try to guess my number [1-9]! \n")
    cl.send(b"\rENTER or ESC to quit\n")

    while True :
        # print(f"Por fuera: {ev.is_set()}")
        if stop_threads:
            print(f"Adentro: {ev.is_set()}")
            resolved_by = f"Already resolved by: {thread_name}\n"
            cl.send(resolved_by.encode())
            break
        data = cl.recv(64).decode()
        print(f"{data}")
        if int(data) == number_to_guess:
            cl.send(b"\r\nYou made it!\n")
            ev.set()
            stop_threads = True
            thread_name = threading.current_thread().name
            break
        elif int(data) > number_to_guess:
            cl.send(b"\r\nMy number is less \n")
        elif int(data) < number_to_guess:
            cl.send(b"\r\nMy number is higher \n")
    cl.close()


if __name__ == '__main__':
    IP = 'localhost'
    PORT = 2000
    ev = threading.Event()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((IP, PORT))
        socket_server.listen()
        print("Listening...")
        print(f"Number to guess: {number_to_guess}")

        while True:
            (cli, add) = socket_server.accept()
            # print(f"Client connected at: {add}")
            # new thread for each new connection
            th = threading.Thread(target=client_driver, args=(cli, add, ev))
            th.name = add
            th.start()
