class MyData:
    __INN=""
    __PASSWORD=""
    __CLIENT_SECRET=""
    __INUSE=0

    # Создание набора данных
    def __init__ (self, INN,PASSWORD,SECRET,INUSE):
        self.__INN=INN
        self.__PASSWORD=PASSWORD
        self.__CLIENT_SECRET=SECRET
        self.__INUSE=INUSE

    # Сохранит, что было использование
    def Use(self):
        self.__INUSE+=1;
        return self

    # Получить ИНН, пароль, специальное поле
    def GetINN(self)->str:
        return self.__INN

    def GetPASS(self)->str:
        return self.__PASSWORD

    def GetSEC(self)->str:
        return self.__CLIENT_SECRET

    # Получить, сколько раз было использовано
    def GetUSE(self)->int:
        return self.__INUSE

    # Обнулить использования
    def ZeoUse(self):
        self.__INUSE=0

    # Для перегона в json
    def CodeMe(self):
        return (self.__INN,self.__PASSWORD, self.__CLIENT_SECRET, self.__INUSE)


class MyDataMass:
    __Data=list()

    # Добавить набор в массив
    def append(self, value):
        self.__Data.append(value)

    # Узнать размер массива
    def size(self)->int:
        return len(self.__Data)

    # Получить i набор данных
    def GetI(self, i):
        return self.__Data[i]

    # Закодировать массив с наборами в json
    def CodeMe(self):
        ret=list()
        for one in self.__Data:
            ret.append(one.CodeMe())
        return ret

    # Раскодировать json
    def UnCodeData(self, data):
        self.__Data=list()
        for one in data:
            self.__Data.append(MyData(one[0],one[1], one[2], one[3]))

    # Обнулить количество использований всех наборов
    def ZeroUse(self):
        for one in self.__Data:
            one.ZeoUse()