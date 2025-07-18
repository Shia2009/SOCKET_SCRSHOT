import socket
from datetime import datetime
import os


port=int(input("Enter the PORT --> "))

host="192.168.56.1"
adr_list=[]
print(f'Server listen on {host}:{port} \t {datetime.now().strftime("%H:%M:%S")}')
server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
listen=int(input("how many sockets to listen to -->"))
server_socket.listen(listen)
print(f"Server listen to {listen} sockets \t {datetime.now().strftime("%H:%M:%S")}")
conn, adr = server_socket.accept()
adr_list.append(adr)
print(f"Get new connection from --> {adr} \t {datetime.now().strftime("%H:%M:%S")}")

def server_program():
    print(adr_list)
    message = input(f"command for {adr} --> ")  # что отправить
    try:
        adr_send=input('Enter the ADDRESS to whom to send --> ')
        port_send=int(input('Enter the PORT to whom to send --> '))
        target_url=(adr_send, port_send)#кому отправить
        conn.sendto(message.encode(), target_url)#отправляем
    except Exception as e:
        print(f"error : [{e}]\t {datetime.now().strftime("%H:%M:%S")}")
    if message=='photo':
        try:
            file = open('server_11.jpg', "wb")
            image_chunk = conn.recv(100000000)  # stream-based protocol
            print('Photo saved')
            while image_chunk:
                file.write(image_chunk)
                image_chunk = conn.recv(100000000)
            file.close()
            print('file_close')
        except Exception as e:
            print(f'ERROR {e}')


if __name__=="__main__":
    while True:
        server_program()
    conn.close()