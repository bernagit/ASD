import os
import time
import numpy as np
from algorithm import MHS

BANCHMARK_FOLDERS = ['./benchmarks1', './benchmarks2']


class Result():
    
    result_path = './results'
    
    def __init__(self, filename, time, mhs):
        self.filename = filename
        self.time = time
        self.mhs = mhs
    
    def save(self):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

        with open(f"{self.result_path}/{self.filename}.result", 'w') as f:
            f.write(f"Time: {time}")
            for r in self.mhs:
                f.write(r)


def get_benchmark_files():
    benchmarks = []
    for folder in BANCHMARK_FOLDERS:
        files = [(folder, f) for f in os.listdir(folder) if f.endswith('.matrix')]
        benchmarks.extend(files)
    
    return benchmarks

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



def main():
    benchmarks = get_benchmark_files()

    for folder, filename in benchmarks:
        break
        start = time.time()
        matrix = read_file(folder, filename)

        # matrix = np.array([[1, 0, 0], [1, 0, 1], [0, 1, 0], [1, 1, 0], [1, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=bool)

        mhs = MHS(matrix)

        end = time.time()


        result = Result(folder, filename, end - start, mhs)
        result.save()

    # matrix = np.array([[1, 0, 0], [1, 0, 1], [0, 1, 0], [1, 1, 0], [1, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=bool)
    # matrix = np.array([[0, 0, 1, 1, 0], [1, 1, 0, 1, 0], [0, 1, 1, 1, 1]], dtype=bool)
    matrix = read_file('benchmarks2', 'c7552.325.matrix')

    # matrix = matrix.transpose()
    mhs = MHS(matrix)
    for x in mhs:
        print(x)


if __name__ == '__main__':
    main()