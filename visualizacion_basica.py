import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

sns.set(style="whitegrid")

# ==========================
# CARGA Y PREPARACIÓN DE DATOS
# ==========================
df = pd.read_csv("data.csv")
df["Date"] = pd.to_datetime(df["Date"])

if "Time" in df.columns:
    try:
        df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    except:
        df["Hour"] = np.nan

# ==========================
# SIDEBAR DE FILTROS
# ==========================
st.sidebar.header("🎛️ Filtros")
branches = st.sidebar.multiselect("Sucursal (Branch)", df["Branch"].unique(), default=df["Branch"].unique())
lines = st.sidebar.multiselect("Línea de producto", df["Product line"].unique(), default=df["Product line"].unique())
customers = st.sidebar.multiselect("Tipo de cliente", df["Customer type"].unique(), default=df["Customer type"].unique())

df_filtered = df[
    (df["Branch"].isin(branches)) &
    (df["Product line"].isin(lines)) &
    (df["Customer type"].isin(customers))
]

# ==========================
# TÍTULO Y KPIs
# ==========================
st.title("📊 Dashboard Comercial Interactivo")

col1, col2, col3 = st.columns(3)
col1.metric("💵 Ventas totales", f"${df_filtered['Total'].sum():,.0f}")
col2.metric("📈 Ingreso bruto", f"${df_filtered['gross income'].sum():,.0f}")
col3.metric("⭐ Prom. calificación", f"{df_filtered['Rating'].mean():.2f} / 10")

# ==========================
# SECCIÓN 2: Visualización básica
# ==========================
st.header("2. Visualización básica de datos")

st.markdown("### a. Total de ventas por día")
ventas_dia = df_filtered.groupby("Date")["Total"].sum()
fig1, ax1 = plt.subplots(figsize=(10, 4))
ventas_dia.plot(ax=ax1, marker='o')
ax1.set_title("Total de ventas por día")
st.pyplot(fig1)

st.markdown("### b. Total vs. Ingreso bruto")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_filtered, x="Total", y="gross income", hue="Product line", ax=ax2)
ax2.set_title("Relación entre Total y Gross Income")
st.pyplot(fig2)

st.markdown("### c. Ingreso bruto por tipo de cliente")
fig3, ax3 = plt.subplots(figsize=(6, 5))
sns.boxplot(data=df_filtered, x="Customer type", y="gross income", ax=ax3)
ax3.set_title("Distribución de ingreso bruto por tipo de cliente")
st.pyplot(fig3)

# ==========================
# SECCIÓN 3: Gráficos compuestos
# ==========================
st.header("3. Gráficos compuestos y contextualización")

st.markdown("### a. Ventas por hora y método de pago")
fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df_filtered, x="Hour", y="Total", hue="Payment", estimator="sum", ci=None, ax=ax4)
ax4.set_title("Ventas por hora por método de pago")
st.pyplot(fig4)

st.markdown("### b. Ingreso bruto por tipo de cliente y género")
fig5, ax5 = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_filtered, x="Customer type", y="gross income", hue="Gender", ax=ax5)
ax5.set_title("Ingreso bruto por tipo de cliente y género")
st.pyplot(fig5)

st.markdown("### c. Ingreso promedio por línea y sucursal")
fig6, ax6 = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_filtered, x="Product line", y="gross income", hue="Branch", estimator=np.mean, ci=None, ax=ax6)
ax6.set_title("Ingreso promedio por línea y sucursal")
plt.xticks(rotation=45)
st.pyplot(fig6)

# ==========================
# SECCIÓN 4: Visualización multivariada
# ==========================
st.header("4. Visualización multivariada")

st.markdown("### a. Matriz de correlación")
numeric_cols = ["Total", "gross income", "cogs", "Rating", "Unit price", "Quantity", "Hour"]
corr = df_filtered[numeric_cols].corr()
fig7, ax7 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax7)
st.pyplot(fig7)

st.markdown("### b. Pairplot entre variables clave")
selected = ["Total", "gross income", "cogs", "Rating"]
fig8 = sns.pairplot(df_filtered[selected])
st.pyplot(fig8)

# ==========================
# SECCIÓN 5: Visualización 3D
# ==========================
st.header("5. Visualización 3D")

st.markdown("### Relación entre Total, Gross Income y Rating")
fig9 = plt.figure(figsize=(10, 6))
ax9 = fig9.add_subplot(111, projection='3d')
ax9.scatter(df_filtered["Total"], df_filtered["gross income"], df_filtered["Rating"],
            c=df_filtered["Rating"], cmap='viridis', s=50)
ax9.set_xlabel("Total")
ax9.set_ylabel("Gross Income")
ax9.set_zlabel("Rating")
ax9.set_title("Total vs Gross Income vs Rating")
st.pyplot(fig9)
