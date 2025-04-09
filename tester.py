import os
import time
import signal
import sys
from algorithm import Solver
from file import read_file
import csv

BANCHMARK_FOLDER = './benchmarks1'  # Esegui solo i file in benchmarks1
TIME_LIMIT = 30 # in secondi

results = {
    "normal": [],
    "row_permutations": [],
    "column_permutations": [],
    "row_and_column_permutations": []
}

def signal_handler(sig, frame):
    """Gestisce il segnale Ctrl+C (SIGINT)."""
    print("\nCtrl+C rilevato! Uscita...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_benchmark_files():
    """Recupera tutti i file di benchmark dalla cartella specificata."""
    benchmarks = []
    for f in os.listdir(BANCHMARK_FOLDER):
        if f.endswith('.matrix'):
            benchmarks.append(f)
    
    # Stampa i nomi dei file trovati
    #print("File trovati:")
    #for filename in benchmarks:
    #    print(f"- {filename}")
    
    return benchmarks

def track_memory_and_time(solver):
    """Esegue il calcolo delle soluzioni con un limite di tempo e tiene traccia del tempo e della memoria."""
    def timeout_handler(signum, frame):
        raise TimeoutError("Tempo limite superato durante il calcolo delle soluzioni.")

    # Imposta il gestore del segnale per il timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIME_LIMIT)  # Imposta il limite di tempo

    try:
        solver.calculate_solutions()
        signal.alarm(0)  # Disabilita l'allarme se il calcolo è completato
        elapsed_time = solver.execution_time
        _, peak_memory = solver.get_used_memory()  # Ottieni il picco di memoria usata
        return elapsed_time, peak_memory / 1024  # Tempo in secondi, memoria in KB
    except TimeoutError as e:
        print(f"[ERROR] {e}")
        signal.alarm(0)  # Disabilita l'allarme
        return None, None  # Restituisce None per tempo e memoria in caso di timeout
    except KeyboardInterrupt:
        print("\n[ERROR] Esecuzione interrotta manualmente.")
        signal.alarm(0)  # Disabilita l'allarme
        return None, None  # Restituisce None per tempo e memoria in caso di interruzione manuale

def run_tests(instance_matrix, instance_filename):
    """Esegue i test per un singolo file di benchmark."""
    print(f"\nInizio test per il file: {instance_filename}")

    # Crea un'istanza del solver per verificare il numero di colonne effettive
    solver = Solver(instance_matrix, instance_filename, debug=True,max_time=TIME_LIMIT)
    num_columns = solver.remove_empty_columns()

    # Verifica il limite sul numero di colonne
    if num_columns > 18:
        print(f"[SKIPPED] La matrice ha {num_columns} colonne effettive, superando il limite di 18. Test saltato.")
        return False  # Indica che l'esecuzione non è stata completata

    # Caso normale
    print("  [INFO] Esecuzione caso normale...")
    normal_time, normal_memory = track_memory_and_time(solver)
    if normal_time is not None and normal_memory is not None:
        results["normal"].append((normal_time, normal_memory))
        print(f"  [DONE] Caso normale completato: Tempo = {normal_time:.2f}s, Memoria = {normal_memory:.2f} KB")
    else:
        print("  [SKIPPED] Caso normale saltato a causa di interruzione o timeout.")
        return False  # Interrompe l'esecuzione per questo file

    # Permutazioni sulle righe
    print("  [INFO] Esecuzione permutazioni sulle righe...")
    solver = Solver(instance_matrix, instance_filename, debug=True)
    solver.permute_rows()
    row_time, row_memory = track_memory_and_time(solver)
    if row_time is not None and row_memory is not None:
        results["row_permutations"].append((row_time, row_memory))
        print(f"  [DONE] Permutazioni sulle righe completate: Tempo = {row_time:.2f}s, Memoria = {row_memory:.2f} KB")
    else:
        print("  [SKIPPED] Permutazioni sulle righe saltate a causa di interruzione o timeout.")
        return False  # Interrompe l'esecuzione per questo file

    # Permutazioni sulle colonne
    print("  [INFO] Esecuzione permutazioni sulle colonne...")
    solver = Solver(instance_matrix, instance_filename, debug=True)
    solver.permute_columns()
    column_time, column_memory = track_memory_and_time(solver)
    if column_time is not None and column_memory is not None:
        results["column_permutations"].append((column_time, column_memory))
        print(f"  [DONE] Permutazioni sulle colonne completate: Tempo = {column_time:.2f}s, Memoria = {column_memory:.2f} KB")
    else:
        print("  [SKIPPED] Permutazioni sulle colonne saltate a causa di interruzione o timeout.")
        return False  # Interrompe l'esecuzione per questo file

    # Permutazioni su righe e colonne
    print("  [INFO] Esecuzione permutazioni su righe e colonne...")
    solver = Solver(instance_matrix, instance_filename, debug=True, )
    solver.permute_columns()
    solver.permute_rows()
    both_time, both_memory = track_memory_and_time(solver)
    if both_time is not None and both_memory is not None:
        results["row_and_column_permutations"].append((both_time, both_memory))
        print(f"  [DONE] Permutazioni su righe e colonne completate: Tempo = {both_time:.2f}s, Memoria = {both_memory:.2f} KB")
    else:
        print("  [SKIPPED] Permutazioni su righe e colonne saltate a causa di interruzione o timeout.")
        return False  # Interrompe l'esecuzione per questo file

    return True  # Indica che tutti i test per questo file sono stati completati



def calculate_averages(results):
    """Calcola i tempi e le memorie medie per ogni caso."""
    averages = {}
    for key, values in results.items():
        total_time = sum(v[0] for v in values)
        total_memory = sum(v[1] for v in values)
        count = len(values)
        averages[key] = {
            "avg_time": total_time / count if count > 0 else 0,
            "avg_memory": total_memory / count if count > 0 else 0
        }
    return averages

def save_results_to_file(averages, output_file="results300.txt"):
    """Salva i risultati medi in un file di testo."""
    with open(output_file, "w") as f:
        f.write("Riepilogo dei risultati medi:\n")
        for case, stats in averages.items():
            f.write(f"{case.capitalize()}: Tempo medio = {stats['avg_time']:.2f}s, Memoria media = {stats['avg_memory']:.2f} KB\n")
    print(f"Risultati salvati in {output_file}")
def save_partial_results(results, output_file="results_partial300.txt"):
    """Salva i risultati medi parziali in un file di testo."""
    averages = calculate_averages(results)
    with open(output_file, "w") as f:
        f.write("Riepilogo dei risultati medi parziali:\n")
        for case, stats in averages.items():
            f.write(f"{case.capitalize()}: Tempo medio = {stats['avg_time']:.2f}s, Memoria media = {stats['avg_memory']:.2f} KB\n")
    print(f"Risultati parziali salvati in {output_file}")

def test_casi_random():
    benchmark_files = get_benchmark_files()

    for filename in benchmark_files:
        instance_path = os.path.join(BANCHMARK_FOLDER, filename)
        print(f"Esecuzione del test per {instance_path}...")
        instance_matrix = read_file(BANCHMARK_FOLDER, filename)
        completed = run_tests(instance_matrix, filename)
        if not completed:
            print(f"[SKIPPED] Test non completato per {filename}.")
        else:
            print(f"[DONE] Test completato per {filename}.")
            save_partial_results(results)

    # Calcola le medie
    averages = calculate_averages(results)

    # Salva i risultati in un file
    save_results_to_file(averages)

import csv
import os

def test_permutazioni_colonne():
    """Esegue i test per ogni file in benchmarks1 considerando diversi casi di permutazione."""
    benchmark_files = get_benchmark_files()

    # Percorso del file CSV
    csv_file_path = "detailed_results.csv"

    # Leggi i file già presenti nel CSV
    existing_files = set()
    if os.path.exists(csv_file_path):
        with open(csv_file_path, "r", newline="") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                existing_files.add(row["filename"])

    # Crea il file CSV e scrive l'intestazione se non esiste
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, "w", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=[
                "filename", "rows", "columns",
                "normal_first", "normal_second",
                "decrescent_first", "decrescent_second",
                "random_first", "random_second",
                "crescent_first", "crescent_second"
            ])
            csvwriter.writeheader()

    # Riprendi l'elaborazione solo per i file non presenti nel CSV
    for filename in benchmark_files:
        if filename in existing_files:
            print(f"[INFO] Il file {filename} è già presente nel CSV. Saltato.")
            continue

        print(f"\nEsecuzione del test per il file: {filename}")

        # Leggi la matrice e crea l'oggetto Solver
        instance_matrix = read_file(BANCHMARK_FOLDER, filename)
        solver = Solver(instance_matrix, filename, debug=True, max_time=TIME_LIMIT)
        solver.parse_matrix()  # Elabora la matrice

        # Ottieni dimensioni della matrice dopo parse_matrix()
        num_rows, num_columns = solver.matrix.shape

        # Controlla se il file deve essere saltato
        if num_columns > 32 and num_rows > 7:
            print(f"[SKIPPED] Il file {filename} ha {num_columns} colonne e {num_rows} righe. Non elaborato.")
            with open(csv_file_path, "a", newline="") as csvfile:
                csvwriter = csv.DictWriter(csvfile, fieldnames=[
                    "filename", "rows", "columns",
                    "normal_first", "normal_second",
                    "decrescent_first", "decrescent_second",
                    "random_first", "random_second",
                    "crescent_first", "crescent_second"
                ])
                csvwriter.writerow({
                    "filename": filename,
                    "rows": num_rows,
                    "columns": num_columns,
                    "normal_first": None,
                    "normal_second": None,
                    "decrescent_first": None,
                    "decrescent_second": None,
                    "random_first": None,
                    "random_second": None,
                    "crescent_first": None,
                    "crescent_second": None
                })
            continue

        # Caso normale
        print("  [INFO] Esecuzione caso normale...")
        solver.calculate_solutions(firstSolution=True)
        normal_first = solver.solution_times[0]
        normal_second = solver.solution_times[1]
        if normal_first is not None:
            print(f"  [DONE] Caso normale completato: Tempo prima soluzione = {normal_first:.2f}s")
        if normal_second is None:
            print("  [INFO] Nessuna seconda soluzione trovata per il caso normale.")

        # Permutazioni colonne decrescenti
        print("  [INFO] Esecuzione permutazioni colonne decrescenti...")
        solver.permute_columns(randomize=False, decrescent=True)
        solver.calculate_solutions(firstSolution=True)
        decrescent_first = solver.solution_times[0]
        decrescent_second = solver.solution_times[1]
        if decrescent_first is not None:
            print(f"  [DONE] Permutazioni colonne decrescenti completate: Tempo prima soluzione = {decrescent_first:.2f}s")
        if decrescent_second is None:
            print("  [INFO] Nessuna seconda soluzione trovata per le permutazioni colonne decrescenti.")

        # Permutazioni colonne randomiche
        print("  [INFO] Esecuzione permutazioni colonne randomiche...")
        solver.permute_columns(randomize=True)
        solver.calculate_solutions(firstSolution=True)
        random_first = solver.solution_times[0]
        random_second = solver.solution_times[1]
        if random_first is not None:
            print(f"  [DONE] Permutazioni colonne randomiche completate: Tempo prima soluzione = {random_first:.2f}s")
        if random_second is None:
            print("  [INFO] Nessuna seconda soluzione trovata per le permutazioni colonne randomiche.")

        # Permutazioni colonne crescenti
        print("  [INFO] Esecuzione permutazioni colonne crescenti...")
        solver.permute_columns(randomize=False, decrescent=False)
        solver.calculate_solutions(firstSolution=True)
        crescent_first = solver.solution_times[0]
        crescent_second = solver.solution_times[1]
        if crescent_first is not None:
            print(f"  [DONE] Permutazioni colonne crescenti completate: Tempo prima soluzione = {crescent_first:.2f}s")
        if crescent_second is None:
            print("  [INFO] Nessuna seconda soluzione trovata per le permutazioni colonne crescenti.")

        # Salva i risultati dettagliati per il file corrente
        with open(csv_file_path, "a", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=[
                "filename", "rows", "columns",
                "normal_first", "normal_second",
                "decrescent_first", "decrescent_second",
                "random_first", "random_second",
                "crescent_first", "crescent_second"
            ])
            csvwriter.writerow({
                "filename": filename,
                "rows": num_rows,
                "columns": num_columns,
                "normal_first": normal_first,
                "normal_second": normal_second,
                "decrescent_first": decrescent_first,
                "decrescent_second": decrescent_second,
                "random_first": random_first,
                "random_second": random_second,
                "crescent_first": crescent_first,
                "crescent_second": crescent_second
            })

        print(f"  [INFO] Risultati salvati per il file: {filename}")

    print(f"\nRisultati dettagliati aggiornati in '{csv_file_path}'")

