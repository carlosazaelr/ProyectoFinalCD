import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import confusion_matrix

# Configuración visual para reportes
sns.set_theme(style="whitegrid", palette="muted")

carpeta_salida = "graficas_estudio"
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

print("=============================================================================")
print(" FASE 1 Y 2: EXTRACCIÓN DE DICCIONARIOS Y LIMPIEZA")
print("=============================================================================\n")

df_num = pd.read_csv("respuestas_estudio.csv")
df_txt = pd.read_csv("respuestas_estudio_etiquetas.csv")

# Creación de diccionarios
df_mapeo = pd.merge(
    df_num[['id', 'genero', 'principal_estresor', 'calidad_sueno', 'nivel_estres', 'carrera', 'situacion_laboral']],
    df_txt[['id', 'genero', 'principal_estresor', 'calidad_sueno', 'nivel_estres', 'carrera', 'situacion_laboral']],
    on='id', suffixes=('_num', '_txt')
)

dicc_genero = dict(zip(df_mapeo['genero_num'], df_mapeo['genero_txt']))
dicc_estresor = dict(zip(df_mapeo['principal_estresor_num'], df_mapeo['principal_estresor_txt']))
dicc_sueno = dict(zip(df_mapeo['calidad_sueno_num'], df_mapeo['calidad_sueno_txt']))
dicc_nivel = dict(zip(df_mapeo['nivel_estres_num'], df_mapeo['nivel_estres_txt']))
dicc_carrera = dict(zip(df_mapeo['carrera_num'], df_mapeo['carrera_txt']))
dicc_laboral = dict(zip(df_mapeo['situacion_laboral_num'], df_mapeo['situacion_laboral_txt']))

# Limpieza del numérico
df_clean = df_num.copy()
columnas_irrelevantes = ['id', 'fecha_registro']
df_clean = df_clean.drop(columns=[col for col in columnas_irrelevantes if col in df_clean.columns])
df_clean = df_clean.dropna(subset=['nivel_estres'])

# Outliers
df_clean.loc[(df_clean['edad'] < 16) | (df_clean['edad'] > 80), 'edad'] = np.nan
df_clean.loc[(df_clean['estatura'] < 130) | (df_clean['estatura'] > 230), 'estatura'] = np.nan
df_clean.loc[(df_clean['peso'] < 35) | (df_clean['peso'] > 200), 'peso'] = np.nan
df_clean.loc[(df_clean['comidas'] < 1) | (df_clean['comidas'] > 6), 'comidas'] = np.nan

# Imputación
num_cols = df_clean.select_dtypes(include=[np.number]).columns
imputer_num = SimpleImputer(strategy='median')
if len(num_cols) > 0:
    df_clean[num_cols] = imputer_num.fit_transform(df_clean[num_cols])

cols_a_entero = ['genero', 'principal_estresor', 'calidad_sueno', 'nivel_estres', 'carrera', 'situacion_laboral']
for col in cols_a_entero:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].round().astype(int)

# DataFrame para visualizaciones (EDA)
df_plot = df_clean.copy()
df_plot['genero'] = df_plot['genero'].map(dicc_genero)
df_plot['principal_estresor'] = df_plot['principal_estresor'].map(dicc_estresor)
df_plot['calidad_sueno'] = df_plot['calidad_sueno'].map(dicc_sueno)
df_plot['nivel_estres'] = df_plot['nivel_estres'].map(dicc_nivel)
df_plot['carrera'] = df_plot['carrera'].map(dicc_carrera)
df_plot['situacion_laboral'] = df_plot['situacion_laboral'].map(dicc_laboral)

orden_estres = ["Ninguno", "Bajo", "Moderado", "Alto", "Muy alto"]
orden_presente = [cat for cat in orden_estres if cat in df_plot['nivel_estres'].unique()]


print("=============================================================================")
print(" FASE 3: GENERANDO Y GUARDANDO GRÁFICOS EDA EN ALTA RESOLUCIÓN")
print("=============================================================================\n")

