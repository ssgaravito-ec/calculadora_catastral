import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Control Reconocimiento Predial",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    color: #e8edf4;
}
.stApp {
    background: #080f1a;
}

/* Header */
.main-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #ffffff;
    margin-bottom: 0;
}
.main-title span { color: #00c8ff; }
.subtitle {
    font-size: 0.85rem;
    color: #4a6a85;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Alerta */
.alert-danger {
    background: linear-gradient(135deg, #2a0a0a, #1a0505);
    border: 1px solid #ff3333;
    border-left: 4px solid #ff3333;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #ffaaaa;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.alert-success {
    background: linear-gradient(135deg, #0a2a15, #051a0d);
    border: 1px solid #00e57a;
    border-left: 4px solid #00e57a;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #80ffbb;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* Metric cards */
.kpi-card {
    background: #0d1b2a;
    border: 1px solid #1a3050;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-blue::after  { background: #00c8ff; }
.kpi-green::after { background: #00e57a; }
.kpi-red::after   { background: #ff4466; }
.kpi-yellow::after{ background: #ffc400; }

.kpi-label {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #4a6a85;
    margin-bottom: 0.4rem;
}
.kpi-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #4a6a85;
    margin-top: 0.3rem;
}

/* Divider */
.div-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1a3050, #00c8ff33, #1a3050, transparent);
    margin: 1.5rem 0;
}

/* Section title */
.sec-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00c8ff;
    margin-bottom: 0.8rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #060d18;
    border-right: 1px solid #1a3050;
}
.sidebar-head {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #00c8ff;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    border-bottom: 1px solid #1a3050;
    padding-bottom: 0.6rem;
    margin-bottom: 1rem;
}

/* Data editor overrides */
.stDataFrame, [data-testid="stDataEditor"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #1a3050 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-head">⚙ Parámetros</div>', unsafe_allow_html=True)

    volumen_total = st.number_input(
        "Volumen Total de Predios",
        min_value=100, max_value=999_999,
        value=5000, step=100,
    )
    funcionarios = st.slider("Funcionarios", 1, 50, 4)
    rendimiento  = st.slider("Rendimiento (predios/func/día)", 1, 30, 7)
    dias_habiles = st.number_input("Días hábiles / mes", 15, 26, 22)

    st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-head">📅 Periodo</div>', unsafe_allow_html=True)

    meta_mes = st.selectbox(
        "Mes límite de la meta",
        ["Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto"],
        index=5,  # Julio por defecto
    )

    st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
    st.caption("Sistema de Control Predial · v3.0")


# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
MESES = ["Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto"]
capacidad_mes = funcionarios * rendimiento * dias_habiles
idx_meta = MESES.index(meta_mes)          # índice del mes límite (0-based)
meses_activos = idx_meta + 1              # cuántos meses para llegar a la meta

# Distribución programada: equitativa hasta el mes límite, 0 después
predios_por_mes_prog = volumen_total / meses_activos if meses_activos > 0 else 0
programado = [
    round(predios_por_mes_prog) if i <= idx_meta else 0
    for i in range(len(MESES))
]
# Ajuste para que la suma sea exactamente el volumen_total
diff = volumen_total - sum(programado[:meses_activos])
if meses_activos > 0:
    programado[idx_meta] += diff

capacidad_total_periodo = capacidad_mes * meses_activos
insuficiente = capacidad_total_periodo < volumen_total


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">Control de <span>Reconocimiento Predial</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Matriz de Seguimiento Operativo · Febrero – Agosto</div>', unsafe_allow_html=True)

# Alerta de insuficiencia
if insuficiente:
    deficit = volumen_total - capacidad_total_periodo
    st.markdown(f"""
    <div class="alert-danger">
        ⚠️ <strong>INSUFICIENCIA DE PERSONAL:</strong> Con {funcionarios} funcionarios a {rendimiento} pred/día,
        la capacidad total ({capacidad_total_periodo:,} predios) no alcanza la meta de {volumen_total:,} predios
        en {meses_activos} meses. <strong>Déficit de {deficit:,} predios.</strong>
        Necesitas al menos <strong>{int(np.ceil(volumen_total / (rendimiento * dias_habiles * meses_activos)))} funcionarios</strong>.
    </div>
    """, unsafe_allow_html=True)
else:
    sobrante = capacidad_total_periodo - volumen_total
    st.markdown(f"""
    <div class="alert-success">
        ✅ <strong>PLAN VIABLE:</strong> Capacidad instalada ({capacidad_total_periodo:,} predios)
        supera la meta de {volumen_total:,}. Margen de {sobrante:,} predios.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MATRIZ EDITABLE
# ─────────────────────────────────────────────
st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">📋 Matriz de Control — Reconocimiento Predial</div>', unsafe_allow_html=True)
st.caption("✏️ Edita los valores en la fila **'Real'** con los datos ejecutados cada mes.")

# Construir DataFrame editable
df_matrix = pd.DataFrame(
    {
        "Subfila": ["🟦 Programado", "✏️ Real", "📊 Balance"],
        **{mes: [programado[i], 0, 0] for i, mes in enumerate(MESES)},
    }
).set_index("Subfila")

# Solo la fila "Real" es editable
col_config = {mes: st.column_config.NumberColumn(mes, min_value=0, step=1) for mes in MESES}

edited = st.data_editor(
    df_matrix.loc[["🟦 Programado", "✏️ Real"]],
    column_config=col_config,
    disabled=["🟦 Programado"],   # solo editable la fila Real
    use_container_width=True,
    key="matriz_editor",
)

# Recalcular balance
real_vals  = [int(edited.loc["✏️ Real", mes])   for mes in MESES]
prog_vals  = [int(edited.loc["🟦 Programado", mes]) for mes in MESES]
balance    = [r - p for r, p in zip(real_vals, prog_vals)]

# Mostrar fila de balance con colores
balance_html = "<table style='width:100%;border-collapse:collapse;font-family:Barlow,sans-serif;font-size:0.85rem;'>"
balance_html += "<tr style='background:#0d1b2a;'>"
balance_html += "<td style='padding:8px 12px;color:#4a6a85;font-weight:600;border:1px solid #1a3050;'>📊 Balance</td>"
for b in balance:
    color = "#00e57a" if b > 0 else "#ff4466" if b < 0 else "#4a6a85"
    sign  = "+" if b > 0 else ""
    balance_html += f"<td style='padding:8px 12px;text-align:right;color:{color};font-weight:700;border:1px solid #1a3050;'>{sign}{b:,}</td>"
balance_html += "</tr></table>"
st.markdown(balance_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────
st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">🎯 KPIs Acumulados</div>', unsafe_allow_html=True)

total_prog = sum(prog_vals)
total_real = sum(real_vals)
total_bal  = total_real - total_prog
avance_pct = (total_real / volumen_total * 100) if volumen_total > 0 else 0
faltan     = volumen_total - total_real

c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    (c1, "kpi-blue",   "Meta Total",           f"{volumen_total:,}",  f"Predios a reconocer"),
    (c2, "kpi-blue",   "Total Programado",      f"{total_prog:,}",     f"Según plan"),
    (c3, "kpi-green",  "Total Ejecutado",        f"{total_real:,}",     f"{avance_pct:.1f}% de la meta"),
    (c4, "kpi-red" if total_bal < 0 else "kpi-green",
                       "Balance Acumulado",
                       f"{'+'if total_bal>=0 else ''}{total_bal:,}",
                       "Superávit" if total_bal >= 0 else "Déficit"),
    (c5, "kpi-yellow", "Predios Restantes",     f"{max(faltan,0):,}",  f"Para completar meta"),
]
for col, cls, lbl, val, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GRÁFICO COMPARATIVO
# ─────────────────────────────────────────────
st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">📈 Curva de Avance — Programado vs. Real</div>', unsafe_allow_html=True)

# Curvas acumuladas
prog_acum = list(np.cumsum(prog_vals))
real_acum = list(np.cumsum(real_vals))
meta_line = [volumen_total] * len(MESES)

df_chart = pd.DataFrame({
    "Programado (acum.)": prog_acum,
    "Real (acum.)":       real_acum,
    "Meta":               meta_line,
}, index=MESES)

st.line_chart(df_chart, use_container_width=True, height=320)

# Gráfico mensual (barras)
st.markdown('<div class="sec-title" style="margin-top:1.2rem;">📊 Ejecución Mensual</div>', unsafe_allow_html=True)
df_bar = pd.DataFrame({
    "Programado": prog_vals,
    "Real":       real_vals,
}, index=MESES)
st.bar_chart(df_bar, use_container_width=True, height=260)


# ─────────────────────────────────────────────
# TABLA RESUMEN DETALLADA
# ─────────────────────────────────────────────
st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">📑 Resumen Detallado por Mes</div>', unsafe_allow_html=True)

df_resumen = pd.DataFrame({
    "Mes": MESES,
    "Programado": prog_vals,
    "Real": real_vals,
    "Balance": balance,
    "% Cumplimiento": [
        f"{(r/p*100):.1f}%" if p > 0 else "N/A"
        for r, p in zip(real_vals, prog_vals)
    ],
    "Prog. Acumulado": prog_acum,
    "Real Acumulado":  real_acum,
}).set_index("Mes")

def color_balance(val):
    try:
        v = int(str(val).replace("+","").replace(",",""))
        if v > 0:  return "color: #00e57a; font-weight:700"
        if v < 0:  return "color: #ff4466; font-weight:700"
    except: pass
    return "color: #4a6a85"

styled = (
    df_resumen.style
    .applymap(color_balance, subset=["Balance"])
    .format({
        "Programado": "{:,}",
        "Real": "{:,}",
        "Balance": "{:+,}",
        "Prog. Acumulado": "{:,}",
        "Real Acumulado": "{:,}",
    })
    .set_properties(**{"text-align": "right", "font-size": "13px"})
    .set_table_styles([
        {"selector": "thead th", "props": [
            ("background", "#0a1628"), ("color", "#00c8ff"),
            ("font-family", "Barlow Condensed, sans-serif"),
            ("letter-spacing", "0.1em"), ("text-transform", "uppercase"),
            ("padding", "10px 14px"), ("border-bottom", "2px solid #00c8ff44"),
        ]},
        {"selector": "tbody th", "props": [
            ("background", "#0d1b2a"), ("color", "#8aaac0"),
            ("padding", "8px 14px"), ("border-right", "2px solid #1a3050"),
        ]},
    ])
)
st.dataframe(styled, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#1a3050;font-size:0.7rem;
letter-spacing:0.2em;text-transform:uppercase;padding:2rem 0 0.5rem;">
Control Operativo Catastral · Reconocimiento Predial · 2025
</div>
""", unsafe_allow_html=True)
