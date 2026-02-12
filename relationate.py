import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("./data/csv/defunciones_2012_2022_columnas_estables.csv")

df["Añoreg"] = df["Añoreg"].astype("Int64")
df["Diaocu"] = df["Diaocu"].astype("Int64")
df["Edadif"] = pd.to_numeric(df["Edadif"], errors="coerce")

cols_text = ["Sexo", "Ocur", "Asist", "Depreg", "Mupreg", "Depocu", "Mupocu"]
for col in cols_text:
    df[col] = df[col].astype(str).str.strip().str.title()

# Mapeo para causas de muerte (CIE-10)
causas_map = {
    "E149": "Diabetes mellitus (no especificada)",
    "I219": "Infarto agudo de miocardio (no especificado)",
    "I64X": "Accidente cerebrovascular (no especificado)",
    "J189": "Neumonía (no especificada)",
    "K746": "Enfermedad hepática crónica (no especificada)",
    "R54X": "Senilidad / vejez",
    "R98X": "Muerte con hallazgos clínicos no especificados",
    "R99X": "Otras causas mal definidas",
    "U071": "COVID-19",
    "X599": "Accidente no especificado"
}

df["Causa_extendida"] = df["Caudef"].map(causas_map).fillna("Otra causa")

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

print("1. RELACIÓN: SEXO vs LUGAR DE OCURRENCIA")
ct_sexo_ocur = pd.crosstab(df["Sexo"], df["Ocur"], normalize="index") * 100
print(ct_sexo_ocur.round(2), "\n")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ct_sexo_ocur.plot(kind='bar', ax=axes[0], edgecolor='black', alpha=0.85)
axes[0].set_title('Distribución de Lugar de Ocurrencia por Sexo')
axes[0].set_xlabel('Sexo')
axes[0].set_ylabel('Porcentaje (%)')
axes[0].legend(title='Lugar de Ocurrencia', bbox_to_anchor=(1.05, 1), loc='upper left')

sns.heatmap(ct_sexo_ocur, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1])
axes[1].set_title('Mapa de Calor: Sexo vs Lugar de Ocurrencia')

plt.tight_layout()
plt.show()


print("2. RELACIÓN: TOP 5 DEPARTAMENTOS vs LUGAR DE OCURRENCIA")
top5 = df["Depreg"].value_counts().head(5).index
ct_dep_ocur = pd.crosstab(df[df["Depreg"].isin(top5)]["Depreg"], df["Ocur"], normalize="index") * 100
print(ct_dep_ocur.round(2), "\n")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

ct_dep_ocur.plot(kind='barh', ax=axes[0], edgecolor='black', alpha=0.85)
axes[0].set_title('Lugar de Ocurrencia por Departamento (Top 5)')
axes[0].set_xlabel('Porcentaje (%)')

sns.heatmap(ct_dep_ocur, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1])
axes[1].set_title('Mapa de Calor: Departamento vs Lugar de Ocurrencia')

plt.tight_layout()
plt.show()


print("3. EVOLUCIÓN TEMPORAL: LUGAR DE OCURRENCIA POR AÑO")
ct_anio_ocur = pd.crosstab(df["Añoreg"], df["Ocur"])
print(ct_anio_ocur.tail(), "\n")

ct_anio_ocur.plot(figsize=(12, 6), marker='o')
plt.title("Evolución de Defunciones por Lugar de Ocurrencia")
plt.xlabel("Año")
plt.ylabel("Número de Defunciones")
plt.grid(True, alpha=0.3)
plt.show()


print("4. TOP 10 CAUSAS DE DEFUNCIÓN vs SEXO")
top_causas = df["Causa_extendida"].value_counts().head(10).index
ct_causa_sexo = pd.crosstab(df[df["Causa_extendida"].isin(top_causas)]["Causa_extendida"], df["Sexo"], normalize="index") * 100
print(ct_causa_sexo.round(2), "\n")

# Crear figura
fig, ax = plt.subplots(figsize=(12, 8))

# Ordenar por la primera columna
ct_causa_sexo_sorted = ct_causa_sexo.sort_values(by=ct_causa_sexo.columns[0], ascending=True)
y_pos = np.arange(len(ct_causa_sexo_sorted))

if ct_causa_sexo_sorted.shape[1] >= 2:
    ax.barh(y_pos, ct_causa_sexo_sorted.iloc[:, 0], color='#e74c3c', alpha=0.85, 
            label=ct_causa_sexo_sorted.columns[0], edgecolor='black', linewidth=1.2)
    ax.barh(y_pos, -ct_causa_sexo_sorted.iloc[:, 1], color='#3498db', alpha=0.85, 
            label=ct_causa_sexo_sorted.columns[1], edgecolor='black', linewidth=1.2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ct_causa_sexo_sorted.index, fontsize=9)
    ax.set_xlabel('Porcentaje (%)', fontsize=11)
    ax.set_title('Distribución por Sexo en Top 10 Causas de Defunción - Comparación Divergente', 
                 fontsize=13, fontweight='bold', pad=15)
    ax.axvline(x=0, color='black', linewidth=1.5)
    ax.legend(loc='best', fontsize=10)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    x_labels = ax.get_xticks()
    ax.set_xticklabels([f'{abs(int(x))}%' for x in x_labels])

plt.tight_layout()
plt.show()


print("5. DISTRIBUCIÓN DE EDAD AL FALLECER POR SEXO")
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

axes[0].hist(df[df["Sexo"] == "Hombre"]["Edadif"].dropna(), bins=30, edgecolor='black', alpha=0.7, color='#3498db')
axes[0].set_title("Hombres")
axes[0].set_xlabel("Edad")
axes[0].set_ylabel("Frecuencia")

axes[1].hist(df[df["Sexo"] == "Mujer"]["Edadif"].dropna(), bins=30, edgecolor='black', alpha=0.7, color='#e74c3c')
axes[1].set_title("Mujeres")
axes[1].set_xlabel("Edad")

fig.suptitle("Distribución de Edad al Fallecer por Sexo")
plt.tight_layout()
plt.show()
