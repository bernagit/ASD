import pandas as pd
import matplotlib.pyplot as plt

# Carica il file CSV
CSV_FILE = "detailed_results.csv"
df = pd.read_csv(CSV_FILE)

# Filtra i dati: ignora i file che non hanno nessun dato
filtered_df = df.dropna(subset=["normal_first", "decrescent_first", "random_first", "crescent_first"], how="all")

# Conta il numero di prime e seconde soluzioni trovate per ogni caso
counts = {
    "Normal First": filtered_df["normal_first"].notna().sum(),
    "Normal Second": filtered_df["norm_second"].notna().sum(),
    "Decrescent First": filtered_df["decrescent_first"].notna().sum(),
    "Decrescent Second": filtered_df["decrescent_second"].notna().sum(),
    "Random First": filtered_df["random_first"].notna().sum(),
    "Random Second": filtered_df["random_second"].notna().sum(),
    "Crescent First": filtered_df["crescent_first"].notna().sum(),
    "Crescent Second": filtered_df["crescent_second"].notna().sum(),
}

# Calcola i tempi medi per ogni caso
average_times_first = {
    "Normal First": filtered_df["normal_first"].mean(),
    "Decrescent First": filtered_df["decrescent_first"].mean(),
    "Random First": filtered_df["random_first"].mean(),
    "Crescent First": filtered_df["crescent_first"].mean(),
}

average_times_second = {
    "Normal Second": filtered_df["norm_second"].mean(),
    "Decrescent Second": filtered_df["decrescent_second"].mean(),
    "Random Second": filtered_df["random_second"].mean(),
    "Crescent Second": filtered_df["crescent_second"].mean(),
}

# Calcola le differenze percentuali rispetto al caso decrescente (separate per prime e seconde soluzioni)
percent_differences_first = {
    key: ((value - average_times_first["Decrescent First"]) / average_times_first["Decrescent First"]) * 100
    for key, value in average_times_first.items()
}

percent_differences_second = {
    key: ((value - average_times_second["Decrescent Second"]) / average_times_second["Decrescent Second"]) * 100
    for key, value in average_times_second.items()
}

# Definisci una mappa di colori coerente per i casi
color_map_first = {
    "Normal First": "blue",
    "Decrescent First": "green",
    "Random First": "darkgrey",
    "Crescent First": "purple",
}

color_map_second = {
    "Normal Second": "lightblue",
    "Decrescent Second": "lightgreen",
    "Random Second": "lightgrey",
    "Crescent Second": "pink",
}

# Grafico 1: Numero di prime e seconde soluzioni trovate
plt.figure(figsize=(10, 6))
plt.bar(counts.keys(), counts.values(), color=[
    color_map_first.get(key, color_map_second.get(key, "black")) for key in counts.keys()
])
plt.title("Numero di Soluzioni Trovate per Caso")
plt.ylabel("Numero di Soluzioni")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("solutions_found.png")
plt.close()

# Grafico 2: Tempi medi per le prime soluzioni
plt.figure(figsize=(10, 6))
plt.bar(average_times_first.keys(), average_times_first.values(), color=[color_map_first[key] for key in average_times_first.keys()])
plt.title("Tempi Medi per le Prime Soluzioni")
plt.ylabel("Tempo Medio (s)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_times_first.png")
plt.close()

# Grafico 3: Tempi medi per le seconde soluzioni
plt.figure(figsize=(10, 6))
plt.bar(average_times_second.keys(), average_times_second.values(), color=[color_map_second[key] for key in average_times_second.keys()])
plt.title("Tempi Medi per le Seconde Soluzioni")
plt.ylabel("Tempo Medio (s)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_times_second.png")
plt.close()

# Stampa i risultati
print("Numero di Soluzioni Trovate:")
for key, value in counts.items():
    print(f"{key}: {value}")

print("\nTempi Medi per le Prime Soluzioni (s):")
for key, value in average_times_first.items():
    print(f"{key}: {value:.6f}")

print("\nTempi Medi per le Seconde Soluzioni (s):")
for key, value in average_times_second.items():
    print(f"{key}: {value:.6f}")

print("\nDifferenze Percentuali per le Prime Soluzioni rispetto al Caso Decrescente:")
for key, value in percent_differences_first.items():
    print(f"{key}: {value:.2f}%")

print("\nDifferenze Percentuali per le Seconde Soluzioni rispetto al Caso Decrescente:")
for key, value in percent_differences_second.items():
    print(f"{key}: {value:.2f}%")