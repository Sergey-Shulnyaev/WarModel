from random import randint, random

def del_dub(l):
    """
    Удаляет дубликаты из списка
    :param l:
    :return:
    """
    new_l = list()
    for i in l:
        it = -1
        for j in new_l:
            if j == i:
                it = j
                break
        if it == -1:
            new_l.append(i)
    return new_l

def randomize_list(l):
    length = len(l)
    new_l = l.copy()
    for i in range(length):
        j = randint(i, length-1)
        a = new_l[i]
        new_l[i] = new_l[j]
        new_l[j] = a
    return new_l

class World():
    def __init__(self, vertexes=[], edges=[]):
        # vertexes - вершины, заданные в виде
        self.vertexes = vertexes
        self.edges = edges
        self.country_list = list()

    def show_graph(self):
        for i in self.country_list:
            print(i.get_number(), i.get_neighbors())

    def generate_vertexes(self, quantity=10, min_w=1, max_w=10):
        for i in range(quantity):
            # генерация вершины
            vert = Vertex(weight=randint(min_w, max_w))
            self.vertexes.append(vert)
        for i in range(quantity):
            # добавление к вершинам рёбер
            if i == 0:
                if len(self.vertexes)==1:
                    neigh = []
                else:
                    neigh = [self.vertexes[1]]
            elif i == quantity - 1:
                neigh = [self.vertexes[quantity - 2]]
            else:
                neigh = [self.vertexes[i - 1], self.vertexes[i + 1]]
            self.vertexes[i].create_neighbors(neigh)

        self.generate_edges()

    def generate_edges(self):
        """
        Генерирует рёбра по текущим вершинам
        :return:
        """
        self.edges = []
        for i in self.vertexes:
            neigh = [vert.get_number() for vert in i.get_neighbors()]
            for j in neigh:
                edge = [i.get_number(), j]
                edge.sort()
                self.edges.append(edge)
        self.edges = del_dub(self.edges)

    def generate_countries(self):
        if self.vertexes == list():
            return -1
        self.country_list = list()
        self.country_list.append(Country([self.vertexes[0]], color=(1,0,0,1)))
        for vert in self.vertexes[1:]:
            self.country_list.append(Country([vert],
                                             color=(random(), random(), random(), 1)))
        for country in self.country_list:
            country.create_neighbors()

    def conquest(self, winner, loser):
        """
        Добавляю вершины в первого, обновляю первого, удаляю второго
        :param winner:
        :param loser:
        :return:
        """
        winner.vertexes.extend(loser.vertexes)
        loser.zeroize()
        new_country_list = list()
        for country in self.country_list:
            if country != loser:
                new_country_list.append(country)

        self.country_list = new_country_list
        for country in self.country_list:
            country.create_neighbor_vertexes()
            country.create_neighbors()

    def search_country_by_number(self, number):
        for country in self.country_list:
            if number == country.get_number():
                your_country = country
                break
        return your_country

    def generate_queue(self):
        self.queue = randomize_list(self.country_list)

    def zeroize(self):
        self.vertexes = list()
        self.edges = list()
        self.country_list = list()
        Vertex.vertex_list = list()
        Country.countries = list()

class Vertex():
    # список вершин, в котором лежат все оставшиеся
    vertex_list = list()

    def __init__(self, weight=0, neighbors=[]):
        """

        :param weight: количество ресурсов в данной вершине
        :param neighbors: соседние вершины, с которыми есть связь
        """
        if self.vertex_list == []:
            number_counter = 0
        else:
            number_counter = self.vertex_list[-1].number + 1
        self.number = number_counter
        self.vertex_list.append(self)
        self.weight = weight
        self.neighbors = neighbors

    def get_number(self):
        return self.number

    def get_neighbors(self):
        return self.neighbors

    def create_neighbors(self, neighbors):
        self.neighbors = neighbors

class Country():
    countries = list()

    def __init__(self, vertexes=[], color=(0,0,0)):
        if self.countries == []:
            number_counter = 0
        else:
            number_counter = self.countries[-1].number + 1
        self.number = number_counter
        self.color = color

        self.neighbor_countries = list()
        self.neighbor_vertexes = list()
        self.vertexes = vertexes

        self.countries.append(self)
        self.create_neighbor_vertexes()

    def create_neighbor_vertexes(self):
        """
        Принимаем список всех вершин, смотрим всех соседей
        :return: список соседей к данным вершинам
        """
        neighbor_vertexes = []
        for i in self.vertexes:
            neighbor_vertexes.extend(i.get_neighbors())
        neighbor_vertexes = del_dub(neighbor_vertexes)
        # без вершин, содержащихся в государстве
        updated_neighbor_vertexes = []
        for vert in neighbor_vertexes:
            flag = 1
            for country_vert in self.vertexes:
                if vert == country_vert:
                    flag = 0
                    break
            if flag == 1:
                updated_neighbor_vertexes.append(vert)
        self.neighbor_vertexes = updated_neighbor_vertexes

    def create_neighbors(self):
        """
        Будет возвращать список текущий соседей(государств), для данного
        :return:
        """
        empty_set = set()
        self.neighbor_countries = list()
        for country in self.countries:
            set1 = set([i.get_number() for i in self.neighbor_vertexes])
            set2 = set([i.get_number() for i in country.vertexes])
            if set1 & set2 != empty_set:
                country_number = country.get_number()
                self.neighbor_countries.append(country)
        self.neighbor_countries = del_dub(self.neighbor_countries)

    def get_number(self):
        return self.number

    def get_neighbors(self):
        return self.neighbor_countries

    def get_wealth(self):
        sum = 0
        for vertex in self.vertexes:
            sum += vertex.weight
        return sum

    def zeroize(self):
        self.neighbor_countries = list()
        self.neighbor_vertexes = list()
        self.vertexes = list()

"""my_w = World()
my_w.generate_vertexes()
my_w.generate_countries()
my_w.show_graph()"""



