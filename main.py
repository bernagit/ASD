import os
import time
import numpy as np
from algorithm import Solver

import signal
import sys

from file import read_file, COMMENT

BANCHMARK_FOLDERS = ['benchmarks1', 'benchmarks2']

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
    pwd = os.getcwd()
    for folder in BANCHMARK_FOLDERS:
        folder = os.path.join(pwd, folder)
        files = [(folder, f) for f in os.listdir(folder) if f.endswith('.matrix')]
        benchmarks.extend(files)
    
    return benchmarks

def write_solutions(input_filename, solutions, resources_info, interruped = False):
    global solver

    input_filename = os.path.basename(input_filename)
    input_filename = '.'.join(input_filename.split('.')[:-1])

    min_card = np.sum(solutions[0])
    max_card = np.sum(solutions[-1])
    found_solutions = len(solutions)
    removed_columns_string = f'[{', '.join(str(i + 1) for i in solver.deleted_columns_index[::-1])}]'

    output_file = open(f'results/{input_filename}.mhs', 'w+')

    output_file.write(f'{COMMENT} Input matrix {solver.matrix.shape[0]} X {solver.matrix.shape[1] + len(solver.deleted_columns_index)}\n')
    output_file.write(f'{COMMENT} Number of MHS found: {found_solutions}\n')
    output_file.write(f'{COMMENT} Minimum cardinality: {min_card}\n')
    output_file.write(f'{COMMENT} Maximum cardinality: {max_card}\n')
    output_file.write(f'{COMMENT} Elapsed time: {resources_info[0]}s\n')
    output_file.write(f'{COMMENT} Memory used: {(resources_info[1][1]) / (1024)} KB\n')
    if len(solver.deleted_columns_index) > 0:
        output_file.write(f'{COMMENT} Computation done removing the columns: {removed_columns_string}\n')
        output_file.write(f'{COMMENT} -> The dimensions of the matrix really used are {solver.matrix.shape[0]} X {solver.matrix.shape[1]}\n')

    output_file.write(f'{COMMENT} Computation stopped at level {solver.current_level}\n')
    if interruped:
        output_file.write(f'{COMMENT} The computation has been stopped by the user before terminating\n')

    output_file.write(f'{COMMENT}\n')
    output_file.write(f'{COMMENT} Hypotesis generated for each level:\n')
    for level in solver.hypoteses_per_level:
        output_file.write(f'{COMMENT} Level {level}: {solver.hypoteses_per_level[level]} hypotes{'es' if solver.hypoteses_per_level[level] > 1 else 'is'}\n')
    output_file.write(f'{COMMENT}\n')

    for x in solutions:
        solution_line = f'{' '.join(['1' if y == True else '0' for y in x])} -\n'
        output_file.write(solution_line)

def main():
    global solver
    cwd = os.getcwd()

    file_names = sys.argv[1:]

    executions = []

    for file_name in file_names:
        executions.append(os.path.join(cwd, file_name))
    else:
        files = get_benchmark_files()
        for folder, file_name in files:
            executions.append(os.path.join(cwd, folder, file_name))
        
    for file_name in executions:
        instance_matrix = read_file(file_name)
        solver = Solver(instance_matrix, file_name)
        # solver.permute_columns()

        solver.calculate_solutions()
        elapsed = time.time() - solver.start_time

        write_solutions(file_name, solver.solutions, [elapsed, solver.get_used_memory()])


if __name__ == '__main__':
    main()