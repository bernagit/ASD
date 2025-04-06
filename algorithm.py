import numpy as np
from node import Node
import time
import tracemalloc

class Solver:
    def __init__(self, matrix, instance_filename, debug = True, max_time = float('inf')):
        self.matrix = matrix
        self.instance_filename = instance_filename
        self.current_level = 0
        self.debug = debug
        self.stopped = False
        self.hypoteses_per_level = {}
        self.max_time = max_time

    def check_solution(self, solution):
        tmp = np.array([False] * self.matrix.shape[0], dtype=bool)
        for i in range(len(solution)):
            if solution[i]:
                tmp = np.logical_or(tmp, self.matrix[:,i])

        if np.sum(tmp) == self.matrix.shape[0]:
            print('Correct solution!')
        else:
            print('NOT correct solution!')

    def remove_empty_columns(self):
        """Rimuove le colonne vuote dalla matrice e restituisce il numero di colonne rimanenti."""
        self.deleted_columns_index = []
        M = self.matrix.shape[1]
        for i in range(self.matrix.shape[1] - 1, -1, -1):
            column = self.matrix[:, i].reshape(-1)
            if np.sum(column) == 0:
                self.matrix = np.delete(self.matrix, i, 1)
                self.deleted_columns_index.append(i)
        if self.debug:
            print(f"Colonne iniziali: {M}, Colonne finali: {self.matrix.shape[1]}")
        return self.matrix.shape[1]

    def remove_same_columns(self):
        counter = {}
        self.duplication_list = {}
        for i in range(self.matrix.shape[1]):
            column = self.matrix[:, i].reshape(-1)
            column_str = ''.join('1' if x else '0' for x in column)

            if column_str not in counter:
                counter[column_str] = []

            counter[column_str].append(i)

        tmp = []
        for key in counter:
            if len(counter[key]) <= 1:
                continue
            x = counter[key][1:]
            tmp.extend(x)
            self.duplication_list[counter[key][0]] = x
        tmp.sort()


        for i in range(len(tmp) - 1, -1, -1):
            self.matrix = np.delete(self.matrix, tmp[i], 1)

        return self.matrix.shape[1]

    def parse_matrix(self):
        """Prepara la matrice per la computazione."""
        self.remove_empty_columns()
        self.remove_same_columns()
        if self.debug:
            matrix_to_print = [[0 if x == False else 1 for x in row] for row in self.matrix]
            for row in matrix_to_print:
                print(row)

    def add_deleted_columns_to_solution(self, solution: np.ndarray):
        solution = solution.reshape(1, self.matrix.shape[1])

        tmp = []
        for key in self.duplication_list:
            tmp.extend(self.duplication_list[key])
        tmp.sort()

        # ripristina le colonne duplicate mettendo a False le righe duplicate
        for i in tmp:
            solution = np.insert(solution, i, [False], axis=1)

        original_indexes = []
        for i in range(len(solution[0])):
            if solution[0][i]:
                original_indexes.append(i)

        original_indexes.sort()

        arr = []
        for idx in range(len(solution[0])):
            if solution[0][idx] and idx in self.duplication_list:
                indexes = []
                indexes.append(idx)
                indexes.extend(self.duplication_list[idx])
                arr.append(indexes)
            elif solution[0][idx] and idx not in self.duplication_list:
                arr.append([idx])
    
        from itertools import product
        combinations = list(product(*arr))
        for combination in combinations:
            # skip the already present solution
            if list(combination) == original_indexes:
                continue
            new_row = np.zeros(len(solution[0]), dtype=bool)
            for i in range(len(combination)):
                new_row[combination[i]] = True
            solution = np.vstack([solution, new_row])
        

        for i in self.deleted_columns_index[::-1]:
            solution = np.insert(solution, i, [False], axis=1)

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

    def calculate_solutions(self, parse_matrix = True):
        tracemalloc.start()
        start = time.time()

        self.start_time = time.time()
        if parse_matrix:
            self.parse_matrix()
        else:
            self.deleted_columns_index = []

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
                elapsed_time = time.time() - start
                if elapsed_time > self.max_time:
                    print('Execution time exceeded 60 seconds, stopping computation.')
                    self.stopped = True
                    break
                if self.stopped:
                    return

                h = self.current[i]
                if h.is_solution():
                    if self.debug:
                        print(f'Found {len(self.solutions) + 1} solution{'s' if len(self.solutions) > 0 else ''}')
                    right_solution = self.add_deleted_columns_to_solution(h.value)
                    # self.solutions.append(right_solution)
                    self.solutions.extend(right_solution)
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