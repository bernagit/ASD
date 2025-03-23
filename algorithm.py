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

        hi = h.initial(h1, matrix)
        hf = h.final(h1, matrix)
        cont = 0
        while hp <= hi and hp >= hf:
            if hp.distance(h1) == 1 and hp.distance(h) == 2:
                h1.propagate(hp)
                cont += 1
            
            pos += 1
            hp = current[pos]
        
        if cont == h.level:
            children.append(h1)
    
    return children




def MHS(matrix: np.ndarray):
    """
    Minimum Hypothesis Search algorithm
    """
    h0 = Node([False] * len(matrix[0]))
    h0.update_level()
    h0._set_fields(matrix)

    global current
    # current = deque([h0])
    current = [h0]
    delta = []

    while len(current) > 0:
        next = []

        i = 0
        n = len(current)
        while i < n:
            h = current[i]
            if check(h):
                delta.append(h)
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
                    next.extend(generate_children(h, matrix))
                    next.sort(reverse=True)
                
            i += 1
        current = next

    return delta