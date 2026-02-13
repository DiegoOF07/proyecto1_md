import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch 
import seaborn as sns
import numpy as np

df = pd.read_csv("./data/csv/defunciones_2012_2022_columnas_estables.csv", 
    dtype={
        "Edadif": "float64",
        "Pnadif": "string",
        "Predif": "string"
    })

df["Añoreg"] = df["Añoreg"].astype("Int64").astype("int")
df["Diaocu"] = df["Diaocu"].astype("Int64")
df["Edadif"] = pd.to_numeric(df["Edadif"], errors="coerce")

cols_text = ["Sexo", "Ocur", "Asist", "Depreg", "Mupreg", "Depocu", "Mupocu"]
for col in cols_text:
    df[col] = df[col].astype(str).str.strip().str.title()

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

colores = ["#FF5151", "#39C95D", "#1C93AD", "#FD7139", "#CD8CE0"]


def analisis_lugar_ocurrencia():
    print("ANÁLISIS: LUGAR DE OCURRENCIA DE DEFUNCIONES")
    ocurrencia_freq = df["Ocur"].value_counts()
    ocurrencia_pct = df["Ocur"].value_counts(normalize=True) * 100
    
    print("\nFRECUENCIA GENERAL DE LUGAR DE OCURRENCIA:")
    resumen = pd.DataFrame({
        'Frecuencia': ocurrencia_freq,
        'Porcentaje': ocurrencia_pct.round(2)
    })
    resumen['Porcentaje'] = resumen['Porcentaje'].astype(str) + '%'
    print(resumen)
    print("\n")
    
    fig, ax = plt.subplots(1, 2, figsize=(14, 8))
    
    ax[0].bar(ocurrencia_pct.index, ocurrencia_pct.values, color=colores[:len(ocurrencia_pct)], 
              edgecolor='black', linewidth=1.5, alpha=0.85)
    ax[0].set_xticks(range(len(ocurrencia_pct)))
    ax[0].set_xticklabels(ocurrencia_pct.index, rotation=15, ha='right', fontsize=10)
    ax[0].set_ylabel('Porcentaje (%)', fontsize=11)
    ax[0].set_title('Distribución General del Lugar de Ocurrencia de Defunciones', 
                    fontsize=12, pad=15)
    ax[0].grid(axis='y', alpha=0.3, linestyle='--')
    
    for i, (idx, val) in enumerate(ocurrencia_pct.items()):
        ax[0].text(i, val + 0.5, f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
    
    ct_anio_ocur = pd.crosstab(df["Añoreg"], df["Ocur"])
    
    for i, col in enumerate(ct_anio_ocur.columns):
        if col == 'Domicilio':
            ax[1].plot(ct_anio_ocur.index, ct_anio_ocur[col], marker='o', 
                       linewidth=3.5, markersize=8, label=col, color='#FF6B6B', 
                       alpha=0.9, zorder=10)
        else:
            ax[1].plot(ct_anio_ocur.index, ct_anio_ocur[col], marker='o', 
                       linewidth=2.5, markersize=6, label=col, 
                       color=colores[i % len(colores)], alpha=0.75)
    
    ax[1].set_xlabel('Año', fontsize=11)
    ax[1].set_ylabel('Número de Defunciones', fontsize=11)
    ax[1].set_title('Evolución Temporal del Lugar de Ocurrencia', 
                    fontsize=12, pad=15)
    ax[1].legend(title='Lugar de Ocurrencia', loc='best', fontsize=9, framealpha=0.9)
    ax[1].grid(True, alpha=0.3, linestyle='--')
    ax[1].set_xticks(ct_anio_ocur.index)
    
    plt.tight_layout()
    plt.show()


def analisis_defunciones_sexo():
    print("ANÁLISIS: DEFUNCIONES POR SEXO EN GUATEMALA")
    
    sexo_pct = df["Sexo"].value_counts(normalize=True) * 100
    sexo_freq = df["Sexo"].value_counts()
    
    print("\nDistribución por Sexo:")
    resumen_sexo = pd.DataFrame({
        'Frecuencia': sexo_freq,
        'Porcentaje': sexo_pct.round(2)
    })
    resumen_sexo['Porcentaje'] = resumen_sexo['Porcentaje'].astype(str) + '%'
    print(resumen_sexo)
    print("\n")
    
    colores_sexo = ["#2C95DB", '#E74C3C']
    
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))
    
    bars = ax[0].bar(sexo_pct.index, sexo_pct.values, color=colores_sexo[:len(sexo_pct)], 
                     edgecolor='black', linewidth=1.5, alpha=0.85)
    ax[0].set_xticks(range(len(sexo_pct)))
    ax[0].set_xticklabels(sexo_pct.index, rotation=0, ha='center', fontsize=11)
    ax[0].set_ylabel('Porcentaje (%)', fontsize=11)
    ax[0].set_title('Distribución General de Defunciones por Sexo', 
                    fontsize=13, pad=15)
    ax[0].grid(axis='y', alpha=0.3, linestyle='--')
    
    for i, (idx, val) in enumerate(sexo_pct.items()):
        freq = sexo_freq[idx]
        ax[0].text(i, val + 0.8, f'{val:.1f}%\n({freq:,})', 
                   ha='center', va='bottom', fontsize=10)
    
    ax[0].axhline(y=50, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Paridad (50%)')
    ax[0].legend(fontsize=9)
    
    ct_anio_sexo = pd.crosstab(df["Añoreg"], df["Sexo"])
    
    for i, col in enumerate(ct_anio_sexo.columns):
        if col == 'Hombre':
            ax[1].plot(ct_anio_sexo.index, ct_anio_sexo[col], marker='o', 
                       linewidth=3.5, markersize=8, label=col, color='#3498DB', 
                       alpha=0.9, zorder=10)
        elif col == 'Mujer':
            ax[1].plot(ct_anio_sexo.index, ct_anio_sexo[col], marker='o', 
                       linewidth=3.5, markersize=8, label=col, color='#E74C3C', 
                       alpha=0.9, zorder=10)
        else:
            ax[1].plot(ct_anio_sexo.index, ct_anio_sexo[col], marker='o', 
                       linewidth=2.5, markersize=6, label=col, 
                       color=colores_sexo[i % len(colores_sexo)], alpha=0.75)
    
    ax[1].set_xlabel('Año', fontsize=11)
    ax[1].set_ylabel('Número de Defunciones', fontsize=11)
    ax[1].set_title('Evolución Temporal de Defunciones por Sexo', 
                    fontsize=13, pad=15)
    ax[1].legend(title='Sexo', loc='best', fontsize=10, framealpha=0.9)
    ax[1].grid(True, alpha=0.3, linestyle='--')
    ax[1].set_xticks(ct_anio_sexo.index)
    
    plt.tight_layout()
    plt.show()


def analisis_pandemia():
    print("ANÁLISIS: DEFUNCIONES DURANTE 2020-2021 vs AÑOS ANTERIORES")
    
    defunciones_anio = df["Añoreg"].value_counts().sort_index()
    
    print("\nDefunciones por Año:")
    for anio, cantidad in defunciones_anio.items():
        print(f"Año {anio}: {cantidad:,} defunciones")
    
    pre_pandemia = defunciones_anio[defunciones_anio.index < 2020]
    pandemia = defunciones_anio[(defunciones_anio.index >= 2020) & (defunciones_anio.index <= 2021)]
    
    promedio_pre = pre_pandemia.mean()
    promedio_pandemia = pandemia.mean()
    
    print(f"\nPromedio anual pre-pandemia (2012-2019): {promedio_pre:,.0f}")
    print(f"Promedio anual pandemia (2020-2021): {promedio_pandemia:,.0f}")
    print(f"Incremento: {promedio_pandemia - promedio_pre:,.0f} ({((promedio_pandemia/promedio_pre - 1) * 100):.1f}%)\n")
    
    colores_anios = ["#A2C0C2" if year < 2020 else '#E74C3C' if year <= 2021 else '#3498DB'
                     for year in defunciones_anio.index]
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    bars = ax[0].bar(defunciones_anio.index, defunciones_anio.values,
                     color=colores_anios, edgecolor='black', linewidth=1.5, alpha=0.85)
    
    ax[0].set_ylabel('Número de Defunciones')
    ax[0].set_title('Defunciones por Año en Guatemala (2012-2022)')
    ax[0].grid(axis='y', alpha=0.3, linestyle='--')
    
    for anio, val in defunciones_anio.items():
        ax[0].text(anio, val + 500, f'{val:,}', ha='center', va='bottom', fontsize=9)
    
    ax[0].axhline(y=promedio_pre, color='#2ECC71', linestyle='--', linewidth=2,
                  label=f'Promedio Pre-Pandemia ({promedio_pre:,.0f})')
    ax[0].axhline(y=promedio_pandemia, color='#E74C3C', linestyle='--', linewidth=2,
                  label=f'Promedio Pandemia ({promedio_pandemia:,.0f})')
    ax[0].legend(fontsize=9)
    
    ax[1].plot(defunciones_anio.index, defunciones_anio.values, 
               marker='o', linewidth=3, markersize=8, color='#3498DB')
    
    for year in [2020, 2021]:
        if year in defunciones_anio.index:
            ax[1].plot(year, defunciones_anio[year], marker='o', 
                      markersize=12, color='#E74C3C', zorder=10)
    
    ax[1].set_xlabel('Año')
    ax[1].set_ylabel('Número de Defunciones')
    ax[1].set_title('Tendencia de Defunciones (2012-2022)')
    ax[1].grid(True, alpha=0.3, linestyle='--')
    ax[1].axhline(y=promedio_pre, color='#2ECC71', linestyle='--', linewidth=2, alpha=0.5)
    
    plt.tight_layout()
    plt.show()


def analisis_departamentos():
    print("ANÁLISIS: DEFUNCIONES POR DEPARTAMENTO")
    
    defunciones_dep = df["Depreg"].value_counts()
    print(f"\nTop 10 Departamentos con más defunciones:")
    print(defunciones_dep.head(10))
    
    guatemala_defunciones = defunciones_dep.get('Guatemala', 0)
    total_defunciones = defunciones_dep.sum()
    resto_defunciones = total_defunciones - guatemala_defunciones
    
    pct_guatemala = (guatemala_defunciones / total_defunciones) * 100
    pct_resto = (resto_defunciones / total_defunciones) * 100
    
    print(f"\nDefunciones en Guatemala: {guatemala_defunciones:,} ({pct_guatemala:.1f}%)")
    print(f"Defunciones en el resto del país: {resto_defunciones:,} ({pct_resto:.1f}%)")
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    top_10 = defunciones_dep.head(10)
    colores_dep = ['#E74C3C' if dep == 'Guatemala' else '#3498DB' for dep in top_10.index]
    
    ax[0].barh(range(len(top_10)), top_10.values, color=colores_dep, 
               edgecolor='black', linewidth=1.5, alpha=0.85)
    ax[0].set_yticks(range(len(top_10)))
    ax[0].set_yticklabels(top_10.index, fontsize=10)
    ax[0].set_xlabel('Número de Defunciones', fontsize=11)
    ax[0].set_title('Top 10 Departamentos con Mayor Número de Defunciones', 
                    fontsize=12, pad=15)
    ax[0].grid(axis='x', alpha=0.3, linestyle='--')
    ax[0].invert_yaxis()
    
    for i, val in enumerate(top_10.values):
        ax[0].text(val + (top_10.max() * 0.01), i, f'{val:,}', 
                   va='center', fontsize=9)
    
    labels = ['Guatemala', 'Resto del País']
    values = [guatemala_defunciones, resto_defunciones]
    colors = ['#E74C3C', '#3498DB']
    explode = (0.1, 0)
    
    wedges, texts, autotexts = ax[1].pie(values, labels=labels, autopct='%1.1f%%', 
                                          startangle=90, explode=explode,
                                          colors=colors, wedgeprops=dict(edgecolor='black'))
    ax[1].set_title("Proporción de Defunciones: Guatemala vs Resto del País")
    
    plt.tight_layout()
    plt.show()


def analisis_edad():
    print("ANÁLISIS: CONCENTRACIÓN DE DEFUNCIONES POR EDAD")
    
    df_edad = df[df["Edadif"].notna()].copy()
    
    grupos_edad = {
        '0-17 años (Niños/Adolescentes)': (0, 17),
        '18-39 años (Jóvenes)': (18, 39),
        '40-59 años (Adultos)': (40, 59),
        '60-79 años (Adultos Mayores)': (60, 79),
        '80+ años (Ancianos)': (80, 150)
    }
    
    def clasificar_edad(edad):
        for grupo, (min_edad, max_edad) in grupos_edad.items():
            if min_edad <= edad <= max_edad:
                return grupo
        return 'Desconocido'
    
    df_edad['Grupo_Edad'] = df_edad['Edadif'].apply(clasificar_edad)
    
    defunciones_grupo = df_edad['Grupo_Edad'].value_counts()
    orden_grupos = list(grupos_edad.keys())
    defunciones_grupo = defunciones_grupo.reindex(orden_grupos)
    
    print("\nDefunciones por Grupo de Edad:")
    print("-" * 80)
    total_defunciones = defunciones_grupo.sum()
    for grupo, cant in defunciones_grupo.items():
        pct = (cant / total_defunciones) * 100
        print(f"{grupo}: {cant:,} ({pct:.1f}%)")
    
    edad_promedio = df_edad['Edadif'].mean()
    edad_mediana = df_edad['Edadif'].median()
    edad_moda = df_edad['Edadif'].mode()[0] if len(df_edad['Edadif'].mode()) > 0 else 0
    
    print(f"\nEstadísticas de Edad al Fallecer:")
    print("-" * 80)
    print(f"Edad Promedio: {edad_promedio:.1f} años")
    print(f"Edad Mediana: {edad_mediana:.1f} años")
    print(f"Edad Moda: {edad_moda:.0f} años")
    
    mayores_60 = defunciones_grupo.loc['60-79 años (Adultos Mayores)':'80+ años (Ancianos)'].sum()
    pct_mayores_60 = (mayores_60 / total_defunciones) * 100
    
    print(f"\nDefunciones en personas ≥60 años: {mayores_60:,} ({pct_mayores_60:.1f}%)")
    
    print("\nResultado:")
    if pct_mayores_60 > 50:
        print(f"SÍ, las defunciones SE CONCENTRAN en personas de mayor edad (≥60 años)")
        print(f"Más del 50% de las defunciones ocurren en este grupo ({pct_mayores_60:.1f}%)")
    else:
        print(f"NO, las defunciones NO se concentran principalmente en mayores (≥60 años)")
        print(f"Solo el {pct_mayores_60:.1f}% de defunciones ocurren en este grupo")
    
    print("\n")
    
    colores_grupos = ['#3498DB', '#F39C12', '#E74C3C', '#8E44AD', '#C0392B']
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    ax[0].bar(range(len(defunciones_grupo)), defunciones_grupo.values, 
              color=colores_grupos, edgecolor='black', linewidth=1.5, alpha=0.85)
    ax[0].set_xticks(range(len(defunciones_grupo)))
    ax[0].set_xticklabels(defunciones_grupo.index, rotation=20, ha='right', fontsize=10)
    ax[0].set_ylabel("Número de Defunciones", fontsize=11)
    ax[0].set_title("Distribución de Defunciones por Grupo de Edad", 
                    fontsize=13, pad=15)
    ax[0].grid(axis='y', alpha=0.3, linestyle='--')
    
    for i, (grupo, cant) in enumerate(defunciones_grupo.items()):
        pct = (cant / total_defunciones) * 100
        ax[0].text(i, cant + (defunciones_grupo.max() * 0.01), 
                   f"{cant:,}\n({pct:.1f}%)", 
                   ha='center', va='bottom', fontsize=9)
    
    ax[0].axhline(y=defunciones_grupo.mean(), color='red', linestyle='--', 
                  linewidth=2, alpha=0.6, label=f'Promedio ({defunciones_grupo.mean():,.0f})')
    ax[0].legend(fontsize=10)
    
    menores_60 = total_defunciones - mayores_60
    labels_edad = ['≥60 años\n(Mayor Edad)', '<60 años\n(Edad Joven/Media)']
    values_edad = [mayores_60, menores_60]
    colors_edad = ['#8E44AD', '#3498DB']
    explode = (0.1, 0)
    
    wedges, texts, autotexts = ax[1].pie(values_edad, labels=labels_edad, autopct='%1.1f%%', 
                                          startangle=90, colors=colors_edad, 
                                          explode=explode,
                                          wedgeprops=dict(edgecolor='black', linewidth=2),
                                          textprops=dict(fontsize=11))
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
    
    ax[1].set_title("Proporción de Defunciones: Mayor vs Menor Edad", 
                    fontsize=13, pad=15)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analisis_lugar_ocurrencia()
    analisis_defunciones_sexo()
    analisis_pandemia()
    analisis_departamentos()
    analisis_edad()