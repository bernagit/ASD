import os
import time
import numpy as np
from algorithm import Solver

import signal
import sys

from file import read_file

BANCHMARK_FOLDERS = ['./benchmarks1', './benchmarks2']

solver: Solver | None = None

def signal_handler(sig, frame):
    """Handle Ctrl+C (SIGINT) signal."""
    print("\nCtrl+C detected! Cleaning up...")
    
    solver.stopped = True
    elapsed = time.time() - solver.start_time
    write_solutions(solver.instance_filename, solver.solutions, [elapsed, solver.get_used_memory()], interruped=True)

    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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

def write_solutions(input_filename, solutions, resources_info, interruped = False):
    global solver

    min_card = np.sum(solutions[0])
    max_card = np.sum(solutions[-1])
    found_solutions = len(solutions)
    removed_columns_string = f'[{', '.join(str(i + 1) for i in solver.deleted_columns_index[::-1])}]'

    filename_without_extension = ''.join(input_filename.split('.')[:-1])
    output_file = open(f'results/{filename_without_extension}.mhs', 'w+')

    output_file.write(f';;; Input matrix {solver.matrix.shape[0]} X {solver.matrix.shape[1] + len(solver.deleted_columns_index)}\n')
    output_file.write(f';;; Number of MHS found: {found_solutions}\n')
    output_file.write(f';;; Minimum cardinality: {min_card}\n')
    output_file.write(f';;; Maximum cardinality: {max_card}\n')
    output_file.write(f';;; Elapsed time: {resources_info[0]}s\n')
    output_file.write(f';;; Memory used: {(resources_info[1][1]) / (1024)} KB\n')
    if len(solver.deleted_columns_index) > 0:
        output_file.write(f';;; Computation done removing the columns: {removed_columns_string}\n')
        output_file.write(f';;; -> The dimensions of the matrix really used are {solver.matrix.shape[0]} X {solver.matrix.shape[1]}\n')

    output_file.write(f';;; Computation stopped at level {solver.current_level}\n')
    if interruped:
        output_file.write(f';;; The computation has been stopped by the user before terminating\n')

    output_file.write(';;;\n')
    output_file.write(';;; Hypotesis generated for each level:\n')
    for level in solver.hypoteses_per_level:
        output_file.write(f';;; Level {level}: {solver.hypoteses_per_level[level]} hypotes{'es' if solver.hypoteses_per_level[level] > 1 else 'is'}\n')
    output_file.write(';;;\n')

    for x in solutions:
        solution_line = f'{' '.join(['1' if y == True else '0' for y in x])} --\n'
        output_file.write(solution_line)

def main():
    global solver

    instance_filename = '74L85.004.matrix'
    instance_matrix = np.array([[1, 0, 0], [1, 0, 1], [0, 1, 0], [1, 1, 0], [1, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=bool)
    # instance_matrix = np.array([[0, 0, 0, 1, 1], [1, 1, 0, 0, 1], [0, 1, 1, 1, 1]], dtype=bool)
    instance_matrix = read_file('benchmarks1', instance_filename)
    solver = Solver(instance_matrix, instance_filename)
    # solver.permute_columns()
    
    solver.calculate_solutions()
    elapsed = time.time() - solver.start_time
    
    write_solutions(instance_filename, solver.solutions, [elapsed, solver.get_used_memory()])


if __name__ == '__main__':
    main()