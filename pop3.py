import socket
import ssl
import getpass

##Класс FTP клиента
class FTPClient:
    def __init__(self):
        self.socket = None ## Инициализация
        self.datasock = None
     ## Функция подключения к серверу
    def connect(self, server, port=21):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## создается сокет для передачи данных с использованием протокола TCP
        self.socket.connect((server, port))


    def connect_datasock(self, server, port):
        self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.datasock.connect((server, port))  ## Устанавливаем соединение с сервером через 21 порт

    ## Функция отправки команд на сервер
    def send_command(self, command):
        self.socket.send(command.encode())

     ## Функция авторизации пользователя
    def authenticate(self):
        username = input("Username:")  ## Считываем с клавиатуры имя пользователя
        usernameCommand = "USER " + username + '\r\n'  ## Формируем команду для отправки на сервер
        self.send_command(usernameCommand)  ## Отправляем имя пользователя на сервер
        recv = self.get_response()  ## Получаем ответ от сервера
        print(recv)  ## Печатаем ответ от сервера на экране
        if '331' in recv:  ## Если в ответе содержится 331, то выполнить следующие действия
            password = getpass.getpass("Password:")  ## Считываем с клавиатуры пароль
            passwordCommand = "PASS " + password + '\r\n'  ## Формируем команду для отправки на сервер
            self.send_command(passwordCommand) ## Отправляем пароль на сервер
            recv = self.get_response() ## Получаем ответ от сервера
            print(recv)  ## Печатаем ответ от сервера на экране
            if '230' in recv: ## Если в ответе сервера содержится 230, то продолжить работу
                return True
            elif '530' in recv:
                print ("Wrong login or password. Try again.\n")
                return self.authenticate()
    ## Функция получения ответа от сервера

    def get_response(self):
        recv = self.socket.recv(1024).decode()
        return recv

    def get_response_ds(self):
        recv = self.datasock.recv(1024).decode()
        return recv

def main():
    ftp = FTPClient() ## Создаем экземпляр класса клиента
    ftp.connect('localhost') ## Подключаемся к локальному серверу FTP


    recv = ftp.get_response() ## Получаем ответ сервера
    print(recv) ## Печатаем ответ сервера на экране

    ## Если пользователь авторизовался
    if ftp.authenticate():
        while True:
            inputCommand = input("Send command: ") + '\r\n' ## Ввод команды с клавиатуры
            ftp.send_command(inputCommand) ## Отправка команды
            recv = ftp.get_response() ## Получение ответа от сервера
            print(recv)
            if '227' in recv:
                recv = recv[27:-4].split(sep=',')
                port = (int(recv[-2])) * 256 + (int(recv[-1]))
                ftp.connect_datasock('localhost', port)
                try:
                    with open('text.txt', 'r') as file:
                        for line in file.readlines():
                            ftp.datasock.send(line.encode())
                    file.close()
                except FileNotFoundError:
                    open('text.txt', 'w').write('')
                data_response = ftp.datasock.recv(1024).decode()
                if data_response:
                    print(data_response)
                ftp.datasock.close()
             ## Печать ответа сервера на экране


if __name__ == "__main__":
    main()