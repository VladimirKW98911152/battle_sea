from tkinter import *
from tkinter import messagebox  # Компонент модуля tkinter для закрытия окна
import time
import random  # random - модуль для генерации случайных чисел

tk = Tk()
app_running = True  # значение app_running становится ложным, после чего цикл "while app_running:" прерывается
size_canvas_x = 500  # Размер поля по горизонтали
size_canvas_y = 500  # Размер поля по вертикали
s_x = s_y = 6  # Переменная, обозначающая количество клеток - размер игрового поля: 6 горизонт(х) х 6 вертикальн(у)
s_y = 6
step_x = size_canvas_x // s_x  #  Шаг отрисовки линий определяется целочисленным делением 500 на 6
step_y = size_canvas_y // s_y  # Такой же шаг делаем для клеток оси y, и то же получаем 5 шагов между ячейками оси y
size_canvas_x = step_x * s_x  # Переменным, в которых указывается размер сторон поля, присваивается значение, равное
size_canvas_y = step_y * s_y  # произведению количества клеток на выбранный шаг отрисовки, чтобы исключить появление
                      #  остатков от деления значения размера поля на количество клеток по горизонтали и вертикали
delta_menu_x = 3  # Переменная, отвечающая за размер меню по оси X
menu_x = step_x * delta_menu_x  # Создание рабочей области для меню, здесь устанавливается размер меню по оси x
menu_y = 40  # Создание рабочей области для меню, и определение её размера, 40 пикселей по вертикали

ships = s_x // 1 + 1  # Переменная, обозначающая максимальное количество кораблей для игрового поля
ship_len1 = s_x // 2  # Переменная, обозначающая корабль длинной в 3 клетки
ship_len2 = s_x // 3  # Переменная, обозначающая корабль длиной в 2 клетки
ship_len3 = s_x // 6  # Переменная, обозначающая корабль длиной в 1 клетку
enemy_ships1 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]  # Список для караблей для игрока. Указанная
                      # строка определяет размерность списка караблей в зависимости от размеров игрового поля.

enemy_ships2 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]   # Список для караблей для компьютера
list_ids = []   #  Переменная, содержащая в себе список отресованных объектов (canvas) и их ID

# points1,2 - это список, куда мы кликнули мышкой и этот список находится поверх списка 1 игрового поля
points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
points2 = [[-1 for i in range(s_x)] for i in range(s_y)]


# boom - писок попаданий по кораблям
boom = [[0 for i in range(s_x)] for i in range(s_y)]  # Заполняем данный список значениями "0", для того, чтобы потом
# добавлять в него значения попаданий

ships_list = []  # список кораблей игрока и компьютера

hod_igrovomu_polu_1 = False  # Переменная, отвечающая за переключение хода на компьютер, если переменная ложная, то наступает
                     # очередность хода компьютера

computer_vs_human = True  # Значение этой переменной означает, что мы действительно играем с компьютером
if computer_vs_human:
    hod_igrovomu_polu_1 = False  # Если ход предоставляется компьютеру, то игрок ходить не может
else:
    add_to_label = ""

# print(enemy_ships1)

def on_closing():  # Функция выхода из игры, импортируется из messagebox
    global app_runing  # Переменная, проверяющая, запущено окно, или нет
    if messagebox.askokcancel("Выйти из игры", "Выйти из игры?"):
        app_runing = False  # При нажатии, объект (окно игры с меню и игровыми полями) уничтожается
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)  # Параметры игры
tk.title("Игра Морской бой")  # Определяет название заголовка окна игры
tk.resizable(0, 0)  # Атрибут, благодаря которому отсутствует возможность изменить размер окна запущенного приложения
tk.wm_attributes("-topmost", 1)  # Атрибут, благодаря которому окно приложения отображается поверх других открытых окон
canvas = Canvas(tk, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="turquoise")
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y, fill="white")
canvas.pack()   # Параметры поля оздаем берюзовый прямоугольный фон для поля с кораблями компьютера
tk.update()   # Вся часть от "tk.protocol("WM_DELETE..." до этой строки относится к импорту из библиотеки "tkinter"


