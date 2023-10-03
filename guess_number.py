import socket
import random

IP = 'localhost'
PORT = 2000
number_to_guess = random.randrange(1, 9)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
    socket_server.bind((IP, PORT))
    socket_server.listen()
    print("Listening...")
    print(f"Number to guess: {number_to_guess}")

    (cli, add) = socket_server.accept()
    print(f"Client connected at: {add}")

    cli.send(b"Try to guess my number [1-9]! \n")
    cli.send(b"\rENTER or ESC to quit\n")

    while True:
        data = cli.recv(64).decode()
        print(f"{data}")
        if int(data) == number_to_guess:
            cli.send(b"\r\nYou made it!\n")
            break
        elif int(data) > number_to_guess:
            cli.send(b"\r\nMy number is less \n")
        elif int(data) < number_to_guess:
            cli.send(b"\r\nMy number is higher \n")
    cli.close()
