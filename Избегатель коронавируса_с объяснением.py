import sys
from itertools import cycle
from random import randrange
from tkinter import messagebox
from tkinter import *

canvas_width = 800 #размеры окна
canvas_height = 600

color_cycle = cycle(['medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
                     'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
                     'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
                     'forest green', 'olive drab']) #цвета короны
interval = 1000  # частота добавления нового вируса
frame_rate = 16  # 16ms = 60fps - скорость
y_speed = 1 #скорость движения по у
factor = 0.994 # коэфф сложности6 показывает, с какой частотой должны появляться вирусы на экране, чем ближе к 1, тем проще
mask=3 #маска, 3 жизни

# зададим начальную позицию человека (у нижнего края по центру холста)
initial_x = canvas_width / 2
initial_y = canvas_height - 20
catcher_tag = "catcher_tag" #создаем тег, т.е. собранные части человека чтобы двигались вместе
head_radius = 19 #радиус головы


# 15 - Хватаем таблетку
def check_tablet():
    global temperature
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = canvas.coords(catcher)
    for tablet_object, tag in zip(tablets, tablet_tags):
        (x, y, x2, y2) = canvas.coords(tablet_object)
        if catcher_x < x and x2 < catcher_x2 and catcher_y2 - y2 < 40:
            tablets.remove(tablet_object)
            tablet_tags.remove(tag)
            canvas.delete(tag)
            if temperature > 36.6:
                 temperature -= 0.4        
            update_texts()
    root.after(frame_rate, check_tablet)

# 14 - Движение таблетки
def move_tablets():
    for tablet_object, tag in zip(tablets, tablet_tags):
        (_, tablet_y1, _, _) = canvas.coords(tablet_object)
        canvas.move(tag, 0, y_speed)
        if tablet_y1 > canvas_height:
            tablets.remove(tablet_object)
            tablet_tags.remove(tag)
            canvas.delete(tag)
            canvas.delete(tablet_object)
    root.after(frame_rate, move_tablets)
        
#13 Таблетка
def create_tablet():
    global tablet_counter
    x = randrange(10, 740)
    y = 100
    tag = "tablet-" + str(tablet_counter)

    tablet = create_circle(x, y, 8, tag, fill_color="gold")    
    tablets.append(tablet)
    tablet_tags.append(tag)
    tablet_counter += 1
    root.after(interval * 6, create_tablet)

#12 - Если заденем короону
def check_corona():
    global mask, temperature
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = canvas.coords(catcher)
    for corona, tag in zip(corona_centers, coronas_tags):
        (x, y, x2, y2) = canvas.coords(corona)
        if catcher_x < x and x2 < catcher_x2 and catcher_y2 - y2 < 40:
            corona_centers.remove(corona)
            coronas_tags.remove(tag)
            canvas.delete(tag)
            update_nose()
            if mask == 0:
                temperature += 0.8
                update_texts()
            if mask > 0:
                mask -= 1
                update_texts()
                if mask == 0:
                    canvas.delete(mask_ris)
    root.after(frame_rate, check_corona)
# -> 1

# 11 - Вправо
def move_right(event):
    (x1, y1, x2, y2) = canvas.coords(catcher)
    if x2 < canvas_width:
        canvas.move(catcher_tag, 30, 0)

# 10 - Влево
def move_left(event):
    (x1, y1, x2, y2) = canvas.coords(catcher)
    if x1 > 0:
        canvas.move(catcher_tag, -30, 0)
        
# 9 - Рисуем маску
def mask1():
    global catcher_tag, initial_center_x, initial_center_y, head_radius    
    mask_x = initial_x - head_radius
    mask_y = initial_y - head_radius
    mask_x2 = initial_x + head_radius
    mask_y2 = initial_y + head_radius
    mask_color = 'light cyan'
    mask_ris = canvas.create_arc(mask_x, mask_y, mask_x2, mask_y2, start=30, extent=120, \
                      style='arc', outline=mask_color, width=5, tag=catcher_tag)
    return mask_ris # -> 1

#8 - Обновление носа
def update_nose():
    global nose, temperature
    color = ['tan2', 'coral', 'tomato', 'orange red', 'red', 'black']
    i = int((temperature - 36.6) // 0.8)
    canvas.itemconfigure(nose, fill=color[i]) # -> 1

#7 - Нос
def nose1():
    global catcher_tag, initial_x, initial_y, head_radius
    nose_color = 'tan2'
    nose_radius = 7
    nose = create_circle(initial_x, initial_y - head_radius, nose_radius, catcher_tag, nose_color)
    return nose # -> 1

#6 - Рисуем человечка
def draw_catcher():
    global catcher_tag, initial_x, initial_y, head_radius
    catcher_tag = "catcher_tag"
    # задаем параметры корзины
    hands_color = 'tan1'
    head_color = 'tan3'   
    hands_radius = 50  # диаметр окружности для рисования дуги
    # рисуем руки
    hands_start_x = initial_x - hands_radius
    hands_start_y = initial_y - hands_radius * 2
    hands_start_x2 = initial_x + hands_radius
    hands_start_y2 = initial_y

    hands = canvas.create_arc(hands_start_x, hands_start_y, hands_start_x2, hands_start_y2, start=200, extent=140, \
                              style='arc', outline=hands_color, width=3, tag=catcher_tag)
    # рисуем голову, функция уже создана
    create_circle(initial_x, initial_y, head_radius, catcher_tag, head_color)
    return hands
    # -> 1

#5 движение короны
def move_coronas():
    global score, frame_rate, interval, y_speed
    for corona, tag in zip(corona_centers, coronas_tags): #zip объединяет пары координат
        (_, corona_y1, _, _) = canvas.coords(corona) #нижняя координата короны (либо скроется, либо заразит)
        #если нужна одна переменная, мы другие можем заменить слэшами!
        canvas.move(tag, randrange(-1, 2), y_speed) #по х не перемещаем, по у с опр.скоростью
        #randrange(-1, 2) - чтобы дергались из стороны в сторону
        if corona_y1 > canvas_height: #если по у скрылась за краем, то
           corona_centers.remove(corona)
           coronas_tags.remove(tag)
           canvas.delete(tag) #убираем корону
           score += 1 #увеличиваем количество дней   
           interval = int(interval * factor) #увеличиваем скорость
           y_speed = y_speed / factor #сокращаем движение по у
           update_texts() #обновляем надпись           
        if int(temperature) >= 41:
            messagebox.showinfo('Всё, капец!', 'Вы прожили ' + str(score) + ' дней')
            sys.exit()
    root.after(frame_rate, move_coronas)
#-> 1

#4
def create_circle(x, y, radius, tag, fill_color): 
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, tag=tag, fill=fill_color, width=0)
#-> 3

