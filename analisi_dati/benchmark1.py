from os import listdir
from file import read_file
import numpy as np
from algorithm import Solver
import time

import matplotlib.pyplot as plt

def plot_dp_metrics(dp_time, dp_memory):
    # Sort data by number of columns
    columns = sorted(dp_time.keys())
    times = [dp_time[col] for col in columns]
    memories = [dp_memory[col] for col in columns]

    # Plot execution time
    plt.figure(figsize=(10, 5))
    plt.plot(columns, times, marker='o', linestyle='-', color='blue')
    plt.title('Execution Time vs Number of Columns')
    plt.xlabel('Number of Columns')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot memory usage
    plt.figure(figsize=(10, 5))
    plt.plot(columns, memories, marker='s', linestyle='-', color='green')
    plt.title('Memory Usage vs Number of Columns')
    plt.xlabel('Number of Columns')
    plt.ylabel('Memory Usage (MB or relevant unit)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    files = listdir('benchmarks1')
    
    dp_time = {}
    dp_memory = {}
    cont = 0
    # percentages = []
    for file in files[::-1]:
        instance_matrix = read_file('benchmarks1', file)
        solver = Solver(instance_matrix, file, debug=False)
        solver.parse_matrix()

        if solver.matrix.shape[1] < 15:
            solver.calculate_solutions()
            elapsed = time.time() - solver.start_time
            dp_time[solver.matrix.shape[1]] = elapsed
            dp_memory[solver.matrix.shape[1]] = solver.get_used_memory()[1]

            cont += 1
            print(cont)
            if cont > 100:
                break


        # percentage = 1 - (len(solver.deleted_columns_index) / instance_matrix.shape[1])
        # print(f'{file}\t{instance_matrix.shape[1]}\t{len(solver.deleted_columns_index)}\t{percentage}')
        # percentages.append(percentage)


    print(dp_time)
    print(dp_memory)
    plot_dp_metrics(dp_time, dp_memory)
    # mean = np.mean(percentages)
    # print(f'The mean column reduction is {mean * 100}%')
    # for i in range(0, 10):
    #     instance_filename = f'74181.00{i}.matrix'
    #     instance_matrix = read_file('benchmarks1', instance_filename)
    #     solver = Solver(instance_matrix, instance_filename, debug=False)
    #     solver.parse_matrix()

    #     print(len(solver.deleted_columns_index))


if __name__ == '__main__':
    main()