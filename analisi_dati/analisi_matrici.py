import os
from algorithm import Solver
from file import read_file

BANCHMARK_FOLDER = './benchmarks1'  # Percorso della cartella benchmarks1

def count_files_with_large_matrices():
    """Conta i file con una matrice che ha più di 18 colonne finali."""
    try:
        files = [f for f in os.listdir(BANCHMARK_FOLDER) if f.endswith('.matrix')]
        count = 0

        for filename in files:
            file_path = os.path.join(BANCHMARK_FOLDER, filename)
            instance_matrix = read_file(BANCHMARK_FOLDER, filename)
            solver = Solver(instance_matrix, filename, debug=False)
            num_columns = solver.remove_empty_columns()

            if num_columns > 18:
                print(f"Il file '{filename}' ha {num_columns} colonne effettive (più di 18).")
                count += 1

        print(f"\nNumero totale di file con più di 18 colonne effettive: {count}")
    except FileNotFoundError:
        print(f"Errore: La cartella {BANCHMARK_FOLDER} non esiste.")
    except Exception as e:
        print(f"Errore durante il conteggio dei file: {e}")

if __name__ == "__main__":
    count_files_with_large_matrices()