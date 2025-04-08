import pandas as pd

# Carica il file CSV
CSV_FILE = "performance_comparison.csv"
df = pd.read_csv(CSV_FILE)

# Filtra i dati validi (escludi righe con "TOO LARGE" o "TIME LIMIT")
valid_df = df[
    (df["termination_status_dz"] == "TERMINATED") | (df["termination_status_dz_dd"] == "TERMINATED")
]

# Conteggio delle soluzioni trovate
only_dz = valid_df[
    (valid_df["termination_status_dz"] == "TERMINATED") & (valid_df["termination_status_dz_dd"] != "TERMINATED")
].shape[0]

only_dz_dd = valid_df[
    (valid_df["termination_status_dz_dd"] == "TERMINATED") & (valid_df["termination_status_dz"] != "TERMINATED")
].shape[0]

both_terminated = valid_df[
    (valid_df["termination_status_dz"] == "TERMINATED") & (valid_df["termination_status_dz_dd"] == "TERMINATED")
].shape[0]

# Differenza di colonne
valid_columns_diff = valid_df.dropna(subset=["columns_after_dz", "columns_after_dz_dd"]).copy()
valid_columns_diff["columns_diff"] = valid_columns_diff["columns_after_dz"] - valid_columns_diff["columns_after_dz_dd"]
mean_columns_diff = valid_columns_diff["columns_diff"].mean()
max_columns_diff = valid_columns_diff["columns_diff"].max()

# Differenza di tempo (quando entrambi trovano la soluzione)
valid_time_diff = valid_df.dropna(subset=["time_dz", "time_dz_dd"]).copy()
valid_time_diff.loc[:, "time_diff"] = valid_time_diff["time_dz"] - valid_time_diff["time_dz_dd"]
mean_time_diff = valid_time_diff["time_diff"].mean()
max_time_diff = valid_time_diff["time_diff"].max()

# Differenza di memoria (quando entrambi trovano la soluzione)
valid_memory_diff = valid_df.dropna(subset=["memory_dz", "memory_dz_dd"]).copy()
valid_memory_diff.loc[:, "memory_diff"] = valid_memory_diff["memory_dz"] - valid_memory_diff["memory_dz_dd"]
mean_memory_diff = valid_memory_diff["memory_diff"].mean()
max_memory_diff = valid_memory_diff["memory_diff"].max()

# Stampa i risultati
print("Analisi delle Performance:")
print(f"Soluzioni trovate solo da dz: {only_dz}")
print(f"Soluzioni trovate solo da dz_dd: {only_dz_dd}")
print(f"Soluzioni trovate da entrambi: {both_terminated}")
print()
print(f"Differenza media di colonne: {mean_columns_diff:.2f}")
print(f"Differenza massima di colonne: {max_columns_diff:.2f}")
print()
print(f"Differenza media di tempo (dz - dz_dd): {mean_time_diff:.2f} secondi")
print(f"Differenza massima di tempo (dz - dz_dd): {max_time_diff:.2f} secondi")
print()
print(f"Differenza media di memoria (dz - dz_dd): {mean_memory_diff:.2f} KB")
print(f"Differenza massima di memoria (dz - dz_dd): {max_memory_diff:.2f} KB")