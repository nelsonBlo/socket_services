import socket
import random
import threading

number_to_guess = random.randrange(1, 9)
thread_name = ""


def client_driver(cl, ad, ev):
    global thread_name
    message = f"Connected with {ad}\n"
    cl.send(message.encode())
    cl.send(b"Try to guess my number [1-9]! \n")
    cl.send(b"\rENTER or ESC to quit\n")

    while not ev.is_set():
        data = cl.recv(64).decode()
        print(f"{data}")
        if int(data) == number_to_guess:
            message = f"\r\n\nYOU MADE IT!! My number was {number_to_guess}\n"
            cl.send(message.encode())
            ev.set()
            thread_name = threading.current_thread().name
            cl.close()
        elif int(data) > number_to_guess and not ev.is_set():
            cl.send(b"\r\nMy number is less \n")
        elif int(data) < number_to_guess and not ev.is_set():
            cl.send(b"\r\nMy number is higher \n")
    try:
        if ev.is_set():
            resolved_by = f"\nThe number was {number_to_guess} and it was already resolved by: {thread_name}\n"
            cl.send(resolved_by.encode())
            cl.close()
    except:
        pass


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
            ev.clear()
