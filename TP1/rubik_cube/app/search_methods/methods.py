import bisect
from time import sleep

import numpy as np
from sortedcontainers import SortedList
from collections import deque
from search_methods.node import Node


class Method(object):
    def __init__(self):
        pass

    def insert_nodes(self, nodes):
        pass

    def calculate_heuristic(self, node, n):
        return 0

    def pop(self):
        pass


class BFS(Method):
    def __init__(self):
        self.border = deque()

    def insert_nodes(self, nodes):
        for node in nodes:
            self.border.append(node)

    def pop(self):
        return self.border.popleft()

class DFS(Method):
    def __init__(self):
        self.border = deque()

    def insert_nodes(self, nodes):
        # recibe ordenados de mas viejos a mas nuevos, por eso el reverse
        for node in nodes[::-1]:
            self.border.appendleft(node)


    def pop(self):
        return self.border.popleft()


class LocalGreedy(Method):
    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic
        self.border = deque()

    def insert_nodes(self, nodes):
        sorted_nodes = sorted(nodes, key=lambda node: node.heuristic)
        for node in sorted_nodes[::-1]:
            self.border.appendleft(node)

    def calculate_heuristic(self, node, n):
        return self.heuristic(node.state, n)

    def pop(self):
        return self.border.popleft()

class GlobalGreedy(Method):
    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic
        self.border = SortedList(key=lambda node: node.heuristic)

    def insert_nodes(self, nodes):
        self.border.update(nodes)

    def calculate_heuristic(self, node, n):
        return self.heuristic(node.state, n)

    def pop(self):
        return self.border.pop(0)

class AStar(Method):
    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic
        self.border = SortedList(key=lambda node: (node.weight, node.heuristic))

    def insert_nodes(self, nodes):
        self.border.update(nodes)

    def calculate_heuristic(self, node, n):
        return self.heuristic(node.state, n)

    def pop(self):
        return self.border.pop(0)

class IDDFS(Method):
    def __init__(self):
        super().__init__()
        self.depth_step = 2
        self.sum_count = 0

    def insert_nodes(self, nodes):
        self.sum_count = 0
        for node in nodes[::-1]:
            if node.depth <= self.depth_step:
                self.border.appendleft(node)
            else:
                self.border.append(node)

        #Bueno lo pusheo pq lo unico que falta es aumentar el depth_step, pero no se puede meter recursivo pq no tengo los nodos de los arboles antiguos
        #Si a alguno se le ocurre algo :8