# 1. Demográfico
plt.figure(figsize=(8, 5))
sns.histplot(data=df_plot, x='edad', hue='genero', multiple="stack", bins=10, kde=True, palette="Set2")
plt.title("Distribución Demográfica: Edad por Género")
plt.savefig(f"{carpeta_salida}/01_demografia.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. Causas
plt.figure(figsize=(10, 6))
sns.countplot(data=df_plot, y='principal_estresor', order=df_plot['principal_estresor'].value_counts().index, hue='principal_estresor', palette="flare", legend=False)
plt.title("Principales Causas de Estrés Universitario")
plt.savefig(f"{carpeta_salida}/02_causas_estres.png", dpi=300, bbox_inches='tight')
plt.close()

# 3. Sueño vs Estrés
plt.figure(figsize=(10, 6))
sns.heatmap(pd.crosstab(df_plot['calidad_sueno'], df_plot['nivel_estres']), annot=True, cmap="YlGnBu", fmt="d")
plt.title("Relación entre Calidad de Sueño y Nivel de Estrés")
plt.savefig(f"{carpeta_salida}/03_sueno_vs_estres.png", dpi=300, bbox_inches='tight')
plt.close()

# 4. BPM vs Estrés
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_plot, x='nivel_estres', y='bpm_manual', order=orden_presente, hue='nivel_estres', palette="coolwarm", legend=False)
plt.title("Fisiología del Estrés: BPM Agrupados por Nivel")
plt.savefig(f"{carpeta_salida}/04_fisiologia_bpm.png", dpi=300, bbox_inches='tight')
plt.close()

# 5. Carreras
plt.figure(figsize=(12, 6))
sns.countplot(data=df_plot, x='carrera', hue='nivel_estres', palette="Set3", hue_order=orden_presente)
plt.xticks(rotation=45, ha='right')
plt.savefig(f"{carpeta_salida}/05_estres_por_carrera.png", dpi=300, bbox_inches='tight')
plt.close()

# 6. Situación Laboral
plt.figure(figsize=(12, 6))
sns.countplot(data=df_plot, y='situacion_laboral', hue='nivel_estres', palette="pastel", hue_order=orden_presente)
plt.title("Impacto de la Carga Laboral en el Estrés Estudiantil")
plt.savefig(f"{carpeta_salida}/06_situacion_laboral.png", dpi=300, bbox_inches='tight')
plt.close()

# 7. Hábitos
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_plot, x='sueno', y='tareas_pendientes', hue='nivel_estres', hue_order=orden_presente, palette="Reds", s=100)
plt.title("Hábitos: Horas de Sueño vs. Tareas Pendientes")
plt.savefig(f"{carpeta_salida}/07_habitos_dispersion.png", dpi=300, bbox_inches='tight')
plt.close()

# 8. Correlación Matemática (Solucionado text error con numeric_only=True)
plt.figure(figsize=(8, 8))
correlaciones = df_clean.corr(method='spearman', numeric_only=True)[['nivel_estres']].sort_values(by='nivel_estres', ascending=False)
correlaciones = correlaciones.drop('nivel_estres')
top_corr = correlaciones.reindex(correlaciones['nivel_estres'].abs().sort_values(ascending=False).index).head(10)
sns.heatmap(top_corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
plt.title("Top 10 Variables Matemáticamente Correlacionadas")
plt.savefig(f"{carpeta_salida}/08_correlacion_matematica.png", dpi=300, bbox_inches='tight')
plt.close()
print("-> Gráficos 01 al 08 generados correctamente en la carpeta.\n")


print("=============================================================================")
print(" FASE 4: MACHINE LEARNING - EVALUACIÓN Y REPORTES EN CONSOLA")
print("=============================================================================\n")

# Variable Binaria (0: Bajo/Normal, 1: Alto/Muy Alto)
y = np.where(df_clean['nivel_estres'] <= 2, 0, 1)
X_raw = df_clean.drop(columns=['nivel_estres'])

# Preprocesamiento
X_encoded = pd.get_dummies(X_raw, drop_first=True)
num_cols_ml = X_raw.select_dtypes(include=[np.number]).columns
scaler = StandardScaler()
X_encoded[num_cols_ml] = scaler.fit_transform(X_encoded[num_cols_ml])

# Split & Entrenar
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42, stratify=y)

modelo = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, class_weight='balanced', random_state=42)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

# --- IMPRESIÓN EN CONSOLA ---
print("--- RENDIMIENTO DEL MODELO (SET DE PRUEBA) ---")
print(classification_report(y_test, y_pred, zero_division=0))

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(modelo, X_encoded, y, cv=cv, scoring='accuracy')

print("--- EVALUACIÓN ROBUSTA (VALIDACIÓN CRUZADA K-FOLD) ---")
print(f"Puntajes: {cv_scores}")
print(f"-> Accuracy Real Promedio: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})\n")

# --- GRÁFICA 9: FEATURE IMPORTANCE ---
importancias = modelo.feature_importances_
pesos_df = pd.DataFrame({'Caracteristica': X_encoded.columns, 'Peso': importancias}).sort_values(by='Peso', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=pesos_df.head(10), x='Peso', y='Caracteristica', hue='Caracteristica', palette='magma', legend=False)
plt.title("Top 10 Características Predictivas (Random Forest)")
plt.xlabel("Importancia Relativa")
plt.ylabel("Atributo")
plt.savefig(f"{carpeta_salida}/09_importancia_predictores.png", dpi=300, bbox_inches='tight')
plt.close()

