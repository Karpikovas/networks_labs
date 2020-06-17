"""Общий алгоритм:
    1. Создаем маску согласно шаблонам класса А, В, С
    2. Дополняем шаблон маски согласно введенным данным (функция set_mask)
            При формировании шаблона маски определенного класса мы указываем количество свободных бит.
            CISCO формула - 2^n = кол-во подсетей, n - количество выделенных бит
            По введенным значениям M и N, вычисляем количество выделенных бит и их сумму сравниваем со 
            свободными. Сумма не должна превышать количество свободных бит
    3. Мы нашли количество выделенных бит nbeat, по таблице выбираем согласно количеству бит число и формируем
    маску
    4. Вызываем функцию получения диапазона IP адресов (get_all_ip)

"""
class Mask:
    """Конструктор класса"""
    def __init__(self, ipclass, n, m):
        self.ipclass = ipclass.upper() #Один из классов А,В,С
        self.id = None #id необходим для формирования маски
        self.n = int(n) 
        self.nbeat = 0 
        self.m = int(m)
        self.mbeat = 0 
        self.mask = None
        self.freebeats = None #свободные биты в маске
        self.variables = [128, 192, 224, 240, 248, 252, 254, 255] #таблица значений для формирования маски
        self.address = [192, 168, 1, 0] #пример адреса, который будем разбивать
        self.minaddress = [0, 0, 0, 0] 
        self.maxaddress = [0, 0, 0, 0]
        self.wildcard = [0, 0, 0, 0] #обратная маска


    def create_mask(self):
        """Создаем шаблон маски согласно выбранного класса"""

        if self.ipclass == 'A':
            self.mask = [255, 0, 0, 0]
            self.freebeats = 24
            self.id = 1
        elif self.ipclass == 'B':
            self.mask = [255, 255, 0, 0]
            self.freebeats = 16
            self.id = 2
        elif self.ipclass == 'C':
            self.mask = [255, 255, 255, 0]
            self.freebeats = 8
            self.id = 3
        self.set_mask()

    def set_mask(self):
        """Находим количество занятых бит под порцию хоста"""
        i = 1
        while i < self.n:
            i *= 2
            self.nbeat += 1
        i = 1
        """Находим количество оставшихся бит"""
        while i < self.m:
            i *= 2
            self.mbeat += 1
        """Сравниваем со значением, которое должно быть, если превышает, то создать маску
        невозможно
        """
        if (self.nbeat + self.mbeat > self.freebeats):
            print("Impossible")
            return
        """Создаем маску, используя подготовленные шаблоны из таблицы variables и выводим ее
        на экран
        """
        while (self.nbeat != 0):
            self.mask[self.id] = self.variables[self.nbeat - 1]
            self.freebeats -= self.nbeat
            self.nbeat = 0;
        print('Mask: {0}'.format(str(self.mask)[1:len(str(self.mask))-1].replace(',','.')))
        self.get_all_ip()

    def get_all_ip(self):
        """В цикле формируем обратную маску, минимальный и максимальный адреса,
        в качестве минимального выбираем следующий за ним адрес, а в качестве максимального предпоследний,
        т.к. первый и полседний адреса нельзя использовать в силу их специального значения IP-адресов
        (Первый адрес - сетевой адрес, последний - широковещательный адрес)
        """
        for i in range(4):
            self.minaddress[i] = self.mask[i] & self.address[i] #поразрядная конъюнкция адреса и маски
                                                                #формирование минимального адреса
            self.wildcard[i] = ~self.mask[i] + 256 #формаирования обратной маски путем инверсии
            self.maxaddress[i] = self.minaddress[i] | self.wildcard[i] #дизъюнкция с обратной маской
                                                                        #формирование максимального адреса
        self.minaddress[3] += 1;
        self.maxaddress[3] -= 1;
        print('Usable range: {0} - {1}'.format(str(self.minaddress)[1:len(str(self.minaddress))-1].replace(',','.'),
        str(self.maxaddress)[1:len(str(self.maxaddress))-1].replace(',','.')))

if __name__ == "__main__":
    ipclass = input("Enter IP class: ")
    n = input("Enter count of subnetworks: ")
    m = input("Enter count of computers: ")
    mask = Mask(ipclass, n, m)
    mask.create_mask()