def draw_table(offset_x=0):  # Функция, предназначенная для рисовки клеточного поля
    for i in range(0, s_x + 1):  # цикл, который отрисовывает ячейки "step_x" на поле
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)   # создание линии, меняются
 # значения иксов. Объявляется переменная i, от значения которой зависит продолжительность цикла, рис. границы ячеек х
    for i in range(0, s_y + 1):  # цикл, который отрисовывает ячейки "step_y" на поле
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)   # создание линии, меняются
# значения игриков. Объявляется переменная i, от значения которой зависит продолжительность цикла, рис. границы ячеек y
               # Линии рисуются от 0 до размера по оси х (size_canvas_x) или у (size_... y) с шагом  step_x (или у)


draw_table()  # Ставим функцию по дорисовке поля перед циклом рабочей области
draw_table(size_canvas_x + menu_x)  # Добавляет отрисовку поля на на рабочей области справа от меню

t0 = Label(tk, text="Здесь Ваши корабли, не стреляйте сюда", font=("Helvetica", 16))  # Добавляет отрисовку наименования рабочей
# области игрока text="Идесь Ваши корабли, не стреляйте сюда" - содержание текста, "font=("Helvetica", 16)" - тип и размер шрифта
t0.place(x=size_canvas_x//2 - t0.winfo_reqwidth() // 2, y=size_canvas_y+3)  # Обозначение координат размещения
#  наименования по оси x (по центру). t0.winfo_reqwidth() // 2 - это смещение текста так, что предыдущее его начало
#  сместилось на половину в сторону начала координат
t1 = Label(tk, text="Здесь корабли компьютера, стреляйте сюда", font=("Helvetica", 16))  # Отрисовка имени рабочей области компьютера
t1.place(x=size_canvas_x + menu_x + size_canvas_x//2 - t1.winfo_reqwidth() // 2, y=size_canvas_y+3)

t0.configure(bg="red")  # Фон, на котором имеется надпись "Здесь Ваши корабли, не стреляйте сюда"
t0.configure(bg="#f0f0f0")  # Устанавливает фон по умолчанию

t3 = Label(tk, text="@@@@@", font=("Helvetica", 16))  # Отрисовка отметки о том, чей ход
t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y)  # Обозначение координат размещения
#  наименования по оси x (по центру). t0.winfo_reqwidth() // 2 - это смещение текста так, что предыдущее его начало
#  сместилось на половину в сторону начала координат


def mark_igrok(igrok_mark_1):  # Помечает, то, игрок или компьютер ходит, то есть чей ход начинается
    if igrok_mark_1:  # Если начинается ход игрока(его табличка это переменная t0), то помечаем его красным цветом
        t0.configure(bg="red")
        t1.configure(bg="#f0f0f0")
        t3.configure(text="Ходит компьютер")
        t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y)
    else:   # Если начинается ход компьютера, (его табличка это переменная t1), то помечаем его красным цветом
        t1.configure(bg="red")
        t0.configure(bg="#f0f0f0")
        t3.configure(text="Ваш ход")
        t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y)

mark_igrok(hod_igrovomu_polu_1)

def button_show_enemy1():  # функция, задающая алгоритм работы кнопки b0 (Показать корабли игрока), вывода кораблей
    for i in range(0, s_x):  # двойной цикл проверки наличия кораблей на направлении вдоль оси x (значения i)
        for j in range(0, s_y):  # двойной цикл проверки наличия кораблей на направлении вдоль оси y (значения y)
            if enemy_ships1[j][i] > 0:  # Строка отвечает за то, чтобы при нажатии кнопки "Показать корабли игрока" -
                color = "orange"  # - целые фрагменты кораблей отрисовывались оранжевым цветом
                if points1[j][i] != -1:  # Строка отвечает за то, чтобы при нажатии кнопки "Показать корабли компьютера"- 
                    color = "black"  # - поврежденные фрагменты кораблей отрисовывались черным цветом
                _id = canvas.create_rectangle(i*step_x, j*step_y, i*step_x + step_x, j*step_y + step_y,
                                              fill=color)  # Координаты фрагментов кораблей игрока и их цвет
                list_ids.append(_id)  # с помощью метода .append добавляем значение переменной id в список list_ids