print("-> Generado: 09_importancia_predictores.png")
print("\n=== PIPELINE DE DATOS Y ML COMPLETADO EXITOSAMENTE ===")

print("=============================================================================")
print(" FASE 5: SELECCIÓN DE CARACTERÍSTICAS Y MODELO ULTRA-REDUCIDO")
print("=============================================================================\n")

# 1. Calcular la separación estadística de todas las variables (ANOVA F-value)
# Evaluamos linealmente qué tanto separa cada columna a las clases de estrés
selector = SelectKBest(score_func=f_classif, k='all')
selector.fit(X_train, y_train)

# Crear DataFrame con los scores de separación
scores_df = pd.DataFrame({
    'Caracteristica': X_train.columns,
    'Score_Separacion': selector.scores_
}).dropna().sort_values(by='Score_Separacion', ascending=False)

# 2. Resaltar y graficar las variables con mayor separación
plt.figure(figsize=(10, 6))
top_k = 5 # Seleccionamos las 5 mejores columnas
# Lógica de colores: Las top 5 en rojo (resaltadas), el resto en gris
colores = ['crimson' if i < top_k else 'lightgray' for i in range(len(scores_df.head(15)))]

sns.barplot(data=scores_df.head(15), x='Score_Separacion', y='Caracteristica', palette=colores, hue='Caracteristica', legend=False)
plt.title("Nivel de Separación de las Variables vs Estrés (ANOVA F-Score)")
plt.xlabel("Score de Separación (Mayor es mejor)")
plt.ylabel("Atributo Fisiológico / Conductual")
plt.savefig(f"{carpeta_salida}/10_separacion_variables.png", dpi=300, bbox_inches='tight')
plt.close()
print("-> Generado: 10_separacion_variables.png")

# 3. Extraer exclusivamente las variables ganadoras
columnas_top = scores_df.head(top_k)['Caracteristica'].tolist()
print(f"\n-> Entrenando nuevo modelo EXCLUSIVAMENTE con estas {top_k} columnas:")
for col in columnas_top:
    print(f"   - {col}")

# Filtramos los datasets para que solo tengan esas columnas
X_train_opt = X_train[columnas_top]
X_test_opt = X_test[columnas_top]
X_encoded_opt = X_encoded[columnas_top] # Para la validación cruzada completa

# 4. Entrenar el nuevo modelo
modelo_reducido = RandomForestClassifier(
    n_estimators=100, 
    max_depth=4,            # Menor profundidad ya que tiene menos variables 
    min_samples_split=4,
    class_weight='balanced', 
    random_state=42
)
modelo_reducido.fit(X_train_opt, y_train)
y_pred_opt = modelo_reducido.predict(X_test_opt)

# 5. Evaluación del Nuevo Modelo
print("\n--- RENDIMIENTO DEL MODELO ULTRA-REDUCIDO (SET DE PRUEBA) ---")
print(classification_report(y_test, y_pred_opt, zero_division=0))

cv_opt = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores_opt = cross_val_score(modelo_reducido, X_encoded_opt, y, cv=cv_opt, scoring='accuracy')

print("--- EVALUACIÓN ROBUSTA (VALIDACIÓN CRUZADA K-FOLD) ---")
print(f"Puntajes: {cv_scores_opt}")
print(f"-> Accuracy Real Promedio (Modelo Reducido): {cv_scores_opt.mean():.4f} (+/- {cv_scores_opt.std():.4f})\n")

print("=== FASE 5 COMPLETADA EXITOSAMENTE ===")

# 6. Gráfica Final: Resultados del Modelo Ultra-Reducido (Matriz de Confusión)
# Calculamos la matriz comparando las respuestas reales (y_test) vs las predicciones (y_pred_opt)
cm = confusion_matrix(y_test, y_pred_opt)

plt.figure(figsize=(7, 5))
# Creamos un mapa de calor para que sea visualmente claro
sns.heatmap(
    cm, 
    annot=True, 
    fmt='d', 
    cmap='Blues', 
    cbar=False,
    annot_kws={"size": 16}, # Números más grandes para mayor claridad
    xticklabels=['Bajo / Normal', 'Alto / Muy Alto'],
    yticklabels=['Bajo / Normal', 'Alto / Muy Alto']
)

plt.title("Resultados del Modelo Reducido: Matriz de Confusión", fontsize=14, pad=15)
plt.xlabel("Predicción del Modelo", fontsize=12, fontweight='bold')
plt.ylabel("Estrés Real del Estudiante", fontsize=12, fontweight='bold')
plt.savefig(f"{carpeta_salida}/11_matriz_confusion_reducido.png", dpi=300, bbox_inches='tight')
plt.close()

print("-> Generado: 11_matriz_confusion_reducido.png")
print("\n=== PROYECTO COMPLETADO AL 100% ===")