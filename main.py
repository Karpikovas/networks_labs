from socket import *
import threading
import sys
import getpass


class FTPClient:
    def __init__(self):
        self.IP = 'localhost'
        self.port = 21
        self.socket = socket()
        self.socket.connect((self.IP, self.port))
        self.recv = self.socket.recv(10000).decode()
        self.datarecv = None
        print(self.recv)

    def authenticate(self):
        username = input("Username:") 
        usernameCommand = "USER " + username + '\r\n'  
        self.socket.send(usernameCommand.encode())  
        self.recv = self.socket.recv(10000).decode()  
        print(self.recv)  
        if '331' in self.recv:  
            password = getpass.getpass("Password:")  
            passwordCommand = "PASS " + password + '\r\n'  ## Формируем команду для отправки на сервер
            self.socket.send(passwordCommand.encode()) ## Отправляем пароль на сервер
            self.recv = self.socket.recv(10000).decode()  ## Получаем ответ от сервера
            print(self.recv)  ## Печатаем ответ от сервера на экране
            if '230' in self.recv: ## Если в ответе сервера содержится 230, то продолжить работу
                return True
            elif '530' in self.recv:
                print ("Wrong login or password. Try again.\n")
                return self.authenticate()

    def datasocket(self, ip, port):
        while True:
            try:
                datasocket = socket()
                datasocket.connect((ip, port))
                try:
                    with open('test.txt', 'r') as file:
                        for line in file.readlines():
                            datasocket.send(line.encode())
                    file.close()
                except FileNotFoundError:
                    open('test.txt', 'w').write('')
                self.datarecv = datasocket.recv(10000).decode()

                if self.datarecv:
                    print(self.datarecv)
                    self.datarecv = ''
                datasocket.close()
            except ConnectionRefusedError:
                pass

    def send(self, command):
        self.socket.send(command.encode())
        self.recv = self.socket.recv(10000).decode()
        print(self.recv)

        if '227' in self.recv:
            self.recv = self.recv[27:-4].split(sep=',')
            port = (int(self.recv[-2])) * 256 + (int(self.recv[-1]))
            print (port)
            try:
                threading.Thread(target=self.datasocket, args=(self.IP, port)).start()
            except ConnectionRefusedError:
                pass


if __name__ == '__main__':
    ftp = FTPClient()
    ftp.authenticate()
    while True:
        inputCommand = input("Send command: ") + '\r\n'
        ftp.send(inputCommand)
