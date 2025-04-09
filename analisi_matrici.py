import os
from algorithm import Solver
from file import read_file
from main import get_benchmark_files


def count_files_with_large_matrices():
    """Conta i file con una matrice che ha più di 18 colonne finali."""
    try:
        files = get_benchmark_files()
        count = 0
        for dir, filename in files:
            instance_matrix = read_file(os.path.join(dir, filename))
            solver = Solver(instance_matrix, filename)
            num_columns = solver.remove_empty_columns()

            if num_columns > 18:
                print(f"Il file '{filename}' ha {num_columns} colonne effettive (più di 18).")
                count += 1

        print(f"\nNumero totale di file con più di 18 colonne effettive: {count}")
    except Exception as e:
        print(f"Errore durante il conteggio dei file: {e}")

if __name__ == "__main__":
    count_files_with_large_matrices()