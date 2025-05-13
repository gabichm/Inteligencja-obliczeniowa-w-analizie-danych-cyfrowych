import pandas as pd

# Wczytaj dane z pliku CSV
filename = "episode_results.csv"  # <- przykładowa nazwa pliku
df = pd.read_csv(filename)

# Wybierz, ile pierwszych wierszy chcesz pokazać
num_rows = 40  # np. 10 pierwszych epizodów

# Generowanie tabeli markdown
markdown = "| Epizod | Nagroda | Maksymalna Pozycja | Kroki do Celu |\n"
markdown += "|--------|---------|---------------------|----------------|\n"
for index, row in df.head(num_rows).iterrows():
    markdown += f"| {row['Epizod']} | {row['Nagroda']:.6f} | {row['Maksymalna Pozycja']:.6f} | {row['Kroki do Celu']} |\n"

print(markdown)
