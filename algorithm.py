import numpy as np
from collections import deque
from node import Node


def check(h: Node):
    """
    Check if hypothesis h is valid
    """
    return h.vector.sum() == len(h.vector)


def generate_children(h: Node, matrix: np.ndarray):
    """
    Generate children of hypothesis h
    """
    children = []
    if h.level == 0:
        for i in range(len(h.value)):
            hp = Node(h.value)
            hp.value[i] = True
            hp.update_level()
            hp._set_fields(matrix)
            children.append(hp)
        return children
    
    hp = current[0]
    pos = 0
    for i in range(h.lm()):
        h1 = Node(h.value)
        h1.value[i] = True
        h1.update_level()
        h1._set_fields(matrix)

        h1.propagate(h)

        children.append(h1)
        # hi = h.initial(h1, matrix)
        # hf = h.final(h1, matrix)
        # cont = 0
        # while hp <= hi and hp >= hf:
        #     if hp.distance(h1) == 1 and hp.distance(h) == 2:
        #         h1.propagate(hp)
        #         cont += 1
            
        #     pos += 1
        #     hp = current[pos]
        
        # if cont == h.level:
        #     children.append(h1)
    
    return children


def parse_matrix(matrix):
    deleted_columns_index = []
    M = matrix.shape[1]
    for i in range(matrix.shape[1] - 1, 0, -1):
        column = matrix[:, i].reshape(-1)
        if np.sum(column) == 0:
            matrix = np.delete(matrix, i, 1)
            deleted_columns_index.append(i)

    print(f'Start columns: {M} - End columns: {matrix.shape[1]}')
    matrix_to_print = [[0 if x == False else 1 for x in row] for row in matrix]
    
    for row in matrix_to_print:
        print(row)

    return matrix, deleted_columns_index


def check_solution(matrix, solution):
    tmp = np.array([False] * matrix.shape[0], dtype=bool)
    for i in range(len(solution)):
        if solution[i]:
            tmp = np.logical_or(tmp, matrix[:,i])

    if np.sum(tmp) == matrix.shape[0]:
        print('Correct solution!')

    else:
        print('NOT correct solution!')


def permute_matrix_columns(matrix):
    col_sums = matrix.sum(axis=0)
    sorted_indices = np.argsort(col_sums)[::-1]
    matrix = matrix[:, sorted_indices]


def MHS(matrix: np.ndarray, delta):
    """
    Minimum Hypothesis Search algorithm
    """
    # permute_matrix_columns(matrix)

    matrix, deleted_columns_index = parse_matrix(matrix)

    h0 = Node([False] * len(matrix[0]))
    h0.update_level()
    h0._set_fields(matrix)

    global current
    current = [h0]
    # delta = []

    while len(current) > 0:
        next = []

        i = 0
        n = len(current)
        print(current[0].level, n)
        while i < n:
            h = current[i]
            if check(h):
                print('Found solution')
                delta.append(h.value)
                current.pop(i)
                i -= 1
                n -= 1

            elif h.level == 0:
                next.extend(generate_children(h, matrix))
            elif h.lm() != 0:
                hs = h.global_initial(matrix)
                tmp = [c for c in current if c <= hs]

                i -= (len(current) - len(tmp))
                n = len(tmp)
                current = tmp
                hp = current[0]

                if hp != h:
                    children = generate_children(h, matrix)
                    next.extend(children)
                    next.sort(reverse=True)
                
            i += 1
        current = next

    for sol in delta:
        check_solution(matrix, sol)

    delta = np.array(delta)
    if len(delta) == 0:
        return delta
    
    for i in deleted_columns_index[::-1]:
        new_column = np.array([False] * delta.shape[0], dtype=bool)
        delta = np.insert(delta, i, new_column, axis=1)

    return delta