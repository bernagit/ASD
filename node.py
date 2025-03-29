import numpy as np

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
        # return index of leftmost True in value
        for i in range(len(self.value)):
            if self.value[i] == True:
                return i

        return -1
        # return np.argmax(self.value)
    
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

    # def __gt__(self, h):
    #     """
    #     Check if hypothesis h is greater than self
    #     """
    #     if self.level < h.level:
    #         return False
        
    #     if self.level > h.level:
    #         return True        

    #     for i in range(len(self.value)):
    #         if self.value[i] < h.value[i]:
    #             return False
    #         elif self.value[i] > h.value[i]:
    #             return True

    #     return False
    
    # def __ge__(self, h):
    #     """
    #     Check if hypothesis h is greater than or equal to self
    #     """
    #     return self.__gt__(h) or self.__eq__(h)
    
    # def __lt__(self, h):
    #     """Check if self is less than hypothesis h."""
    #     if self.level < h.level:
    #         return True
    #     elif self.level > h.level:
    #         return False

    #     for i in range(len(self.value)):
    #         if self.value[i] < h.value[i]:
    #             return True
    #         elif self.value[i] > h.value[i]:
    #             return False

    #     return False
    
    # def __le__(self, h):
    #     """Check if self is less than or equal to hypothesis h."""
    #     return self.__lt__(h) or self.__eq__(h)
    
    # def __eq__(self, h):
    #     """
    #     Check if hypothesis h is equal to self
    #     """
    #     return self.level == h.level and np.array_equal(self.value, h.value)

    # def __ne__(self, h):
    #     """
    #     Check if hypothesis h is not equal to self
    #     """
    #     return not self.__eq__(h)

    def _binary_representation(self):
        """Convert the boolean array to a binary string representation."""
        return ''.join('1' if bit else '0' for bit in self.value)

    def __lt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self._binary_representation() < other._binary_representation()

    def __le__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self._binary_representation() <= other._binary_representation()

    def __gt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self._binary_representation() > other._binary_representation()

    def __ge__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self._binary_representation() >= other._binary_representation()

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return np.array_equal(self.value, other.value)

    def __ne__(self, other):
        return not self.__eq__(other)

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