def test_casi_ordinati(name_file):
    benchmark_files = get_benchmark_files()

    print(f"Esecuzione del test per {name_file} ")
    print("esecuione caso normale")
    solnormal=Solver(read_file(BANCHMARK_FOLDER, name_file), name_file, debug=True, max_time=TIME_LIMIT)
    solnormal.parse_matrix()
    solnormal.calculate_solutions()
    print(f"tempo esecuzione caso normale: {solnormal.execution_time}")

    print("esecuzione permutazioni colonne decrescenti")
    sol=Solver(read_file(BANCHMARK_FOLDER, name_file), name_file, debug=True, max_time=TIME_LIMIT)
    sol.parse_matrix()
    sol.permute_columns(randomize=False, decrescent=True)
    sol.calculate_solutions()
    print(f"tempo esecuzione permutazioni colonne decrescenti: {sol.execution_time}")

    print("esecuzione permutazione colonne randomiche")
    sol1 = Solver(read_file(BANCHMARK_FOLDER, name_file), name_file, debug=True, max_time=TIME_LIMIT)
    sol1.parse_matrix()
    sol1.permute_columns(randomize=True)
    sol1.calculate_solutions()
    print(f"tempo esecuzione permutazioni colonne randomiche: {sol1.execution_time}") 

    print("esecuzione permutazione colonne crescenti")
    soldec = Solver(read_file(BANCHMARK_FOLDER, name_file), name_file, debug=True, max_time=TIME_LIMIT)
    soldec.parse_matrix()
    soldec.permute_columns(randomize=False, decrescent=False)
    soldec.calculate_solutions()
    print(f"tempo esecuzione permutazioni colonne crescenti: {soldec.execution_time}")

