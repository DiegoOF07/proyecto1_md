import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns

df = pd.read_csv("./data/csv/defunciones_2012_2022_columnas_estables.csv", 
    dtype={
        "Edadif": "float64",
        "Pnadif": "string",
        "Predif": "string"
    })

features_num = ["Edadif", "Diaocu", "Añoreg"]
features_cat = ["Sexo", "Ocur"]

df_cluster = df[features_num + features_cat].dropna()


def encontrar_k_optimo():
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), features_num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), features_cat)
        ]
    )
    X = preprocessor.fit_transform(df_cluster)
    
    inertia = []
    k_values = range(2, 10)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(7, 5))
    plt.plot(k_values, inertia, marker='o')
    plt.xlabel("Número de clusters (k)")
    plt.ylabel("Inercia")
    plt.title("Método del codo para elegir k")
    plt.grid(True)
    plt.show()


def aplicar_clustering(k=4):
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), features_num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), features_cat)
        ]
    )
    
    X = preprocessor.fit_transform(df_cluster)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_cluster["cluster"] = kmeans.fit_predict(X)
    
    return df_cluster


def visualizar_clusters_pca():
    X_scaled = StandardScaler().fit_transform(df_cluster[features_num])
    
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    df_vis = df_cluster.copy()
    df_vis["PC1"] = X_pca[:, 0]
    df_vis["PC2"] = X_pca[:, 1]

    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=df_vis, x="PC1", y="PC2", hue="cluster", palette="tab10", alpha=0.6)
    plt.title("Visualización de clusters usando PCA (2D)")
    plt.grid(alpha=0.3, linestyle="--")
    plt.show()


def analizar_clusters():
    print("\nTamaño de cada cluster:")
    print(df_cluster["cluster"].value_counts().sort_index())

    print("\nPromedios por cluster:")
    print(df_cluster.groupby("cluster")[features_num].mean())

    print("\nDistribución por sexo (%):")
    print(pd.crosstab(df_cluster["cluster"], df_cluster["Sexo"], normalize='index').round(4) * 100)

    print("\nLugar de ocurrencia por cluster (%):")
    print(pd.crosstab(df_cluster["cluster"], df_cluster["Ocur"], normalize='index').round(4) * 100)


if __name__ == "__main__":
    encontrar_k_optimo()
    aplicar_clustering(k=4)
    visualizar_clusters_pca()
    analizar_clusters()