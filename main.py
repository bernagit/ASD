import os

import numpy as np

from algorithm import MHS

BANCHMARK_FOLDERS = ['./benchmarks1', './benchmarks2']

def get_benchmark_files():
    benchmarks = []
    for folder in BANCHMARK_FOLDERS:
        # filter files based on matrix file extension
        files = [f for f in os.listdir(folder) if f.endswith('.matrix')]
        benchmarks.append(files)
    
    return benchmarks

def main():
    # benchmarks = get_benchmark_files()
    matrix = np.array([[1, 0, 0], [1, 0, 1], [0, 1, 0], [1, 1, 0], [1, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=bool)
    MHS(matrix)

main()