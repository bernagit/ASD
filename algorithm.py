import numpy as np
from collections import deque

class Node():
    """
    Hypothesis node class
    """

    def __init__(self, value: list[bool]):
        self.value = np.array(value, dtype=bool)
        self.level = np.sum(self.value)
        self.vector = None

    def update_level(self):
        self.level = np.sum(self.value)

    def _set_fields(self, matrix: np.ndarray):
        if self.level == 1:
            # get the matrix column at index value
            self.vector = matrix[:, np.where(self.value)[0]].reshape(-1)
        else:
            # return an empty vector
            self.vector = np.zeros(len(matrix), dtype=bool)

    def lm(self):
        # return index of leftmost True in vector

        return np.argmax(self.value)
    
    def propagate(self, h):
        """
        Propagate hypothesis h to hp
        """
        self.vector = np.logical_or(self.vector, h.vector)

    def global_initial(self, matrix):
        """
        Return global initial
        """
        new_value = np.copy(self.value)
        new_value[0] = True
        # Find the rigthmost True in vector
        i = np.where(self.value == True)[0][-1]

        new_value[i] = False

        n = Node(new_value)
        n._set_fields(matrix)
        return n

    def __gt__(self, h):
        """
        Check if hypothesis h is greater than self
        """
        if self.level < h.level:
            return False
        
        if self.level > h.level:
            return True        

        for i in range(len(self.value)):
            if self.value[i] < h.value[i]:
                return False
            elif self.value[i] > h.value[i]:
                return True

        return False
    
    def __ge__(self, h):
        """
        Check if hypothesis h is greater than or equal to self
        """
        return self.__gt__(h) or self.__eq__(h)
    
    def __lt__(self, h):
        """Check if self is less than hypothesis h."""
        if self.level < h.level:
            return True
        elif self.level > h.level:
            return False

        for i in range(len(self.value)):
            if self.value[i] < h.value[i]:
                return True
            elif self.value[i] > h.value[i]:
                return False

        return False
    
    def __le__(self, h):
        """Check if self is less than or equal to hypothesis h."""
        return self.__lt__(h) or self.__eq__(h)
    
    def __eq__(self, h):
        """
        Check if hypothesis h is equal to self
        """
        return self.level == h.level and np.array_equal(self.value, h.value)

    def __ne__(self, h):
        """
        Check if hypothesis h is not equal to self
        """
        return not self.__eq__(h)

    def initial(self, h, matrix):
        """
        Return initial hypothesis
        """
        new_value = np.copy(h.value)
        i = np.where(new_value == True)[0][-1]
        new_value[i] = False

        initial = Node(new_value)
        initial.update_level()
        initial._set_fields(matrix)
        return initial


    def final(self, h, matrix):
        """
        Return final hypothesis
        """
        new_value = np.copy(h.value)
        i = np.where(new_value == True)[0][1]
        new_value[i] = False

        initial = Node(new_value)
        initial.update_level()
        initial._set_fields(matrix)
        return initial
    
    def distance(self, h):
        """
        Return distance between hypothesis h and self
        """
        return np.sum(np.logical_xor(self.value, h.value))
    
    def __str__(self):
        return f'{self.value}'


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

    for d in delta:
        print(d)
    return delta