def button_show_enemy2():  # функция, задающая алгоритм работы кнопки b0 (Показать корабли компьютера), вывода кораблей
    for i in range(0, s_x):  # двойной цикл проверки наличия кораблей на направлении вдоль оси x (значения i)
        for j in range(0, s_y):  # двойной цикл проверки наличия кораблей на направлении вдоль оси y (значения y)
            if enemy_ships2[j][i] > 0:  # Строка отвечает за то, чтобы при нажатии кнопки "Показать корабли компьютера" -
                color = "orange"  # - целые фрагменты кораблей отрисовывались зеленым цветом
                if points2[j][i] != -1:  # Строка отвечает за то, чтобы при нажатии кнопки "Показать корабли компьютера" -
                    color = "black"  # - поврежденные фрагменты кораблей отрисовывались черным цветом
                _id = canvas.create_rectangle(size_canvas_x + menu_x + i*step_x, j*step_y, size_canvas_x + menu_x +
                                              i*step_x + step_x, j*step_y + step_y, fill=color)  # Координаты фрагментов
                # кораблей компьютера и их цвет
                list_ids.append(_id)  # с помощью метода .append добавляем значение переменной id в список list_ids


def button_begin_again():  # Задаем алгоритм работы кнопки b1 (Начать заново), заключается в очищении списка list_ids
    global list_ids  # Присваиваем спискам list_ids, points1 и boom статус глобальных, определяем им глобальную зону
    global points1  #  видимости, чтобы работа с этими списками перенеслась в эту функцию и чтобы не нужно было
    global points2  #  создавать их новые копии
    global boom
    global enemy_ships1  # Определяем для переменных enemy_ships1 и enemy_ships2 значения
    global enemy_ships2  # глобальных переменных
    for el in list_ids:
        canvas.delete(el)  # Если в поле (canvas) есть элементы, то они удаляются из списка
    list_ids = []  # После очищение списка присваиваем ему значение [], то есть элементов в нем нет
    generate_ships_list()
    enemy_ships1 = generate_enemy_ships()  # После очищения вновь запускаем функцию,
    enemy_ships2 = generate_enemy_ships()  # которая генерирует и расставляет корабли
    points1 = [[-1 for i in range(s_x)] for i in range(s_y + 1)]  # строка отвечает за обнуление списка, который
      # сформировался в результате нажатий на области поля игрока в предыдущей игре
    points2 = [[-1 for i in range(s_x)] for i in range(s_y + 1)]  # строка отвечает за обнуление списка, который
      # сформировался в результате нажатий на области поля компьютера в предыдущей игре
    boom = [[0 for i in range(s_x)] for i in range(s_y)]  # строка отвечает за обнуление списка, количества попаданий


b0 = Button(tk, text="Показать корабли игрока", command=button_show_enemy1)  # Кнопка "Показать корабли игрока"
b0.place(x=size_canvas_x+20, y=20)  # Координаты кнопки в рабочей области разместить в 20 пунктах от горизонтальной
# границы рабочей области (крайнего значения переменной "size_canvas_x") на 20 пункте по вертикальной оси "Y"

b2 = Button(tk, text="Показать корабли компьютера", command=button_show_enemy2)  # Кнопка "Показать корабли компьютера"
b2.place(x=size_canvas_x+20, y=55)  # Координаты кнопки в рабочей области разместить в 20 пунктах от горизонтальной
# границы рабочей области (крайнего значения переменной "size_canvas_x") на 55 пункте по вертикальной оси "Y"

b1 = Button(tk, text="Начать заново", command=button_begin_again)  # Кнопка "Начать игру заново"
b1.place(x=size_canvas_x+20, y=90)  # Координаты кнопки в рабочей области разместить в 20 пунктах от горизонтальной
# границы рабочей области (крайнего значения переменной "size_canvas_x") на 90 пункте по вертикальной оси "Y"

b5 = Button(tk, text="1. Ходите левой кнопкой мыши!")  # Надпись о том, какой кнопкой ходить
b5.place(x=size_canvas_x+20, y=125)  # Координаты кнопки в рабочей области разместить в 20 пунктах от горизонтальной
# границы рабочей области (крайнего значения переменной "size_canvas_x") на 125 пункте по вертикальной оси "Y"