def corona(): #3 рисование короны
    global corona_counter, interval
    x = randrange(10, 740) #случайное положение по х
    y = 40
    tag = "corona-" + str(corona_counter) 
    fill = next(color_cycle) #следующий цвет из списка
    radius_45 = 12 * 0.707 #радиус на котором будут находиться маленькие кружочки 12 * синус 45(0.7)
    corona_center = create_circle(x, y, 8, tag, fill) #центральный круг короновируса, радиус 8

    # круги под углом 90 градусов
    create_circle(x + 12, y, 2, tag, fill) #радиус маленьких кружков = 2, радиус расположения = 12
    create_circle(x - 12, y, 2, tag, fill) # -> 4 Делаем функцию отрисовки вируса
    create_circle(x, y + 12, 2, tag, fill)
    create_circle(x, y - 12, 2, tag, fill)

    # круги под углом 45 градусов
    create_circle(x + radius_45, y + radius_45, 2, tag, fill)
    create_circle(x + radius_45, y - radius_45, 2, tag, fill)
    create_circle(x - radius_45, y + radius_45, 2, tag, fill)
    create_circle(x - radius_45, y - radius_45, 2, tag, fill)

    corona_centers.append(corona_center) #добавляем номер вируса в список
    coronas_tags.append(tag) #добавляем номер тега в список
    corona_counter += 1
    root.after(interval, corona) #добавить корону через interval мсек
#-> 1

def update_texts(): #2
    canvas.itemconfigure(lives_text, text='Температура: ' + '{0:.1f}'.format(temperature))
    canvas.itemconfigure(score_text, text='Дни: ' + str(score))
    canvas.itemconfigure(defence_text, text="Защита маски " + (u'\u2764') * mask)
#-> 1

#1 - НАЧАЛО 
root = Tk() #окно
canvas = Canvas(root, width=canvas_width, height=canvas_height, background='black')
#Нарисованная картинка (как вариант):
#canvas.create_rectangle(-5, canvas_height-100, canvas_width+5, \
#                           canvas_height+5, fill="brown", width=0) #нижний прямоугольник, земля
#canvas.create_oval(-80, -80, 120, 120, fill="orange", width=0) #солнце, видно в окне кусок
canvas.pack()

corona_counter = 0 #считает сколько корон на экране
tablet_counter = 0 #сколько таблеток
score = 0 #считает прошедшие дни
score_text = canvas.create_text(10, 10, anchor='nw', font='Timesnewroman', fill='silver') #блок для счета
temperature = 36.6 #первоначальная температура
lives_text = canvas.create_text(800 - 10, 10, anchor='ne', font='Timesnewroman', fill='green2') #блок для температуры
defence_text = canvas.create_text(canvas_width - 10, 30, anchor='ne', font='Timesnewroman', fill='green2') #Маска
update_texts() #функция для информационных надписей -> 2

#Рисуем картинку из файла:
img = PhotoImage(file = "fon.png")
canvas.create_image(0, 100, image=img, anchor=NW)
update_texts()

corona_centers = [] #координаты центров короны для отрисовки
coronas_tags = [] #координаты тегов короны для одновременной отрисовки
root.after(frame_rate, corona) #отрисовка короны -> 3
root.after(frame_rate, move_coronas) #движение короны -> 5
root.after(frame_rate, update_nose) #обновление носа -> 8

nose = nose1() # создаем нос -> 7
catcher = draw_catcher()#создаем человечка -> 6
mask_ris = mask1() # создаем маску -> 9

canvas.bind('<Left>', move_left) # движение влево -> 10
canvas.bind('<Right>', move_right) # движеине вправо -> 11
canvas.focus_set()

root.after(frame_rate, check_corona) # если заденем корону -> 12

tablets = [] #координаты центров таблеток для отрисовки
tablet_tags = [] #координаты тегов таблетки для одновременной отрисовки
root.after(frame_rate, create_tablet) # Рисуем таблетку -> 13
root.after(frame_rate, move_tablets) # Движение таблетки -> 14
root.after(frame_rate, check_tablet) # Если заденем таблетку -> 15

root.mainloop()