import csv

def rigenera_csv(csv_file_path):
    """Rigenera il file CSV aggiungendo i nomi delle colonne."""
    # Definisci i nomi delle colonne
    fieldnames = [
        "filename", "rows", "columns_initial", "columns_after_parse",
        "normal_first", "normal_second",
        "decrescent_first", "decrescent_second",
        "random_first", "random_second",
        "crescent_first", "crescent_second"
    ]

    # Leggi il contenuto esistente del file CSV
    rows = []
    if os.path.exists(csv_file_path):
        with open(csv_file_path, "r", newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            rows = list(csvreader)

    # Scrivi il file CSV con l'intestazione
    with open(csv_file_path, "w", newline="") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()  # Scrivi l'intestazione
        for row in rows:
            if len(row) == len(fieldnames):  # Assicurati che il numero di colonne corrisponda
                csvwriter.writerow(dict(zip(fieldnames, row)))

    print(f"[INFO] File CSV rigenerato con l'intestazione: {csv_file_path}")


import csv
import os

def aggiungi_intestazione_csv(csv_file_path):
    """Aggiunge un'intestazione al file CSV senza cancellare i dati esistenti."""
    # Definisci i nomi delle colonne
    fieldnames = [
        "filename", "rows", "columns_after_parse",
        "normal_first", "normal_second",
        "decrescent_first", "decrescent_second",
        "random_first", "random_second",
        "crescent_first", "crescent_second"
    ]

    # Leggi il contenuto esistente del file CSV
    if not os.path.exists(csv_file_path):
        print(f"[ERROR] Il file {csv_file_path} non esiste.")
        return

    with open(csv_file_path, "r", newline="") as csvfile:
        rows = list(csvfile)  # Leggi tutte le righe esistenti

    # Controlla se l'intestazione è già presente
    if rows and rows[0].strip() == ",".join(fieldnames):
        print("[INFO] L'intestazione è già presente nel file CSV.")
        return

    # Aggiungi l'intestazione e riscrivi il file
    with open(csv_file_path, "w", newline="") as csvfile:
        csvfile.write(",".join(fieldnames) + "\n")  # Scrivi l'intestazione
        csvfile.writelines(rows)  # Scrivi i dati esistenti

    print(f"[INFO] Intestazione aggiunta al file CSV: {csv_file_path}")


# Percorso del file CSV
csv_file_path = "detailed_results.csv"

# Aggiungi l'intestazione al file CSV
aggiungi_intestazione_csv(csv_file_path)

if __name__ == "__main__":
    #test_casi_random()
    #name_file = "c432.000.matrix"

    #test_casi_ordinati(name_file=name_file)
    test_permutazioni_colonne()