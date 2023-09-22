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

    cli.send(b"Try to guess my number! ")
    while True:
        data = cli.recv(64).decode()
        print(data)
        if int(data) == number_to_guess:
            cli.send(b"You made it!")
            break
        elif int(data) > number_to_guess:
            cli.send(b"My number is less ")
        elif int(data) < number_to_guess:
            cli.send(b"My number is higher ")
    cli.close()
