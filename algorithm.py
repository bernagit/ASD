import numpy as np
from node import Node
import time
import tracemalloc

class Solver:
    def __init__(self, matrix, instance_filename, debug = True):
        self.matrix = matrix
        self.instance_filename = instance_filename
        self.current_level = 0
        self.debug = debug
        self.stopped = False
        self.hypoteses_per_level = {}

    def check_solution(self, solution):
        tmp = np.array([False] * self.matrix.shape[0], dtype=bool)
        for i in range(len(solution)):
            if solution[i]:
                tmp = np.logical_or(tmp, self.matrix[:,i])

        if np.sum(tmp) == self.matrix.shape[0]:
            print('Correct solution!')

        else:
            print('NOT correct solution!')

    def parse_matrix(self):
        self.deleted_columns_index = []
        M = self.matrix.shape[1]
        for i in range(self.matrix.shape[1] - 1, 0, -1):
            column = self.matrix[:, i].reshape(-1)
            if np.sum(column) == 0:
                self.matrix = np.delete(self.matrix, i, 1)
                self.deleted_columns_index.append(i)

        if self.debug:
            print(f'Start columns: {M} - End columns: {self.matrix.shape[1]}')
            matrix_to_print = [[0 if x == False else 1 for x in row] for row in self.matrix]
            
            for row in matrix_to_print:
                print(row)

    def add_deleted_columns_to_solution(self, solution):
        solution = solution.reshape(1, self.matrix.shape[1])
        for i in self.deleted_columns_index[::-1]:
            solution = np.insert(solution, i, [False], axis=1)

        solution = solution.reshape(-1)
        return solution

    def get_used_memory(self):
        return tracemalloc.get_traced_memory()

    def permute_rows(self):
        permuted_indices = np.random.permutation(self.matrix.shape[0])
        self.matrix = self.matrix[permuted_indices]
        self.permuted_row_indices = permuted_indices

    def permute_columns(self):
        permuted_indices = np.random.permutation(self.matrix.shape[1])
        self.matrix = self.matrix[:,permuted_indices]
        self.permuted_column_indices = permuted_indices

    def get_solutions_without_permutation(self):
        right_solutions = []
        for sol in self.solutions:
            right_solution = np.zeros_like(sol).reshape(1, len(sol))
            right_solution[:, self.permuted_column_indices] = sol
            right_solution = right_solution.reshape(-1)
            right_solutions.append(right_solution)

        return right_solutions

    def generate_children(self, h: Node):
        """
        Generate children of hypothesis h
        """
        children = []
        if h.level == 0:
            for i in range(len(h.value)):
                hp = Node(h.value)
                hp.value[i] = True
                hp.update_level()
                hp._set_fields(self.matrix)
                children.append(hp)
            return children
        
        hp = self.current[0]
        pos = 0
        for i in range(h.lm()):
            h1 = Node(h.value)
            h1.value[i] = True
            h1.update_level()
            h1._set_fields(self.matrix)

            h1.propagate(h)

            hi = h.initial(h1, self.matrix)
            hf = h.final(h1, self.matrix)

            try:
                pos = self.current.index(hi)
            except:
                pos = 0
            hp = self.current[pos]

            cont = 0
            while hp <= hi and hp >= hf:
                if hp.distance(h1) == 1 and hp.distance(h) == 2:
                    h1.propagate(hp)
                    cont += 1
                
                pos += 1
                hp = self.current[pos]
            
            if cont == h.level:
                children.append(h1)
        
        return children

    def calculate_solutions(self):
        tracemalloc.start()

        self.start_time = time.time()
        self.parse_matrix()

        h0 = Node([False] * len(self.matrix[0]))
        h0.update_level()
        h0._set_fields(self.matrix)

        self.current = [h0]
        self.solutions = []

        max_level = max(self.matrix.shape)
        self.current_level = 0
        while len(self.current) > 0 and self.current_level <= max_level:
            self.hypoteses_per_level[self.current_level] = len(self.current)
            if self.debug:
                print(f'Starting level {self.current_level} with {len(self.current)} hypotesis')
            next = []

            i = 0
            n = len(self.current)
            while i < n:
                if self.stopped:
                    return

                h = self.current[i]
                if h.is_solution():
                    if self.debug:
                        print(f'Found {len(self.solutions) + 1} solution{'s' if len(self.solutions) > 0 else ''}')
                    right_solution = self.add_deleted_columns_to_solution(h.value)
                    self.solutions.append(right_solution)
                    self.current.pop(i)
                    i -= 1
                    n -= 1

                elif h.level == 0:
                    next.extend(self.generate_children(h))
                elif h.lm() != 0:
                    hs = h.global_initial(self.matrix)
                    tmp = [c for c in self.current if c <= hs]

                    i -= (len(self.current) - len(tmp))
                    n = len(tmp)
                    self.current = tmp
                    hp = self.current[0]

                    if hp != h:
                        children = self.generate_children(h)
                        next.extend(children)
                        next.sort(reverse=True)
                    
                i += 1
            
            self.current = next
            self.current_level += 1

        self.execution_time = time.time() - self.start_time