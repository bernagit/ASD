import os
import csv
import time
import tracemalloc
from algorithm import Solver, Option
from file import read_file

BANCHMARK_FOLDER = './benchmarks1'
TIME_LIMIT = 120  # Limite di tempo in secondi
MAX_COLUMNS = 16  # Numero massimo di colonne dopo parse_matrix
CSV_FILE = "permutation_results.csv"

def test_permutations():
    """Esegue i test con diverse permutazioni e salva i risultati in un CSV."""
    # Recupera i file di benchmark
    benchmark_files = [f for f in os.listdir(BANCHMARK_FOLDER) if f.endswith('.matrix')]

    # Recupera i file già presenti nel CSV
    existing_files = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                existing_files.add(row["filename"].strip())  # Rimuovi spazi o caratteri invisibili

    # Definisci i nomi delle colonne del CSV
    fieldnames = [
        "filename", "time_no_permutation", "memory_no_permutation",
        "time_random_permutation", "memory_random_permutation",
        "time_decrescent_permutation", "memory_decrescent_permutation",
        "time_crescent_permutation", "memory_crescent_permutation"
    ]

    # Crea il file CSV e scrivi l'intestazione se non esiste
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writeheader()

    # Esegui i test per ogni file
    for filename in benchmark_files:
        if filename in existing_files:
            print(f"[INFO] Il file {filename} è già presente nel CSV. Saltato.")
            continue  # Salta il file se è già presente nel CSV

        filepath = os.path.join(BANCHMARK_FOLDER, filename)
        instance_matrix = read_file(filepath)

        results = {"filename": filename}

        # Funzione per eseguire un caso specifico
        def execute_case(option):
            solver = Solver(instance_matrix.copy(), filename, option)
            solver.parse_matrix()  # Esegui parse_matrix
            if solver.matrix.shape[1] > MAX_COLUMNS:
                print(f"[SKIPPED] Il file {filename} supera il limite di colonne dopo permutazione. Troppo grande.")
                return None, None
            tracemalloc.start()
            start_time = time.time()
            solver.calculate_solutions(preprocess=False)
            elapsed_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            if elapsed_time > TIME_LIMIT:
                return "TIME LIMIT", None
            return elapsed_time, peak / 1024  # Converti in KB

        # Caso 1: Nessuna permutazione
        option_no_permutation = Option(debug=True, delete_zeros=True, delete_duplicates=True, max_time=TIME_LIMIT)
        results["time_no_permutation"], results["memory_no_permutation"] = execute_case(option_no_permutation)

        # Caso 2: Permutazione casuale
        option_random_permutation = Option(debug=True, delete_zeros=True, delete_duplicates=True, max_time=TIME_LIMIT, permute_columns=True)
        results["time_random_permutation"], results["memory_random_permutation"] = execute_case(option_random_permutation)

        # Caso 3: Permutazione decrescente
        option_decrescent_permutation = Option(debug=True, delete_zeros=True, delete_duplicates=True, max_time=TIME_LIMIT, permute_columns_desc=True)
        results["time_decrescent_permutation"], results["memory_decrescent_permutation"] = execute_case(option_decrescent_permutation)

        # Caso 4: Permutazione crescente
        option_crescent_permutation = Option(debug=True, delete_zeros=True, delete_duplicates=True, max_time=TIME_LIMIT, permute_columns_asc=True)
        results["time_crescent_permutation"], results["memory_crescent_permutation"] = execute_case(option_crescent_permutation)

        # Salva i risultati nel CSV
        with open(CSV_FILE, "a", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writerow(results)

        print(f"[INFO] Risultati salvati per il file {filename}")

    print(f"\n[INFO] Test completati. Risultati salvati in '{CSV_FILE}'.")


if __name__ == "__main__":
    test_permutations()