def draw_point(x, y):
    print(enemy_ships1[y][x])  # Команда, которая выводит в консоль области, в которой произошло нажатие кнопки мыши
    if enemy_ships1[y][x] == 0:
        color = "red"
        id1 = canvas.create_rectangle(x * step_x, y * step_y, x * step_x + step_x, y * step_y +
                                      step_y // 9 + step_y // 9, fill=color)  # Параметры и цвет метки рабочей области
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 12, y * step_y + step_y // 9 +
                                      step_y // 9, x * step_x + step_x // 2 + step_x // 12, y * step_y + step_y,
                                      fill=color)

        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships1[y][x] > 0:
        color = "blue"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 12, x * step_x + step_x,
                                     y * step_y + step_y // 2 + step_y // 12, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 12, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 12, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def draw_point2(x, y, offset_x=size_canvas_x + menu_x):  # Делаем отрисовку нажатий, но с учетом смещения на длину 1 -
    # - поля и меню
    print(enemy_ships1[y][x])  # Команда, которая выводит в консоль области, в которой произошло нажатие кнопки мыши
    if enemy_ships2[y][x] == 0:
        color = "red"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x, y * step_y +
                                      step_y // 9 + step_y // 9, fill=color)  # Параметры и цвет метки рабочей области
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 12, y * step_y + step_y // 9 +
                                      step_y // 9, offset_x + x * step_x + step_x // 2 + step_x // 12, y * step_y +
                                      step_y, fill=color)

        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships2[y][x] > 0:
        color = "blue"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 12, offset_x + x *
                                      step_x + step_x, y * step_y + step_y // 2 + step_y // 12, fill=color)
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 12, y * step_y, offset_x +
                                      x * step_x + step_x // 2 + step_x // 12, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)

def check_winner(x, y): # Первая проверка игрока, требует создания дополнитеольного списка boom (список попаданий)
    win = False  # Если суммы значений enemy_ships1 и boom совпадает, win принимает значение False (лож), т.е. победы нет
    if enemy_ships1[y][x] > 0:  # если значение в этом списке находится не "0", то мы пишем его в boom[y][x]
        boom[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))  # строка осуществляет суммирование значений enemy_ships1
    sum_boom = sum(sum(i) for i in zip(*boom))  # строка осуществляет суммирование значений enemy_boom
    if sum_enemy_ships1 == sum_boom:  # Если суммы значений enemy_ships1 и boom совпадает, win принимает значение True
        win = True
    return win


def check_winner2():  # Вторая проверка игрока (по спискам). Устанавливается, что в начале игры игрок уже победил
    win = True  # Но если в начале игры имеется хоть одна клетка, где enemy_ships1[j][i] больше "0", то победы нет
                # Присваем win изначальное значение True (истина), т.е. победа есть
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:  # если имеется клетка с координатами points1, в которых мы не прокликали, -
                    win = False  # - то win принимает значение False (лож), т.е. победы нет

    return win

def check_winner2_igrok_2():  # Проверка победы копьютера (по спискам). Устанавливается, что в начале игры компьютер уже -
    win = True  # -победил, но если в начале игры имеется хоть одна клетка, где enemy_ships1[j][i] больше "0", -
                # - то победы нет рисваем win изначальное значение True (истина), т.е. победа есть
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:  # если имеется клетка с координатами points1, в которых компьютер не прокликал,
                    win = False  #  то win принимает значение False (лож), т.е. победы нет

    return win


