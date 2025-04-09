import numpy as np
from node import Node
import time
import tracemalloc

class Option():
    def __init__(self,
                 debug=False,
                 delete_zeros=False,
                 delete_duplicates=False,
                 max_time=float('inf'),
                 permute_rows=False,
                 permute_columns=False,
                 permute_columns_desc=False,
                 permute_columns_asc=False):
        self.debug = debug
        self.delete_zeros = delete_zeros
        self.delete_duplicates = delete_duplicates
        self.max_time = max_time
        self.permute_rows = permute_rows
        self.permute_columns = permute_columns
        self.permute_columns_desc = permute_columns_desc
        self.permute_columns_asc = permute_columns_asc
class Solver:
    def __init__(self, matrix, instance_filename, option: Option=Option()):
        self.matrix = matrix
        self.instance_filename = instance_filename
        self.current_level = 0
        self.stopped = False
        self.hypoteses_per_level = {}
        self.max_time = option.max_time
        self.option = option

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
        if self.option.debug:
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
        if self.option.delete_zeros:
            self.remove_empty_columns()
        if self.option.delete_duplicates:
            self.remove_same_columns()
        if self.option.debug:
            matrix_to_print = [[0 if x == False else 1 for x in row] for row in self.matrix]
            for row in matrix_to_print:
                print(row)

    def add_deleted_columns_to_solution(self, solution: np.ndarray):
        solution = solution.reshape(1, self.matrix.shape[1])

        if self.option.delete_duplicates:
            tmp = []
            for key in self.duplication_list:
                tmp.extend(self.duplication_list[key])
            tmp.sort()

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
            num_of_combinations = 1
            for element in arr:
                num_of_combinations *= len(element)
            
            if self.option.debug:
                print(f'Number of combinations: {num_of_combinations}')
            if num_of_combinations > 1000000:
                print(f'Warning: number of combinations is too high ({num_of_combinations}), skipping this step.')
                self.stopped = True

            if not self.stopped:
                combinations = list(product(*arr))

                # remove the already present solution from the combinations
                combinations.remove(tuple(original_indexes))
                
                start = time.time()
                i = 0
                for combination in combinations:
                    if i % 1000 == 0:
                        elapsed_time = time.time() - start
                        print(f'Adding combination {i} of {len(combinations)}')
                        if elapsed_time > self.max_time:
                            print(f'Execution time exceeded {self.max_time} seconds, stopping computation.')
                            self.stopped = True
                            return
                    new_row = np.zeros(len(solution[0]), dtype=bool)
                    new_row[list(combination)] = True
                    solution = np.vstack([solution, new_row])
                    i += 1

                if self.option.debug:
                    print(f'Added {len(combinations)} new solutions by combining the duplicated columns')

        if self.option.delete_zeros:
            for i in self.deleted_columns_index[::-1]:
                solution = np.insert(solution, i, [False], axis=1)

        return solution

    def get_used_memory(self):
        return tracemalloc.get_traced_memory()

    def permute_rows(self):
        if self.option.permute_rows:
            permuted_indices = np.random.permutation(self.matrix.shape[0])
            self.matrix = self.matrix[permuted_indices]
            self.permuted_row_indices = permuted_indices

    def permute_columns(self):
        if self.option.debug:
            start= time.time()
        if self.option.permute_columns:
            permuted_indices = np.random.permutation(self.matrix.shape[1])
            self.matrix = self.matrix[:,permuted_indices]
            self.permuted_column_indices = permuted_indices
        elif self.option.permute_columns_desc:
            # Permutazione delle colonne in base al numero di '1'
            column_sums = np.sum(self.matrix, axis=0)  # Somma degli elementi di ogni colonna
            permuted_indices = np.argsort(-column_sums)  # Ordina in ordine decrescente
            self.matrix = self.matrix[:, permuted_indices]
            self.permuted_column_indices = permuted_indices  # Salva gli indici permutati
            if self.option.debug:
                print(f"Colonne permutate in base al numero di '1': {permuted_indices}")
        elif self.option.permute_columns_asc:
            # Permutazione delle colonne in base al numero di '0'
            column_sums = np.sum(self.matrix, axis=0)
            permuted_indices = np.argsort(column_sums)  # Ordina in ordine crescente
            self.matrix = self.matrix[:, permuted_indices]
            self.permuted_column_indices = permuted_indices  # Salva gli indici permutati
            if self.option.debug:
                print(f"Colonne permutate in base al numero di '0': {permuted_indices}")
        if self.option.debug:
            end = time.time()
            elapsed_time = end - start
            print(f"Tempo di esecuzione per la permutazione delle colonne: {elapsed_time:.4f} secondi")

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

    def preprocess_matrix(self):
        self.parse_matrix()
        self.permute_columns()
        self.permute_rows()

    def calculate_solutions(self, firstSolution=False, preprocess=True):
        tracemalloc.start()
        start = time.time()

        if preprocess:
            self.preprocess_matrix()
        
        self.start_time = time.time()

        h0 = Node([False] * len(self.matrix[0]))
        h0.update_level()
        h0._set_fields(self.matrix)

        self.current = [h0]
        self.solutions = []

        max_level = max(self.matrix.shape)
        self.current_level = 0
        while len(self.current) > 0 and self.current_level <= max_level:
            self.hypoteses_per_level[self.current_level] = len(self.current)
            if self.option.debug:
                print(f'Starting level {self.current_level} with {len(self.current)} hypotesis')
            next = []

            i = 0
            n = len(self.current)
            while i < n:
                elapsed_time = time.time() - start
                if elapsed_time > self.max_time:
                    print(f'Execution time exceeded {self.max_time} seconds, stopping computation.')
                    self.stopped = True
                    break
                if self.stopped:
                    return

                h = self.current[i]
                if h.is_solution():
                    if self.option.debug:
                        time_solution = time.time() - start
                        print(f'Found {len(self.solutions) + 1} solution{"s" if len(self.solutions) > 0 else ""} at time {time_solution:.2f} seconds')

                    if firstSolution:
                        if len(self.solutions) == 0:
                            self.solution_times = (time.time() - self.start_time, self.solution_times[1])
                        elif len(self.solutions) == 1:
                            self.solution_times = (self.solution_times[0], time.time() - self.start_time)
                            self.execution_time = time.time() - self.start_time
                            return
                        
                    right_solution = self.add_deleted_columns_to_solution(h.value)
                    
                    if self.stopped:
                        return

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