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

Builder.load_file("base.kv")

class BlackLabel(Label):
    #Label с вбитым черным цветом текста
    def __init__(self, *args, **kwargs):
        super(BlackLabel, self).__init__(*args, **kwargs)
        self.color = 255, 255, 255, 1

class CircleButton(Button):
    def __init__(self, *args, **kwargs):
        super(CircleButton, self).__init__(*args, **kwargs)
        self.size_hint = (None, None)

        self.pos = (200, 200)
        self.size = (50, 50)
        self.bind(on_press=self.press_color)
        self.bind(on_release=self.release_color)

        #self.canvas.clear()
        self.background_color = (0,0,0,0)
        with self.canvas.before:
            Color(rgb=(0, 0, 0))
            Ellipse(pos=self.pos, size=self.size)



    def press_color(self, mes):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(0, 255, 0, 1))
            Ellipse(pos=self.pos, size=self.size)

    def release_color(self, mes):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(0, 0, 0, 1))
            Ellipse(pos=self.pos, size=self.size)

class Edge(Widget):
    def __init__(self, points=[], loop=False, *args, **kwargs):
        super(Edge, self).__init__(*args, **kwargs)
        self.points = points
        self.loop = loop
        with self.canvas.before:
            Color(1.0, 0.0, 1.0)
            Line(width=3,
                 points=self.points)

class MainScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)

        width, height = Window.size

        # Заголовок
        self.text1 = BlackLabel(size_hint=(None, None),
                               width=100,
                               height=30,
                               font_size=14,
                               pos=(50, height-30))
        self.text1.text = 'Количество стран-вершин'
        self.add_widget(self.text1)

        # Окно поиска
        self.input1 = TextInput(multiline=False,
                                size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                pos=(200, height - 30),
                                on_text_validate=print)
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
        self.add_widget(self.generate_map)

        # Заголовок
        self.text2 = BlackLabel(size_hint=(None, None),
                               width=100,
                               height=30,
                               font_size=14,
                               pos=(50, height - 70))
        self.text2.text = 'Играть за'
        self.add_widget(self.text2)

        # Окно выбора игрока
        self.dropdown = DropDown()
        self.country_change = Button(
                                size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                text='1',
                                pos=(150, height - 70)
                                )
        self.country_change.bind(on_release=self.update_dropdown_1)
        # Действие в момент выбора
        # self.dropdown.bind(on_select=lambda instance, x: setattr(self.search, 'text', x))
        self.add_widget(self.country_change)

        # Заголовок
        self.attack = Button(size_hint=(None, None),
                                width=100,
                                height=30,
                                font_size=14,
                                text='Атаковать',
                                pos=(50, height - 110))
        self.add_widget(self.attack)

        # Окно выбора игрока
        self.dropdown_2 = DropDown()
        self.attack_country = Button(
            size_hint=(None, None),
            width=100,
            height=30,
            font_size=14,
            text='1',
            pos=(150, height - 110)
        )
        self.attack_country.bind(on_release=self.update_dropdown_2)
        # Действие в момент выбора
        # self.dropdown.bind(on_select=lambda instance, x: setattr(self.search, 'text', x))
        self.add_widget(self.attack_country)

    def update_dropdown_1(self, struct):
        self.dropdown.dismiss()
        self.dropdown=DropDown()
        self.dropdown.max_height = Window.size[1]*0.7

        #Здесь будет возвращаться список
        #Кнопки будут создавать маршрут уже до цели
        for index in range(40):
            btn = Button(text=f'{index}', size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.dropdown.open(struct)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.country_change, 'text', x))

    def update_dropdown_2(self, struct):
            self.dropdown_2.dismiss()
            self.dropdown_2 = DropDown()
            self.dropdown_2.max_height = Window.size[1] * 0.7

            # Здесь будет возвращаться список
            # Кнопки будут создавать маршрут уже до цели
            for index in range(40):
                btn = Button(text=f'{index}', size_hint_y=None, height=30)
                btn.bind(on_release=lambda btn: self.dropdown_2.select(btn.text))
                self.dropdown_2.add_widget(btn)

            self.dropdown_2.open(struct)
            self.dropdown_2.bind(on_select=lambda instance, x: setattr(self.attack_country, 'text', x))

class GameScreen(MainScreen):
    """
    Наследуем экран со всеми надписями
    """
    def __init__(self, *args, **kwargs):
        super(GameScreen, self).__init__(*args, **kwargs)
        global my_w
        self.s1 = CircleButton(text="jenkins", color=(0,0,0), font_size=25)
        self.add_widget(self.s1)

        self.s2 = Edge([100,200,200,200,100,300])
        self.add_widget(self.s2)


class MainApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        #Window.size = (720 / 2.2, 1520 / 2.2)
        # Window.fullscreen = True

        # Create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(GameScreen(name='main'))

        return self.sm


if __name__ == '__main__':
    global mapp, my_w
    my_w = World()
    my_w.generate_vertexes()
    my_w.show_graph()
    mapp = MainApp()
    mapp.run()