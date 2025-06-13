import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="Dashboard de Ventas Pro", layout="wide")
st.title("🚀 Dashboard Avanzado de Ventas")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel de ventas", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=0)
    df.columns = df.columns.map(str).str.strip()

    col_map = {
        "Monto": "Ventas",
        "Costo": "Costos",
        "Utilidad": "Utilidad",
        "Rentabilidad": "Rentabilidad",
        "Fecha": "Fecha",
        "Vendedor": "Vendedor",
        "Descripción": "Descripción",
        "Marca": "Marca",
        "Línea": "Línea",
        "Canal": "Canal",
    }
    df.rename(columns=col_map, inplace=True)

    for col in ["Ventas", "Costos", "Utilidad", "Rentabilidad"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "Fecha" in df.columns:
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

    df_filtrado = df.copy()
    st.markdown("---")
    st.subheader("🎯 Filtros Avanzados")
    col1, col2, col3 = st.columns(3)
    with col1:
        # === Filtro de Vendedor con COMBO ===
        vendedores_map = {
            "C03 - RA HERNANDEZ": "C03",
            "C46 - V ORTEGA": "C46",
            "C51 - P NUÑEZ": "C51",
            "C67 - W MOREL": "C67",
            "C69 - W. BERIHUETE": "C69",
            "C73 - G. NUÑEZ": "C73",
            "JYA - J. YAN": "JYA",
            "MCJ - M.CAPELLAN": "MCJ",
            "K93 - V. PEREZ UREÑA": "K93",
            "R37 - P FERREIRA": "R37",
            "R53 - M GONZALEZ": "R53",
            "C77 - D.MONTILLA": "C77",
            "MBR - M BRITO": "MBR",
            "JJE - J. JEREZ": "JJE",
            "JDE - J.DE JESUS": "JDE",
            "S03 - R ALVINO": "S03",
            "S07 - J RAFAEL": "S07",
            "S19 - W ANTONIO": "S19",
            "MAB - M ABREU": "MAB",
            "C06 - VENTAS CASA": "C06",
            "S03 - R ALBINO": "S03",
            "AVE - A.VENTURAS": "AVE",
            "K73 - AIDA TEJADA R.": "K73",
            "K83 - J. DAJER": "K83",
            "C62 - A RAMIREZ": "C62",
            "S07 - J RAFAEL": "S07",
        }
        vendedor_combo = st.multiselect("Vendedor", list(vendedores_map.keys()))
        vendedores = [vendedores_map[v] for v in vendedor_combo]
        marcas = st.multiselect("Marca", df["Marca"].dropna().unique() if "Marca" in df.columns else [])
    with col2:
        fecha_rango = st.date_input("Rango de Fecha", [])
        rango_rent = st.slider("Filtrar Rentabilidad (%)", -1.0, 2.0, (-1.0, 2.0)) if "Rentabilidad" in df.columns else None
    with col3:

        buscar_desc = st.text_input("Buscar por Descripción")
        lineas = st.multiselect("Línea", df["Línea"].dropna().unique() if "Línea" in df.columns else [])

    df_filtrado = df.copy()
    if vendedores:
        df_filtrado = df_filtrado[df_filtrado["Vendedor"].isin(vendedores)]
    if marcas:
        df_filtrado = df_filtrado[df_filtrado["Marca"].isin(marcas)]
    if lineas:
        df_filtrado = df_filtrado[df_filtrado["Línea"].isin(lineas)]
    
    canales = st.multiselect("Selecciona Canal", df["Canal"].dropna().unique() if "Canal" in df.columns else [], key="canal_widget_final")
    if canales:
        df_filtrado = df_filtrado[df_filtrado["Canal"].isin(canales)]

    if canales:
        df_filtrado = df_filtrado[df_filtrado["Canal"].isin(canales)]
    if canales:
        df_filtrado = df_filtrado[df_filtrado["Canal"].isin(canales)]
    if fecha_rango and len(fecha_rango) == 2:
        start_dt = pd.to_datetime(datetime.datetime.combine(fecha_rango[0], datetime.time.min))
        end_dt = pd.to_datetime(datetime.datetime.combine(fecha_rango[1], datetime.time.max))
        df_filtrado = df_filtrado[df_filtrado["Fecha"].between(start_dt, end_dt)]
    if rango_rent:
        df_filtrado = df_filtrado[(df_filtrado["Rentabilidad"] >= rango_rent[0]) & (df_filtrado["Rentabilidad"] <= rango_rent[1])]
    if buscar_desc and "Descripción" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["Descripción"].str.contains(buscar_desc, case=False, na=False)]

    # KPIs después de aplicar los filtros
    st.markdown("---")
    st.subheader("📌 Indicadores Generales")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Total Ventas", f"RD${df_filtrado['Ventas'].sum():,.2f}" if "Ventas" in df_filtrado.columns else "N/A")
    with col2:
        st.metric("💸 Total Costos", f"RD${df_filtrado['Costos'].sum():,.2f}" if "Costos" in df_filtrado.columns else "N/A")
    with col3:
        st.metric("📈 Total Utilidad", f"RD${df_filtrado['Utilidad'].sum():,.2f}" if "Utilidad" in df_filtrado.columns else "N/A")
    with col4:
        rent = df_filtrado["Rentabilidad"].mean() if "Rentabilidad" in df_filtrado.columns else 0
        st.metric("📊 Rentabilidad Promedio", f"{rent:.2%}")

    st.markdown("---")
    st.subheader("📊 Análisis Gráfico")

    if "Canal" in df_filtrado.columns and "Ventas" in df_filtrado.columns:
        resumen_canal = df_filtrado.groupby("Canal")["Ventas"].sum().reset_index()
        
        canal_data = df_filtrado.groupby("Canal")["Ventas"].sum().reset_index()
        fig_canal = px.bar(canal_data, x="Canal", y="Ventas", title="Ventas por Canal", text_auto=True)

        st.plotly_chart(fig_canal, use_container_width=True, key="canal_chart")


        if "Vendedor" in df_filtrado.columns and "Ventas" in df_filtrado.columns:
            resumen = df_filtrado.groupby("Vendedor")["Ventas"].sum().reset_index()
            fig = px.bar(resumen, x="Vendedor", y="Ventas", color="Vendedor", title="Ventas por Vendedor")
            st.plotly_chart(fig, use_container_width=True)

        if "Fecha" in df_filtrado.columns:
            resumen_fecha = df_filtrado.groupby("Fecha")["Ventas"].sum().reset_index()
            fig_fecha = px.line(resumen_fecha, x="Fecha", y="Ventas", title="Ventas por Fecha")
            st.plotly_chart(fig_fecha, use_container_width=True)

        if "Descripción" in df_filtrado.columns and "Rentabilidad" in df_filtrado.columns:
            resumen_tipo = df_filtrado.groupby("Descripción")["Rentabilidad"].mean().reset_index().sort_values(by="Rentabilidad", ascending=False).head(20)
            fig_tipo = px.bar(resumen_tipo, x="Descripción", y="Rentabilidad", color="Descripción", title="Top 20 Rentabilidad por Artículo")
            st.plotly_chart(fig_tipo, use_container_width=True)

        if "Utilidad" in df_filtrado.columns and "Rentabilidad" in df_filtrado.columns:
            fig_disp = px.scatter(df_filtrado, x="Utilidad", y="Rentabilidad", color="Vendedor", title="Utilidad vs Rentabilidad")
            st.plotly_chart(fig_disp, use_container_width=True)

        if "Fecha" in df_filtrado.columns:
            df_filtrado["Mes"] = df_filtrado["Fecha"].dt.to_period("M").astype(str)
            resumen_mes = df_filtrado.groupby("Mes")["Ventas"].sum().reset_index()
            fig_mes = px.area(resumen_mes, x="Mes", y="Ventas", title="Ventas por Mes")
            st.plotly_chart(fig_mes, use_container_width=True)

        st.markdown("---")
        st.subheader("🏆 Rankings")
        if "Descripción" in df_filtrado.columns and "Ventas" in df_filtrado.columns:
            top_prod = df_filtrado.groupby("Descripción")["Ventas"].sum().sort_values(ascending=False).head(10)
            st.dataframe(top_prod.reset_index().rename(columns={"Ventas": "Total Ventas"}))

        if "Vendedor" in df_filtrado.columns and "Rentabilidad" in df_filtrado.columns:
            top_vend = df_filtrado.groupby("Vendedor")["Rentabilidad"].mean().sort_values(ascending=False).head(5)
            st.dataframe(top_vend.reset_index().rename(columns={"Rentabilidad": "Rentabilidad Promedio"}))

        st.markdown("---")
        st.subheader("📋 Tabla Dinámica")
        if "Vendedor" in df_filtrado.columns and "Fecha" in df_filtrado.columns:
            pivote = pd.pivot_table(df_filtrado, index="Vendedor", columns=df_filtrado["Fecha"].dt.month, values="Ventas", aggfunc="sum", fill_value=0)
            st.dataframe(pivote, use_container_width=True)

        st.markdown("---")
        st.subheader("📥 Descarga del Resultado")
        st.dataframe(df_filtrado, use_container_width=True, height=500)
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV filtrado", csv, file_name="ventas_limpias_pro.csv", mime="text/csv")

        # --- Gráficos y análisis ---