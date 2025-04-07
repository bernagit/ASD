import os
import csv
import time
import tracemalloc  # Per monitorare l'uso della memoria
from algorithm import Solver, Option
from file import read_file

BANCHMARK_FOLDER = './benchmarks1'
TIME_LIMIT = 120  # Limite di tempo in secondi
MAX_COLUMNS = 18  # Numero massimo di colonne per eseguire il solver
CSV_FILE = "performance_comparison.csv"

def analyze_benchmarks():
    """Esegue i benchmark con diverse opzioni e salva i risultati in un CSV."""
    # Recupera i file di benchmark
    benchmark_files = [f for f in os.listdir(BANCHMARK_FOLDER) if f.endswith('.matrix')]

    # Recupera i file già presenti nel CSV
    existing_files = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                existing_files.add(row["filename"])  # Aggiungi i nomi dei file già analizzati

    # Definisci i nomi delle colonne del CSV
    fieldnames = [
        "filename", "columns_after_dz", "columns_after_dz_dd",
        "time_dz", "memory_dz", "termination_status_dz",
        "time_dz_dd", "memory_dz_dd", "termination_status_dz_dd"
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

        # Crea l'oggetto Solver con l'opzione dz
        opt_dz = Option(debug=True, delete_zeros=True, delete_duplicates=False, max_time=TIME_LIMIT)
        solver_dz = Solver(instance_matrix, filename, opt_dz)
        solver_dz.parse_matrix()
        columns_after_dz = solver_dz.matrix.shape[1]

        # Inizializza i risultati per il caso dz
        elapsed_time_dz = None
        memory_dz = None
        termination_status_dz = None

        # Esegui il solver con dz solo se il numero di colonne è entro il limite
        if columns_after_dz <= MAX_COLUMNS:
            tracemalloc.start()  # Inizia il monitoraggio della memoria
            start_time = time.time()
            solver_dz.calculate_solutions()
            elapsed_time_dz = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()  # Ottieni la memoria corrente e di picco
            memory_dz = peak / 1024  # Converti in KB
            tracemalloc.stop()  # Ferma il monitoraggio della memoria
            termination_status_dz = "TERMINATED" if elapsed_time_dz <= TIME_LIMIT and solver_dz.stopped==False else "TIME LIMIT"
        else:
            termination_status_dz = "TOO LARGE"
            print(f"[INFO] Il file {filename} ha {columns_after_dz} colonne. Caso dz non eseguito.")

        # Crea l'oggetto Solver con le opzioni dz e dd
        instance_matrixdd = read_file(filepath)

        opt_dz_dd = Option(debug=True, delete_zeros=True, delete_duplicates=True, max_time=TIME_LIMIT)
        solver_dz_dd = Solver(instance_matrixdd, filename, opt_dz_dd)
        solver_dz_dd.parse_matrix()
        columns_after_dz_dd = solver_dz_dd.matrix.shape[1]

        # Inizializza i risultati per il caso dz e dd
        elapsed_time_dz_dd = None
        memory_dz_dd = None
        termination_status_dz_dd = None

        # Esegui il solver con dz e dd solo se il numero di colonne è entro il limite
        if columns_after_dz_dd <= MAX_COLUMNS:
            print(f"numero colonne dopo dz e dd: {columns_after_dz_dd}")
            tracemalloc.start()  # Inizia il monitoraggio della memoria
            start_time = time.time()
            solver_dz_dd.calculate_solutions()
            elapsed_time_dz_dd = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()  # Ottieni la memoria corrente e di picco
            memory_dz_dd = peak / 1024  # Converti in KB
            tracemalloc.stop()  # Ferma il monitoraggio della memoria
            termination_status_dz_dd = "TERMINATED" if elapsed_time_dz_dd <= TIME_LIMIT and solver_dz_dd.stopped==False else "TIME LIMIT"
        else:
            termination_status_dz_dd = "TOO LARGE"
            print(f"[INFO] Il file {filename} ha {columns_after_dz_dd} colonne. Caso dz e dd non eseguito.")
    
        # Salva i risultati nel CSV
        with open(CSV_FILE, "a", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writerow({
                "filename": filename,
                "columns_after_dz": columns_after_dz,
                "columns_after_dz_dd": columns_after_dz_dd,
                "time_dz": elapsed_time_dz if termination_status_dz == "TERMINATED" else None,
                "memory_dz": memory_dz if termination_status_dz == "TERMINATED" else None,
                "termination_status_dz": termination_status_dz,
                "time_dz_dd": elapsed_time_dz_dd if termination_status_dz_dd == "TERMINATED" else None,
                "memory_dz_dd": memory_dz_dd if termination_status_dz_dd == "TERMINATED" else None,
                "termination_status_dz_dd": termination_status_dz_dd
            })

        print(f"[INFO] Risultati salvati per il file {filename}")

    print(f"\n[INFO] Analisi completata. Risultati salvati in '{CSV_FILE}'.")


if __name__ == "__main__":
    analyze_benchmarks()