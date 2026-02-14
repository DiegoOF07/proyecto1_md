import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./data/defunciones_2012_2022_columnas_estables.csv", 
    dtype={
        "Edadif": "float64",
        "Pnadif": "string",
        "Predif": "string"
    })

df['Añoreg'] = df['Añoreg'].astype('Int64')
df['Diaocu'] = df['Diaocu'].astype('Int64')
df['Edadif'] = pd.to_numeric(df['Edadif'], errors='coerce').astype('Int64')


def mostrar_info_variables_numericas():
    numeric_vars_info = df[['Añoreg', 'Diaocu', 'Edadif']].describe()
    print("Información de variables numéricas:\n", numeric_vars_info)


def graficar_distribuciones():
    fig, axes = plt.subplots(2, 2, figsize=(9, 6))
    
    axes[0, 0].hist(df['Añoreg'], bins=20, color='skyblue', edgecolor='black', linewidth=1.2)
    axes[0, 0].set_title("Distribución del año de registro")
    axes[0, 0].set_xlabel("Año")
    axes[0, 0].set_ylabel("Frecuencia")
    
    axes[0, 1].hist(df['Diaocu'], bins=31, color='salmon', edgecolor='black', linewidth=1.2)
    axes[0, 1].set_title("Distribución del día de ocurrencia")
    axes[0, 1].set_xlabel("Día del mes")
    axes[0, 1].set_ylabel("Frecuencia")
    
    axes[1, 0].hist(df['Edadif'], bins=30, color='lightgreen', edgecolor='black', linewidth=1.2)
    axes[1, 0].set_title("Distribución de la edad al fallecer")
    axes[1, 0].set_xlabel("Edad")
    axes[1, 0].set_ylabel("Frecuencia")
    
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.show()


def crear_tabla_frecuencia(columna, nombre, top=None):
    counts = df[columna].value_counts()
    if top:
        counts = counts.head(top)
    
    freq_table = pd.DataFrame({
        'Frecuencia': counts,
        'Porcentaje': (counts / len(df) * 100).round(2)
    })
    freq_table['Porcentaje'] = freq_table['Porcentaje'].astype(str) + '%'
    
    print(f"\n{nombre}")
    print("-" * 80)
    print(freq_table)


def analizar_frecuencias():
    crear_tabla_frecuencia('Depocu', '1. DEPARTAMENTO DE OCURRENCIA (Top 10)', top=10)
    crear_tabla_frecuencia('Sexo', '2. SEXO')
    
    print("\n3. MES DE OCURRENCIA")
    print("-" * 80)
    mesocu_freq = pd.DataFrame({
        'Frecuencia': df['Mesocu'].value_counts().sort_index(),
        'Porcentaje': (df['Mesocu'].value_counts(normalize=True).sort_index() * 100).round(2)
    })
    mesocu_freq['Porcentaje'] = mesocu_freq['Porcentaje'].astype(str) + '%'
    print(mesocu_freq)
    
    crear_tabla_frecuencia('Ocur', '4. LUGAR DE OCURRENCIA')
    crear_tabla_frecuencia('Caudef', '5. CAUSA DE DEFUNCIÓN (Top 10)', top=10)


if __name__ == "__main__":
    mostrar_info_variables_numericas()
    graficar_distribuciones()
    analizar_frecuencias()