def hod_computer():  # функция, отвечающая за ходы компьютера
    global points1  # Присваиваем нашим спискам points1/2 и hod_igrovomu_polu_1 статус глобальной, определяем ему глобальную
    global points2  # зону видимости
    global hod_igrovomu_polu_1
    tk.update()
    time.sleep(0.5)  # Добавляем из модуля time метод задержки действия на 1 секунду - time.sleep(1)
    hod_igrovomu_polu_1 = False
    ip_x = random.randint(0, s_x-1)  # Генерирует случайное число порядкового номера клетки поля по оси x
    ip_y = random.randint(0, s_y-1)  # Генерирует случайное число порядкового номера клетки поля по оси y
    while not points1[ip_y][ip_x] == - 1:  # Цикл, генерирующий случайные числа до тех пор, пока в этом списке будет
        ip_x = random.randint(0, s_x-1)     # значение, отличное от одного, координаты будут определяться заново
        ip_y = random.randint(0, s_y-1)
    points1[ip_y][ip_x] = 7
    draw_point(ip_x, ip_y)  # Функция по отображению на экране крестика, или Т, если щелкнул мышью по полю
    if check_winner2():
        winner = " Вы проиграли....."  # Надпись о поражении игрока
        print(winner)
        points1 = [[10 for i in range(s_x)] for i in range(s_y)]
        points2 = [[10 for i in range(s_x)] for i in range(s_y)]  # Препятствует нажатию на клетки после победы
        id1 = canvas.create_rectangle(step_x * 2, step_y * 2, size_canvas_x + menu_x + size_canvas_x - step_x * 2,
                                      size_canvas_y - step_y * 2, fill="yellow")  # Выводит на экран желтую
        # окаемку таблички с уведомлением о победе компьютера
        list_ids.append(id1)  # Стерает окаемку таблички после нажатия "Начать заново"
        id2 = canvas.create_rectangle(step_x * 2 + step_x // 4, step_y * 2 + step_y // 4, size_canvas_x + menu_x
                                      + size_canvas_x - step_x * 2 - step_x // 4, size_canvas_y - step_y * 2 -
                                      step_y // 4, fill="red")  # Выводит на экран зеленый фон таблички с
        # уведомлением о поражении игрока
        list_ids.append(id2)  # Стерает фон таблички после нажатия "Начать заново"
        id3 = canvas.create_text(step_x * 7 + step_x // 2, step_y * 2 + step_y // 2 + step_y // 2, text=winner,
                                 font=("Times New Roman", 50), justify=CENTER)
        # id3 - выводит надпись о поражении игрока (выводит значение переменной winner)
        list_ids.append(id3)  # Стерает надпись о поражении игрока после нажатия "Начать заново"


def add_to_all(event):
    global points1  # Присваиваем нашим спискам points1/2 и hod_igrovomu_polu_1 статус глобальной, определяем им глобальную
    global points2  # зону видимости
    global hod_igrovomu_polu_1
    _type = 0  # Переменная, в которой мы будем хранить то нажатие, которое мы произвели, 0 это для левой кнопки мыши
    if event.num == 3:
        _type = 1   # А единица будет для правой кнопки мыши, то есть переменная"_type"  будет хранить 0, если мы нажали
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()  # Для того, чтобы получить координаты окошка, по которому
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()  # щелкнули кнопкой мыши mouse_x - по оси x, другая по y
    # print(mouse_x, mouse_y)  # Здесь "print" выводит в консоль значения координаты клеток указываются исходя из
    # значений size_canvas_x и size_canvas_y, за начало координат, берется верхней левый угол поля
    ip_x = mouse_x // step_x  # Переменная, обозначающая координаты относительно порядкового номера клеток поля по оси x
    ip_y = mouse_y // step_y  # Переменная, обозначающая координаты относительно порядкового номера клеток поля по оси y
    print(ip_x, ip_y, "_type:", _type)  # Команда, которая выводит в консоль значения координат, единицами которых
    # кявляются порядковые номера клеток по оси x и по оси y. "_type:", _type выводит значение нажатой кнопки мыши

    # Первое игровое поле
    if ip_x < s_x and ip_y < s_y and hod_igrovomu_polu_1:  # Проверка того, чтобы не выйти за пределы первого игрового поля
        if points1[ip_y][ip_x] == - 1:  # проверка того, нажимали ли мы уже на выбранную область, благодаря этой части
            # тела функции, объект будет отрисовываться только в том случае, если нажатия на него не было
            points1[ip_y][ip_x] = _type  # Если координаты нажатия мышки совпали с координатами _type, то наступает
            hod_igrovomu_polu_1 = False  # очередь хода компьютера, то есть переменная hod_igrovomu_polu_1 становится False
            draw_point(ip_x, ip_y)  # Функция по отображению на экране крестика, или буквы Т, если произведен щелчок по полю
            if check_winner2():
                winner = "Вы проиграли....."  # Надпись о поражении игрока
                hod_igrovomu_polu_1 = True  #  Если игрок победил, то он может первым ходить после начала новой игры
                print(winner)
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]  # Препятствует нажатию на клетки после победы
                id1 = canvas.create_rectangle(step_x * 2, step_y*2, size_canvas_x + menu_x + size_canvas_x - step_x * 2,
                                              size_canvas_y - step_y * 2, fill="yellow")  # Выводит на экран желтую
                                                                   # окаемку таблички с уведомлением о проигрыше игрока
                list_ids.append(id1)  #  Стерает окаемку таблички после нажатия "Начать заново"
                id2 = canvas.create_rectangle(step_x * 2 + step_x // 4, step_y * 2 + step_y // 4, size_canvas_x + menu_x
                                              + size_canvas_x - step_x * 2 - step_x // 4, size_canvas_y - step_y * 2 -
                                              step_y // 4, fill="green")  # Выводит на экран зеленый фон таблички с
                                                                          # уведомлением о поражении игрока
                list_ids.append(id2)  #  Стерает фон таблички после нажатия "Начать заново"
                id3 = canvas.create_text(step_x * 7 + step_x // 2, step_y * 2 + step_y // 2 + step_y // 2, text=winner,
                                         font=("Times New Roman", 50), justify=CENTER)
                # id3 - выводит надпись о поражении игрока (выводит значение переменной winner)
                list_ids.append(id3)  #  Стерает надпись о поражении игрока после нажатия "Начать заново"
    mark_igrok(hod_igrovomu_polu_1)
    

    # Второе игровое поле
    if ip_x >= s_x + delta_menu_x and ip_x <= s_x + s_x + delta_menu_x and ip_y < s_y and not hod_igrovomu_polu_1:  #  Про-
        # - верка того, чтобы мы не вышли за перделы второго игрового поля за пределы игрового поля not hod_igrovomu_polu_1:
        # щзначает, что в данном условии переменная hod_igrovomu_polu_1 имеет значение False
        # print("ок")
        if points2[ip_y][ip_x - s_x - delta_menu_x] == - 1:  # проверка того, нажимали ли мы уже на выбранную область,
         # благодаря этой части тела функции, компьютер будет отрисовывать объект только в том случае, если нажатия
         # на него не было
            points2[ip_y][ip_x - s_x - delta_menu_x] = _type  # Если координаты нажатия мышки совпали с координатами
            hod_igrovomu_polu_1 = True  # _type, то очередь хода возвращается ко второму игрока, то есть переменная
                                  #  hod_igrovomu_polu_1 становится True
            draw_point2(ip_x - s_x - delta_menu_x, ip_y)  # Функция по отображению на экране крестика, или буквы Т,
         # если щелкнул мышью по полю
            # if check_winner(ip_x, ip_y):  # срока, которая отвечает за проверку того, победил игрок, или нет
            if check_winner2_igrok_2():
                winner = "Вы победили !!!!!"  # Надпись о победе игрока
                hod_igrovomu_polu_1 = False  # Если победил игрок, то в он ходит первым в следующей игре
                print(winner)
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]  # Препятствует нажатию на клетки после победы
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                id1 = canvas.create_rectangle(step_x * 2, step_y * 2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 2,
                                              size_canvas_y - step_y * 2, fill="yellow")  # Выводит на экран желтую
                # окаемку таблички с уведомлением о победе игрока
                list_ids.append(id1)  # Стерает окаемку таблички после нажатия "Начать заново"
                id2 = canvas.create_rectangle(step_x * 2 + step_x // 4, step_y * 2 + step_y // 4, size_canvas_x + menu_x
                                              + size_canvas_x - step_x * 2 - step_x // 4, size_canvas_y - step_y * 2 -
                                              step_y // 4, fill="green")  # Выводит на экран зеленый фон таблички с
                # уведомлением о победе игрока
                list_ids.append(id2)  # Стерает фон таблички после нажатия "Начать заново"
                id3 = canvas.create_text(step_x * 7 + step_x // 2, step_y * 2 + step_y // 2 + step_y // 2, text=winner,
                                         font=("Times New Roman", 50), justify=CENTER)
                # id3 - выводит надпись о победе игрока (выводит значение переменной winner)
                list_ids.append(id3)  # Стерает надпись о победе игрока после нажатия "Начать заново"
            elif computer_vs_human:
                mark_igrok(hod_igrovomu_polu_1)
                hod_computer()
    mark_igrok(hod_igrovomu_polu_1)


canvas.bind_all("<Button-1>", add_to_all)  # Отвечает за выделение выбранной области левой кнопкой мыши


def generate_ships_list():
    global ships_list
    ships_list = [ship_len1, ship_len2, ship_len2, ship_len3, ship_len3, ship_len3, ship_len3]  # создаем список
    # кораблей для того, чтобы потом цикл "sum_1_enemy != sum_1_all_ships:" раскидал эти корабли по полю
    print(ships_list)  # Эта команда на экран значения случайно созданного списка.

def generate_enemy_ships():  # Сама функция по размещению кораблей на поле в случайном порядке
    global ships_list
    enemy_ships = []  # Присваиваем нашему списку статус глобального, определяем ему глобальную зону видимости,
    # чтобы работа с данным списком перенеслась в эту функцию и чтобы не создавать его новую копию

    sum_1_all_ships = sum(ships_list)  # Подсчеет суммарной длины кораблей
    sum_1_enemy = 0  # переменная, которая считает количество противников - кораблей в нашем списке
    

    while sum_1_enemy != sum_1_all_ships:  # этот цикл постоянно разбрасывает корабли, пока они не перестанут пересекать
        # ся друг с другом
        enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)] # Обнуляем массив кораблей, расположение 
    # которых не соответствует этому устовин. +1 для доп. линии справа и снизу, для успешных проверок генерации кораблей

        for i in range(0, ships):
            len = ships_list[i]  # Берем за длину корабля переменную "len", в которую случайным образом задаем значение
            horizont_vertikal = random.randrange(1, 3)  # как будем располагать судно 1- горизонтальное 2 - вертикальное
            # Тройка не включается, так как это индекс, до которого распространяется область видимости

            primerno_x = random.randrange(0, s_x)  # Отвечает за случайное расположение координат судна по оси х,
            if primerno_x + len > s_x:        # входящее в диапазон координат от значения 0 до значеня переменной s_x
                primerno_x = primerno_x - len  # если конечная координата находится за пределами s_x, то мы сдвигаем
