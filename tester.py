import os
import time
import signal
import sys
from algorithm import Solver
from file import read_file

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
    print("File trovati:")
    for filename in benchmarks:
        print(f"- {filename}")
    
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
    solver = Solver(instance_matrix, instance_filename, debug=True)
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

def main():
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

if __name__ == "__main__":
    main()