import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carica il file CSV
CSV_FILE = "permutation_results.csv"
df = pd.read_csv(CSV_FILE)

# Filtra i dati: escludi file senza dati e con TIME LIMIT
filtered_df = df.dropna(subset=["time_no_permutation", "memory_no_permutation"])
filtered_df = filtered_df[
    (filtered_df["time_no_permutation"] != "TIME LIMIT") &
    (filtered_df["time_random_permutation"] != "TIME LIMIT") &
    (filtered_df["time_decrescent_permutation"] != "TIME LIMIT") &
    (filtered_df["time_crescent_permutation"] != "TIME LIMIT")
]

# Converti i dati in numeri
columns_to_convert = [
    "time_no_permutation", "memory_no_permutation",
    "time_random_permutation", "memory_random_permutation",
    "time_decrescent_permutation", "memory_decrescent_permutation",
    "time_crescent_permutation", "memory_crescent_permutation"
]
filtered_df[columns_to_convert] = filtered_df[columns_to_convert].apply(pd.to_numeric)

# Calcola il numero di casi completati per ogni scenario
completed_cases = {
    "No Permutation": filtered_df["time_no_permutation"].count(),
    "Random Permutation": filtered_df["time_random_permutation"].count(),
    "Decrescent Permutation": filtered_df["time_decrescent_permutation"].count(),
    "Crescent Permutation": filtered_df["time_crescent_permutation"].count()
}

# Calcola i tempi medi e le memorie medie
average_times = {
    "No Permutation": filtered_df["time_no_permutation"].mean(),
    "Random Permutation": filtered_df["time_random_permutation"].mean(),
    "Decrescent Permutation": filtered_df["time_decrescent_permutation"].mean(),
    "Crescent Permutation": filtered_df["time_crescent_permutation"].mean()
}

average_memories = {
    "No Permutation": filtered_df["memory_no_permutation"].mean(),
    "Random Permutation": filtered_df["memory_random_permutation"].mean(),
    "Decrescent Permutation": filtered_df["memory_decrescent_permutation"].mean(),
    "Crescent Permutation": filtered_df["memory_crescent_permutation"].mean()
}

# Calcola le differenze percentuali rispetto al caso senza permutazioni
time_differences = {
    key: ((value - average_times["No Permutation"]) / average_times["No Permutation"]) * 100
    for key, value in average_times.items()
}

memory_differences = {
    key: ((value - average_memories["No Permutation"]) / average_memories["No Permutation"]) * 100
    for key, value in average_memories.items()
}

# Grafico 1: Numero di casi completati
plt.figure(figsize=(8, 6))
plt.bar(completed_cases.keys(), completed_cases.values(), color=["blue", "orange", "green", "red"])
plt.title("Numero di Casi Completati per Scenario")
plt.ylabel("Numero di Casi")
plt.savefig("completed_cases.png")
plt.close()

# Grafico 2: Confronto dei tempi medi
plt.figure(figsize=(8, 6))
plt.bar(average_times.keys(), average_times.values(), color=["blue", "orange", "green", "red"])
plt.title("Confronto dei Tempi Medi per Scenario")
plt.ylabel("Tempo Medio (s)")
plt.savefig("average_times.png")
plt.close()

# Grafico 3: Confronto delle memorie medie
plt.figure(figsize=(8, 6))
plt.bar(average_memories.keys(), average_memories.values(), color=["blue", "orange", "green", "red"])
plt.title("Confronto delle Memorie Medie per Scenario")
plt.ylabel("Memoria Media (KB)")
plt.savefig("average_memories.png")
plt.close()

# Stampa i risultati
print("Tempi Medi (s):")
for key, value in average_times.items():
    print(f"{key}: {value:.2f}")

print("\nMemorie Medie (KB):")
for key, value in average_memories.items():
    print(f"{key}: {value:.2f}")

print("\nDifferenze Percentuali nei Tempi (%):")
for key, value in time_differences.items():
    print(f"{key}: {value:.2f}%")

print("\nDifferenze Percentuali nelle Memorie (%):")
for key, value in memory_differences.items():
    print(f"{key}: {value:.2f}%")