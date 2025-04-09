from algorithm import Solver
from file import read_file
import numpy as np

def main():
    instance_filename = '74L85.002.matrix'
    instance_matrix = read_file('benchmarks1/' + instance_filename)

    solver = Solver(instance_matrix, instance_filename)
    solver.calculate_solutions()
    first_solutions = solver.solutions
    first_solutions_binary = [''.join(['1' if x else '0' for x in first_solution]) for first_solution  in first_solutions]
    first_solutions_binary.sort()
    first_solutions_time = solver.execution_time

    solver = Solver(instance_matrix, instance_filename)
    solver.permute_rows()
    solver.calculate_solutions()
    second_solutions = solver.solutions
    second_solutions_binary = [''.join(['1' if x else '0' for x in second_solution]) for second_solution  in second_solutions]
    second_solutions_binary.sort()
    second_solutions_time = solver.execution_time

    print('Checking rows permutations:')
    print(f'Number of solutions without permutation: {len(first_solutions)}')
    print(f'Number of solutions WITH permutation: {len(second_solutions)}')
    if len(first_solutions) == len(second_solutions):
        print('Count OK')
    else:
        print('Something is wrong...')
        return

    number_of_equal_solutions = 0
    for i in range(len(first_solutions)):
        if first_solutions_binary[i] == second_solutions_binary[i]:
            number_of_equal_solutions += 1

    if number_of_equal_solutions == len(first_solutions):
        print('All the solutions are the same!')
        print('Check passed')
    else:
        print('The solutions found aren\'t the same...')
        return

    print()
    print()

    solver = Solver(instance_matrix, instance_filename)
    solver.permute_columns()
    solver.calculate_solutions()
    third_solutions = solver.get_solutions_without_permutation()
    third_solutions_binary = [''.join(['1' if x else '0' for x in third_solution]) for third_solution  in third_solutions]
    third_solutions_binary.sort()
    third_solutions_time = solver.execution_time

    print('Checking columns permutations:')
    print(f'Number of solutions without permutation: {len(first_solutions)}')
    print(f'Number of solutions WITH permutation: {len(third_solutions)}')
    if len(first_solutions) == len(third_solutions):
        print('Count OK')
    else:
        print('Something is wrong...')
        return


    number_of_equal_solutions = 0
    for i in range(len(first_solutions)):
        if first_solutions_binary[i] == third_solutions_binary[i]:
            number_of_equal_solutions += 1

    if number_of_equal_solutions == len(first_solutions):
        print('All the solutions are the same!')
        print('Check passed')
    else:
        print('The solutions found aren\'t the same...')
        return
    
    print()
    print()

    solver = Solver(instance_matrix, instance_filename)
    solver.permute_columns()
    solver.permute_rows()
    solver.calculate_solutions()
    fourth_solutions = solver.get_solutions_without_permutation()
    fourth_solutions_binary = [''.join(['1' if x else '0' for x in fourth_solution]) for fourth_solution  in fourth_solutions]
    fourth_solutions_binary.sort()
    fourth_solutions_time = solver.execution_time

    print('Checking rows AND columns permutations:')
    print(f'Number of solutions without permutation: {len(first_solutions)}')
    print(f'Number of solutions WITH permutation: {len(fourth_solutions)}')
    if len(first_solutions) == len(fourth_solutions):
        print('Count OK')
    else:
        print('Something is wrong...')
        return


    number_of_equal_solutions = 0
    for i in range(len(first_solutions)):
        if first_solutions_binary[i] == fourth_solutions_binary[i]:
            number_of_equal_solutions += 1

    if number_of_equal_solutions == len(first_solutions):
        print('All the solutions are the same!')
        print('Check passed')
    else:
        print('The solutions found aren\'t the same...')
        return

    print()
    print()

    print('Execution times:')
    print(f'No permutations: {first_solutions_time} s')
    print(f'Row permutations: {second_solutions_time} s')
    print(f'Column permutations: {third_solutions_time} s')
    print(f'Row and column permutations: {fourth_solutions_time} s')

main()