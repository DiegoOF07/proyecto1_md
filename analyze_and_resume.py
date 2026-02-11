import pandas as pd
import matplotlib.pyplot as plt

df_stable = pd.read_csv("./data/csv/defunciones_2012_2022_columnas_estables.csv")
df = df_stable.copy()

df['Añoreg'] = df['Añoreg'].astype('Int64')
df['Diaocu'] = df['Diaocu'].astype('Int64')
df['Edadif'] = pd.to_numeric(df['Edadif'], errors='coerce').astype('Int64')

numeric_vars_info = df[['Añoreg', 'Diaocu', 'Edadif']].describe()
print("Información de variables numéricas:\n", numeric_vars_info)

fig, axes = plt.subplots(2, 2, figsize=(9, 6))

# Gráfica 1: Año de registro
axes[0, 0].hist(df['Añoreg'], bins=20, color='skyblue', edgecolor='black', linewidth=1.2)
axes[0, 0].set_title("Distribución del año de registro")
axes[0, 0].set_xlabel("Año")
axes[0, 0].set_ylabel("Frecuencia")

# Gráfica 2: Día de ocurrencia
axes[0, 1].hist(df['Diaocu'], bins=31, color='salmon', edgecolor='black', linewidth=1.2)
axes[0, 1].set_title("Distribución del día de ocurrencia")
axes[0, 1].set_xlabel("Día del mes")
axes[0, 1].set_ylabel("Frecuencia")

# Gráfica 3: Edad al fallecer
axes[1, 0].hist(df['Edadif'], bins=30, color='lightgreen', edgecolor='black', linewidth=1.2)
axes[1, 0].set_title("Distribución de la edad al fallecer")
axes[1, 0].set_xlabel("Edad")
axes[1, 0].set_ylabel("Frecuencia")

axes[1, 1].axis('off')

plt.tight_layout()
plt.show()

df['Depocu'].value_counts().head(10)
df['Sexo'].value_counts(normalize=True)
df['Mesocu'].value_counts()
df['Ocur'].value_counts()
df['Caudef'].value_counts().head(10)

# 1. Departamento de ocurrencia (Top 10)
print("\n1. DEPARTAMENTO DE OCURRENCIA (Top 10)")
print("-" * 80)
depocu_freq = pd.DataFrame({
    'Frecuencia': df['Depocu'].value_counts().head(10),
    'Porcentaje': (df['Depocu'].value_counts(normalize=True).head(10) * 100).round(2)
})
depocu_freq['Porcentaje'] = depocu_freq['Porcentaje'].astype(str) + '%'
print(depocu_freq)

# 2. Sexo
print("\n2. SEXO")
print("-" * 80)
sexo_freq = pd.DataFrame({
    'Frecuencia': df['Sexo'].value_counts(),
    'Porcentaje': (df['Sexo'].value_counts(normalize=True) * 100).round(2)
})
sexo_freq['Porcentaje'] = sexo_freq['Porcentaje'].astype(str) + '%'
print(sexo_freq)

# 3. Mes de ocurrencia
print("\n3. MES DE OCURRENCIA")
print("-" * 80)
mesocu_freq = pd.DataFrame({
    'Frecuencia': df['Mesocu'].value_counts().sort_index(),
    'Porcentaje': (df['Mesocu'].value_counts(normalize=True).sort_index() * 100).round(2)
})
mesocu_freq['Porcentaje'] = mesocu_freq['Porcentaje'].astype(str) + '%'
print(mesocu_freq)

# 4. Lugar de ocurrencia
print("\n4. LUGAR DE OCURRENCIA")
print("-" * 80)
ocur_freq = pd.DataFrame({
    'Frecuencia': df['Ocur'].value_counts(),
    'Porcentaje': (df['Ocur'].value_counts(normalize=True) * 100).round(2)
})
ocur_freq['Porcentaje'] = ocur_freq['Porcentaje'].astype(str) + '%'
print(ocur_freq)

# 5. Causa de defunción (Top 10)
print("\n5. CAUSA DE DEFUNCIÓN (Top 10)")
print("-" * 80)
caudef_freq = pd.DataFrame({
    'Frecuencia': df['Caudef'].value_counts().head(10),
    'Porcentaje': (df['Caudef'].value_counts(normalize=True).head(10) * 100).round(2)
})
caudef_freq['Porcentaje'] = caudef_freq['Porcentaje'].astype(str) + '%'
print(caudef_freq)
