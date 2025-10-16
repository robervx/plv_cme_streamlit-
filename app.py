import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from sql_connector import get_engine

st.set_page_config(page_title="CME-PLV", page_icon="🚔", layout="wide")

st.markdown("# 🚔 Cuadro de Mando Estratégico – PLV")
st.caption("Analítico mensual · Operativo tiempo real · Organizativo · Estratégico")

# --- Data access helpers
def load_intervenciones_local():
    path = os.path.join("data", "intervenciones_2025.xlsx")
    if os.path.exists(path):
        try:
            df = pd.read_excel(path)
            # Try to normalize column names
            cols = {c: c.strip().lower().replace(" ", "_") for c in df.columns}
            df = df.rename(columns=cols)
            # Expected columns for demo: mes_inicio / total_intervenciones / total_actas / total_denuncias / distrito / unidad / tipo
            # If the file is simple (e.g., Month + Total), adapt on the fly
            if "mes_inicio" not in df.columns:
                # Try to infer a date column
                for c in df.columns:
                    if "mes" in c.lower():
                        df["mes_inicio"] = pd.to_datetime(df[c], errors="coerce")
                        break
            if "total_intervenciones" not in df.columns:
                # If a single "total" column exists, rename it
                for c in df.columns:
                    if "total" in c.lower():
                        df = df.rename(columns={c: "total_intervenciones"})
                        break
            return df
        except Exception as e:
            st.warning(f"No se pudo leer el Excel local: {e}")
    return pd.DataFrame()

def query_sql(sql):
    engine = get_engine()
    if engine is None:
        return None
    return pd.read_sql(sql, engine)

# Sidebar filters
with st.sidebar:
    st.header("Filtros")
    year = st.selectbox("Año", [2025, 2024, 2023], index=0)
    distrito = st.text_input("Distrito (contiene)", "")
    unidad = st.text_input("Unidad (contiene)", "")

tab_analitica, tab_operativa, tab_organizativa, tab_estrategica = st.tabs([
    "📊 Analítica (mensual)",
    "🛰️ Operativa (tiempo real)",
    "🏛️ Organizativa",
    "🎯 Estratégica"
])

# ----------------- Analítica (mensual) -----------------
with tab_analitica:
    st.subheader("Evolución mensual y carga operativa")
    st.caption("KPIs: Intervenciones totales, variación mensual, promedio diario, % con acta/denuncia, ratio intervención/agente, tiempos medios.")

    # Try SQL first (example) else local Excel
    sql_demo = f"""
    SELECT TOP 2000 *
    FROM bi.vw_intervenciones_mensual
    WHERE YEAR(mes_inicio) = {year}
    ORDER BY mes_inicio
    """
    df = query_sql(sql_demo)
    if df is None or df.empty:
        df = load_intervenciones_local()

    if df.empty:
        st.info("Sube datos a 'data/intervenciones_2025.xlsx' o configura .env para SQL Server.")
    else:
        # Basic filtering
        if "distrito" in df.columns and distrito:
            df = df[df["distrito"].astype(str).str.contains(distrito, case=False, na=False)]
        if "unidad" in df.columns and unidad:
            df = df[df["unidad"].astype(str).str.contains(unidad, case=False, na=False)]

        # Derive monthly totals
        if "mes_inicio" in df.columns:
            df["mes_inicio"] = pd.to_datetime(df["mes_inicio"], errors="coerce")
        group_cols = ["mes_inicio"]
        total_col = "total_intervenciones" if "total_intervenciones" in df.columns else df.select_dtypes(include="number").columns[0]
        monthly = df.groupby(group_cols)[total_col].sum().reset_index().sort_values("mes_inicio")

        # KPI row
        col1, col2, col3, col4 = st.columns(4)
        total = monthly[total_col].sum()
        col1.metric("Intervenciones (YTD)", f"{total:,.0f}")
        if len(monthly) >= 2:
            mom = (monthly[total_col].iloc[-1] - monthly[total_col].iloc[-2]) / max(monthly[total_col].iloc[-2], 1)
            col2.metric("Variación mensual", f"{mom*100:,.1f}%")
        else:
            col2.metric("Variación mensual", "—")
        prom_dia = monthly[total_col].mean() / 30.0
        col3.metric("Promedio diario (aprox.)", f"{prom_dia:,.1f}")
        col4.metric("Meses analizados", str(monthly.shape[0]))

        fig = px.line(monthly, x="mes_inicio", y=total_col, markers=True, title="Intervenciones por mes")
        fig.update_layout(margin=dict(l=0,r=0,b=0,t=40))
        st.plotly_chart(fig, use_container_width=True)

        # If there are categorical breakdowns
        if "distrito" in df.columns:
            by_district = df.groupby(["distrito"])[total_col].sum().reset_index().sort_values(total_col, ascending=False)
            st.markdown("**Intervenciones por distrito (YTD)**")
            fig2 = px.bar(by_district, x=total_col, y="distrito", orientation="h")
            st.plotly_chart(fig2, use_container_width=True)

        if "tipo" in df.columns:
            by_tipo = df.groupby(["tipo"])[total_col].sum().reset_index().sort_values(total_col, ascending=False)
            st.markdown("**Intervenciones por tipo (YTD)**")
            fig3 = px.bar(by_tipo, x="tipo", y=total_col)
            st.plotly_chart(fig3, use_container_width=True)

# ----------------- Operativa (tiempo real) -----------------
with tab_operativa:
    st.subheader("Situación actual (placeholder)")
    st.caption("KPIs: Intervenciones activas, unidades en servicio, % cobertura, T. medio de respuesta (24h), mapa calor incidencias.")
    st.info("Esta pestaña está preparada para conectarse a datos en vivo (Grafana o SQL con refresco). De momento muestra widgets de ejemplo.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Intervenciones activas", "—")
    c2.metric("Unidades en servicio", "—")
    c3.metric("% Cobertura operativa", "—")
    c4.metric("T. medio respuesta (24h)", "—")
    st.write("🔧 Integra aquí una consulta SQL de las últimas 24–48h o un iframe de Grafana.")

# ----------------- Organizativa -----------------
with tab_organizativa:
    st.subheader("Personas, procesos e innovación")
    st.caption("KPIs: Plantilla total, % efectivos operativos, formación, propuestas, proyectos de innovación.")
    st.info("Carga aquí tus tablas RRHH y de innovación; por defecto no hay datos locales.")
    st.write("🔧 Enlaza vistas como bi.vw_rrhh_mensual y una tabla de propuestas/proyectos para gráficos.")

# ----------------- Estratégica -----------------
with tab_estrategica:
    st.subheader("Balanced Scorecard – Visión estratégica")
    st.caption("KPIs: Satisfacción ciudadana, incidentes graves/1000 hab., cumplimiento campañas, tiempo tramitación, % KPIs en verde, formación, innovación.")
    st.write("""
- **Índice Global de Eficiencia Policial (IGEP)** – promedio ponderado de:
  - Eficiencia operativa (analítica)
  - Saturación operativa (operativa)
  - Desarrollo organizativo (organizativa)
  - % KPIs estratégicos cumplidos
  
🔧 Cuando estén disponibles, conecta aquí los KPIs consolidados trimestrales/anuales.
""")
