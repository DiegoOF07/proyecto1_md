# Análisis de Mortalidad en Guatemala (2012-2022)

## Descripción del Proyecto

Este proyecto realiza un análisis estadístico exhaustivo de las defunciones registradas en Guatemala durante el período 2012-2022. Utilizando datos oficiales en formato SPSS, el análisis explora patrones demográficos, temporales y geográficos de la mortalidad, con especial énfasis en el impacto de la pandemia de COVID-19.

## Estructura del Proyecto

```
├── data/
│   ├── spss/                          # Archivos SPSS originales (defun_*.sav)
│   ├── defunciones_2012_2022.csv     # Dataset completo unificado
│   └── defunciones_2012_2022_columnas_estables.csv  # Dataset con columnas estables
├── convert_and_reduce.py              # Conversión SPSS → CSV y análisis de variables
├── analyze_and_resume.py              # Análisis descriptivo básico
├── relationate.py                     # Análisis de relaciones entre variables
├── prove_questions.py                 # Respuesta a preguntas específicas de investigación
├── clustering.py                      # Análisis de clustering (K-Means)
└── README.md
```

## Requisitos e Instalación

### Dependencias

```bash
pip install pandas matplotlib seaborn numpy scikit-learn pyreadstat
```
### Configuración

1. Clonar el repositorio
2. Ejecutar los scripts en el siguiente orden

### 1. `convert_and_reduce.py` - Procesamiento Inicial
**Ejecutar:**
```bash
python convert_and_reduce.py
```
---

### 2. `analyze_and_resume.py` - Análisis Descriptivo
**Ejecutar:**
```bash
python analyze_and_resume.py
```

---

### 3. `relationate.py` - Análisis de Relaciones

**Ejecutar:**
```bash
python relationate.py
```
---
### 4. `prove_questions.py` - Preguntas de Investigación

**Ejecutar:**
```bash
python prove_questions.py
```
---

### 5. `clustering.py` - Análisis de Clustering

**Ejecutar:**
```bash
python clustering.py
```

