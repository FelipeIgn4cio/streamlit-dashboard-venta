import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cargar los datos
df = pd.read_csv("data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour

st.title("📊 Dashboard de Análisis de Ventas")

# SIDEBAR
st.sidebar.title("🔎 Filtros")
product_lines = st.sidebar.multiselect("Líneas de producto", df["Product line"].unique(), default=df["Product line"].unique())
branches = st.sidebar.multiselect("Sucursales", df["Branch"].unique(), default=df["Branch"].unique())

df_filtered = df[(df["Product line"].isin(product_lines)) & (df["Branch"].isin(branches))]

# 1. Ventas por día
st.header("1. Total de ventas por día")
ventas_dia = df_filtered.groupby("Date")["Total"].sum()
fig, ax = plt.subplots()
ventas_dia.plot(marker='o', ax=ax)
ax.set_title("Ventas por día")
ax.set_xlabel("Fecha")
ax.set_ylabel("Total")
st.pyplot(fig)

# 2. Dispersión Total vs Gross Income
st.header("2. Relación entre Total y Gross Income")
fig, ax = plt.subplots()
sns.scatterplot(data=df_filtered, x="Total", y="gross income", hue="Product line", ax=ax)
ax.set_title("Dispersión: Total vs. Ingreso Bruto")
st.pyplot(fig)

# 3. Boxplot ingreso bruto por cliente y género
st.header("3. Ingreso bruto por tipo de cliente y género")
fig, ax = plt.subplots()
sns.boxplot(data=df_filtered, x="Customer type", y="gross income", hue="Gender", ax=ax)
ax.set_title("Distribución por tipo de cliente y género")
st.pyplot(fig)

# 4. Línea: ventas por hora y método de pago
st.header("4. Ventas por hora del día y método de pago")
fig, ax = plt.subplots()
sns.lineplot(data=df_filtered, x="Hour", y="Total", hue="Payment", estimator="sum", ci=None, ax=ax)
ax.set_title("Total de ventas por hora")
st.pyplot(fig)

# 5. Barras: ingreso promedio por línea de producto y sucursal
st.header("5. Ingreso promedio por línea de producto según sucursal")
fig, ax = plt.subplots()
sns.barplot(data=df_filtered, x="Product line", y="gross income", hue="Branch", estimator=np.mean, ci=None, ax=ax)
ax.set_title("Ingreso promedio por línea y sucursal")
plt.xticks(rotation=45)
st.pyplot(fig)


