import pandas as pd
from glob import glob
from collections import Counter, defaultdict
import os

DATA_PATH = "./data/spss/defun_*.sav"
OUTPUT_CSV = "./data/csv/defunciones_2012_2022.csv"
OUTPUT_CSV_STABLE = "./data/csv/defunciones_2012_2022_columnas_estables.csv"

files = glob(DATA_PATH)

def convert(files):
    dfs = []

    for file in files:
        df = pd.read_spss(file)

        if "Edadif" in df.columns:
            df["Edadif"] = pd.to_numeric(df["Edadif"], errors="coerce")

        if "Pnadif" in df.columns:
            df["Pnadif"] = df["Pnadif"].astype(str).str.strip()

        if "Predif" in df.columns:
            df["Predif"] = df["Predif"].astype(str).str.strip()

        dfs.append(df)

    df_total = pd.concat(dfs, ignore_index=True)
    return df_total


def convert_and_save(files, output_path=OUTPUT_CSV):
    df = convert(files)
    df.to_csv(output_path, index=False)
    print(f"CSV completo guardado en: {output_path}")
    return df


def analyze_variables(files):
    variable_counter = Counter()
    variable_files = defaultdict(list)

    for file in files:
        df = pd.read_spss(file)
        filename = os.path.basename(file)

        for col in df.columns:
            variable_counter[col] += 1
            variable_files[col].append(filename)

    print("\nFrecuencia de variables:\n")
    for col, count in variable_counter.most_common():
        print(f"- {col:15} → aparece en {count} archivos")


    return variable_counter, variable_files


def get_stable_variables(variable_counter, total_files):
    stable_vars = [var for var, count in variable_counter.items() if count == total_files]
    return stable_vars


def convert_and_save_stable(files, output_path=OUTPUT_CSV_STABLE):
    variable_counter, _ = analyze_variables(files)
    total_files = len(files)

    stable_cols = get_stable_variables(variable_counter, total_files)

    print("\nVariables estables detectadas:\n")
    for col in stable_cols:
        print(f"- {col}")

    df_total = convert(files)
    df_stable = df_total[stable_cols]

    df_stable.to_csv(output_path, index=False)
    print(f"\nCSV con columnas estables guardado en: {output_path}")

    return df_stable, stable_cols


if __name__ == "__main__":
    print(f"Archivos detectados: {len(files)}")
    convert_and_save(files)

    df_stable, stable_vars = convert_and_save_stable(files)