# координаты судна (переменной primerno_x) то мы путем вычитания сдвигаем их к началу координат, то есть в лево
            primerno_y = random.randrange(0, s_y)  # эта часть цикла аналогична части цикла для переменной primerno_x
            if primerno_y + len > s_y:             # только она распространяется на переменую primerno_y, отвечающую
                primerno_y = primerno_y - len      # за расположение координат по оси y

            if horizont_vertikal == 1:  # Условие, если компьютер выбрал горизонтальное размещение, то есть переменная
                if primerno_x + len <= s_x:  # horizont_vertikal приняла значение 1, то применяется
                    for j in range(0, len):  # primerno_x + len <= s_x: означает, если мы не вышли за границы поля, то
                        try:  # переменной j присваивается значение в диапазоне от начала координат до крайней точки
                            # try - означает начало блока, соблюдение условий которого порождает исключение
                            # в данном случае Exception
                            check_near_ships = 0  # длины корабля, после чего цикл проверяет
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля (переменная
                # i), присваивая ему значение i + 1, чтобы корабль не располагался по краям поля, то есть не равнялся 0
                        except Exception:  # except исключение, порождаемое блоком try, в данном случае это Exception
                            pass
            if horizont_vertikal == 2:  # Условие, если компьютер выбрал ертикальное размещение, то есть переменная
                if primerno_y + len <= s_y:  # horizont_vertikal приняла значение 2, то применяется
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] +\
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1


    return enemy_ships


generate_ships_list()
enemy_ships1 = generate_enemy_ships()  # Функция по размещению/генерации кораблей Игрока на поле в случайном порядке
enemy_ships2 = generate_enemy_ships()  # Функция по размещению/генерации кораблей Компьютера на поле в случайном порядке

# Создаем цикл для игры, означающий, что программа, выводящая на экран окно, заданное выше, исполняется бесконечно
while app_running:  # Цикл рабочей области
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)

