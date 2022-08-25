import collections

import numpy as np
from enums.moves import MovesN2, MovesN3
from rubik import Rubik
from search_methods.node import Node


class Manager:
    BORDER_DTYPE = [('heuristicValue', float), ('node', Node)]

    def __init__(self, method, rubik, rubikUtils):
        self.method = method
        self.visited = []
        self.n = rubik.n
        self.border = collections.deque([Node(rubik.cube, None, None, 0, self.method.calculate_weight, self.n)])
        self.deepsOfStates = {}
        self.rubikUtils = rubikUtils

    def solve(self):
        i = 0
        possibleMoves = np.array(list(map(int, MovesN3 if self.n == 3 else MovesN2)))
        # para root
        node = self.border.pop()
        rubik = Rubik(self.n, self.rubikUtils, node.state)

        while not rubik.is_solved() and (len(self.border) > 0 or len(self.visited) == 0):

            if rubik.to_string() not in self.deepsOfStates or self.deepsOfStates[
                rubik.to_string()] > node.deep:
                # Solo expando cuando no he visitado el estado o si es menos profundo que cuando lo visite
                self.deepsOfStates[rubik.to_string()] = node.deep
                if node.lastMovement is not None:
                    # chequeo que no sea root node
                    nextMoves = np.delete(possibleMoves,
                                              np.where(int((node.lastMovement + (len(MovesN3) / 2)) % len(MovesN3))))
                else: nextMoves = possibleMoves
                np.random.shuffle(nextMoves)

                newBorders = []
                for nextMove in nextMoves:
                    newNode = Node(
                        rubik.move(nextMove),
                        node, nextMove, node.deep + 1,
                        self.method.calculate_weight, self.n)
                    node.add_children(newNode)
                    newBorders.append(newNode)
                self.border = self.method.insert_nodes(self.border, newBorders)

            self.visited.append(node)
            node = self.border.popleft()
            rubik = Rubik(self.n, self.rubikUtils, node.state)
            i += 1
            if i % 10000 == 0:
                print(i, node.deep)

        if rubik.is_solved():
            self.visited.append(node)
            print("Nodos expandidos: " + str(len(self.visited)))
            print("Nodos borde: " + str(len(self.border)))
            print("Profundidad: " + str(node.deep))
            return node
        else:
            raise ValueError('No solution found')