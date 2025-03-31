import numpy as np

def read_file(folder, filename):
    file = f"{folder}/{filename}"
    line = ';;;'
    with open(file, 'r') as f:
        lines = f.readlines()
        
        matrix = []
        for line in lines:
            if line.startswith(';;;'):
                continue

            line = line.replace('-', '')
            line = line.strip()
            matrix.append([bool(int(x)) for x in line.split()])
        
        matrix = np.array(matrix, dtype=bool)
        return matrix