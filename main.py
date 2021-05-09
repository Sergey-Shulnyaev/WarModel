from classes import *

from kivy.app import App, Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.actionbar import ActionDropDown
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.treeview import TreeView
from kivy.graphics import Color, Ellipse, Bezier, Line
from functools import partial

Builder.load_file("base.kv")

class BlackLabel(Label):
    #Label с вбитым черным цветом текста
    def __init__(self, *args, **kwargs):
        super(BlackLabel, self).__init__(*args, **kwargs)
        self.color = 255, 255, 255, 1

class CircleButton(Button):
    def __init__(self, circle_color=(0, 0, 0, 1), *args, **kwargs):
        super(CircleButton, self).__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.circle_color = circle_color
        self.bind(on_press=self.press_color)
        self.bind(on_release=self.release_color)

        #self.canvas.clear()
        self.background_color = (0,0,0,0)
        with self.canvas.before:
            Color(rgba=self.circle_color)
            Ellipse(pos=self.pos, size=self.size)



    def press_color(self, mes):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(0, 255, 0, 1))
            Ellipse(pos=self.pos, size=self.size)

    def release_color(self, mes):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.circle_color)
            Ellipse(pos=self.pos, size=self.size)

class Edge(Widget):
    def __init__(self, points=[], loop=False, *args, **kwargs):
        super(Edge, self).__init__(*args, **kwargs)
        self.points = points
        self.loop = loop
        with self.canvas.before:
            Color(.2, 0.2, .2, 1.0)
            Line(width=3,
                 points=self.points)

class MainScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        self.gen_env()
        #self.gen_map()
        self.edges = list()
        self.countries = list()
        self.player = None

    def gen_env(self):
        width, height = Window.size

        # Заголовок
        self.text1 = BlackLabel(size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                pos=(50, height - 30))
        self.text1.text = 'Количество стран-вершин'
        self.add_widget(self.text1)

        # Окно поиска
        self.input1 = TextInput(multiline=False,
                                size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                pos=(200, height - 30),
                                text='1')
                                # on_text_validate=print)
        self.add_widget(self.input1)

        # Генерация карты вершин
        self.generate_map = Button(
                                size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                text='Генерировать',
                                pos=(310, height - 30)
        )
        self.generate_map.bind(on_release=self.gen_map)
        self.add_widget(self.generate_map)

        #gamma
        self.gamma_text = BlackLabel(size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                pos=(450, height - 30))
        self.gamma_text.text = 'Введите гамма'
        self.add_widget(self.gamma_text)

        # Окно ввода гаммы
        self.input_gamma = TextInput(multiline=False,
                                size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                pos=(550, height - 30),
                                text='2')
        # on_text_validate=print)
        self.add_widget(self.input_gamma)

        # ввод гаммы
        self.gamma_button = Button(size_hint=(None, None),
                                  width=130,
                                  height=30,
                                  font_size=14,
                                  text='Изменить гамма',
                                  pos=(550, height - 70))
        self.gamma_button.bind(on_release=self.change_gamma)
        self.add_widget(self.gamma_button)

        # Заголовок
        self.play_button= Button(size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                text='Играть за',
                                pos=(50, height - 70))
        self.play_button.bind(on_release=self.add_player)
        self.add_widget(self.play_button)

        # Окно выбора игрока
        self.dropdown_1 = DropDown()
        self.country_change = Button(
            size_hint=(None, None),
            width=100,
            height=30,
            font_size=14,
            text='',
            pos=(150, height - 70)
        )
        self.country_change.bind(on_release=self.update_dropdown_1)
        # Действие в момент выбора
        # self.dropdown.bind(on_select=lambda instance, x: setattr(self.search, 'text', x))
        self.add_widget(self.country_change)

        self.model_game_btn = Button(
            size_hint=(None, None),
            width=100,
            height=30,
            font_size=14,
            text='Играть раунд',
            pos=(310, height - 70)
        )
        self.model_game_btn.bind(on_release=partial(self.model_game, 0))
        self.add_widget(self.model_game_btn)

        # Кнопка атаки
        self.attack = Button(size_hint=(None, None),
                             width=100,
                             height=30,
                             font_size=14,
                             text='Атаковать',
                             pos=(50, height - 110))
        self.attack.bind(on_release=self.country_conquest)
        self.add_widget(self.attack)

        # Окно выбора игрока
        self.dropdown_2 = DropDown()
        self.attack_country = Button(
            size_hint=(None, None),
            width=100,
            height=30,
            font_size=14,
            text='',
            pos=(150, height - 110)
        )
        self.attack_country.bind(on_release=self.update_dropdown_2)
        # Действие в момент выбора
        # self.dropdown.bind(on_select=lambda instance, x: setattr(self.search, 'text', x))
        self.add_widget(self.attack_country)

        # Кнопка паса
        self.passs = Button(size_hint=(None, None),
                             width=100,
                             height=30,
                             font_size=14,
                             text='Пасовать',
                             pos=(50, height - 150))
        self.passs.bind(on_release=self.pass_round)
        self.add_widget(self.passs)

    def change_gamma(self, *args):
        global my_w
        my_w.gamma = float(self.input_gamma.text)

    def update_dropdown_1(self, struct):
        if self.player:
            return -1
        global my_w
        self.dropdown_1.dismiss()
        self.dropdown_1=DropDown()
        self.dropdown_1.max_height = Window.size[1] * 0.7

        #Здесь будет возвращаться список стран
        for country in my_w.country_list:
            btn = Button(text=f'{country.get_number()}', size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dropdown_1.select(btn.text))
            self.dropdown_1.add_widget(btn)

        self.dropdown_1.open(struct)
        self.dropdown_1.bind(on_select=lambda instance, x: setattr(self.country_change, 'text', x))

        self.attack_country.text=''

    def update_dropdown_2(self, struct):
        global my_w
        # Здесь будет возвращаться список соседей для выбранной страны
        if self.country_change.text!='':
            self.dropdown_2.dismiss()
            self.dropdown_2 = DropDown()
            self.dropdown_2.max_height = Window.size[1] * 0.7

            number = int(self.country_change.text)
            your_country = my_w.search_country_by_number(number)

            for neigh in your_country.get_neighbors():
                btn = Button(text=f'{neigh.get_number()}', size_hint_y=None, height=30)
                btn.bind(on_release=lambda btn: self.dropdown_2.select(btn.text))
                self.dropdown_2.add_widget(btn)

            self.dropdown_2.open(struct)
            self.dropdown_2.bind(on_select=lambda instance, x: setattr(self.attack_country, 'text', x))

    def country_conquest(self, *args):
        global my_w
        at_number = int(self.country_change.text)
        def_number = int(self.attack_country.text)
        if at_number!='' and def_number!='':
            att = my_w.search_country_by_number(at_number)
            deff = my_w.search_country_by_number(def_number)
            my_w.attack(att, deff)
            self.attack_country.text=''
            self.update_map()
        self.model_game(flag=1)

    def pass_round(self, *args):
        self.model_game(flag=1)

    def model_game(self, flag=0, *args):
        global my_w
        #создаём очередь
        if flag==0:
            self.queue = my_w.generate_queue()
            self.i = 0
        while self.i < len(self.queue):
            play_country = self.queue[self.i]
            if self.player == play_country:
                self.update_map()
                break

            loser = my_w.play(play_country)
            # создаём новую очередь, если что-то делаем
            if loser:
                new_queue = list()
                for country in self.queue:
                    if country != loser:
                        new_queue.append(country)
                self.queue = new_queue
            # проверяем сместилась ли она так, что элемент с текущим номером стал другим, если да, то ничего не делаем,
            # если нет, то i++
            if self.i < len(self.queue):
                if play_country == self.queue[self.i]:
                    self.i += 1

        self.update_map()

    def add_player(self, *args):
        if self.country_change.text !='':
            self.player = self.country_change.text

    def gen_map(self, *args):
        global my_w
        quantity = int(self.input1.text)

        my_w.zeroize()
        my_w.generate_vertexes(quantity=quantity)
        my_w.generate_countries()
        self.update_map()

    def update_map(self, *args):
        coordinate_vert_dict = dict()
        k = 0
        for vert in my_w.vertexes:
            coordinate_vert_dict[vert.get_number()] = (20 + k * 80, 200)
            k += 1
        defalt_size = 50
        # очистка ребёр с экрана
        for edge in self.edges:
            self.remove_widget(edge)
        self.edges = list()
        for edge in my_w.edges:
            x1, y1 = coordinate_vert_dict[edge[0]]
            x2, y2 = coordinate_vert_dict[edge[1]]
            kivy_edge = Edge([x1 + defalt_size // 2, y1 + defalt_size // 2,
                              x2 + defalt_size // 2, y2 + defalt_size // 2])
            self.edges.append(kivy_edge)
            self.add_widget(kivy_edge)

        for country in self.countries:
            # print(country)
            self.remove_widget(country)
        self.countries = list()
        for country in my_w.country_list:
            for vert in country.vertexes:
                cb = CircleButton(text=f'{vert.weight}',
                                  circle_color=country.color, font_size=25,
                                  pos=coordinate_vert_dict[vert.get_number()],
                                  size=(defalt_size, defalt_size))
                self.countries.append(cb)
                self.add_widget(cb)

class MainApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        #Window.size = (720 / 2.2, 1520 / 2.2)
        # Window.fullscreen = True

        # Create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))

        return self.sm


if __name__ == '__main__':
    global mapp, my_w

    my_w = World(gamma=2)
    mapp = MainApp()
    mapp.run()