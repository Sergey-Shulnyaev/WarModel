from random import randint

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

class World():
    def __init__(self, vertexes=[], edges=[]):
        # vertexes - вершины, заданные в виде
        self.vertexes = vertexes
        self.edges = edges

    def show_graph(self):
        for i in self.vertexes:
            print(i.get_number(), i.get_neighbors())

    def generate_vertexes(self, quantity=10, min_w=1, max_w=10):
        for i in range(quantity):
            # генерация вершины
            v = Vertex(weight=randint(min_w, max_w))
            # добавление к вершинам рёбер
            if i == 0:
                v.create_neighbors([1])
            elif i == quantity-1:
                v.create_neighbors([quantity-2])
            else:
                v.create_neighbors([i-1, i+1])
            self.vertexes.append(v)

        self.generate_edges()

    def generate_edges(self):
        """
        Генерирует рёбра по текущим вершинам
        :return:
        """
        self.edges = []
        for i in self.vertexes:
            neigh = i.get_neighbors()
            for j in neigh:
                edge = [i.get_number(), j]
                edge.sort()
                self.edges.append(edge)
        self.edges = del_dub(self.edges)

    def generate_countries(self):
        None

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

    def __init__(self, vertexes=[]):
        self.vertexes = vertexes
        self.neighbor_vertexes = self.create_neighbor_vertexes()

    def create_neighbor_vertexes(self):
        """
        Принимаем список всех вершин, смотрим всех соседей
        :return: список соседей к данным вершинам
        """
        neighbor_vertexes = []
        for i in self.vertexes:
            neighbor_vertexes.extend(i.get_neighbors)
        return del_dub(neighbor_vertexes)

    def create_neighbors(self):
        """
        Будет возвращать список текущий соседей(государств), для данного
        :return:
        """
        None


