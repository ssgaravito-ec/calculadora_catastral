import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Capacidad Operativa Catastral",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

/* Fondo principal */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    color: #e8edf4;
}

/* Encabezado principal */
.main-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: linear-gradient(90deg, #00d4ff, #7b61ff, #00d4ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
    margin-bottom: 0.2rem;
}
@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.sub-header {
    font-size: 0.95rem;
    color: #6a8fa8;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Tarjetas de métricas personalizadas */
.metric-card {
    background: linear-gradient(145deg, #0e1f35, #162a42);
    border: 1px solid #1e3a55;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.metric-card.blue::before  { background: linear-gradient(90deg, #00d4ff, #0099bb); }
.metric-card.purple::before { background: linear-gradient(90deg, #7b61ff, #5040cc); }
.metric-card.green::before  { background: linear-gradient(90deg, #00e5a0, #00aa70); }
.metric-card.orange::before { background: linear-gradient(90deg, #ff9500, #cc6600); }

.metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6a8fa8;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #e8edf4;
    line-height: 1;
}
.metric-delta {
    font-size: 0.82rem;
    color: #00e5a0;
    margin-top: 0.4rem;
}
.metric-icon {
    position: absolute;
    top: 1.2rem; right: 1.4rem;
    font-size: 1.8rem;
    opacity: 0.25;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0d1b2a 100%);
    border-right: 1px solid #1e3a55;
}
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label {
    color: #a0bcd0 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Sección de título lateral */
.sidebar-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #00d4ff;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e3a55;
    margin-bottom: 1.2rem;
}

/* Divisor estilizado */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a55, #00d4ff33, #1e3a55, transparent);
    margin: 1.8rem 0;
}

/* Encabezado de sección */
.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #7b61ff;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Contenedor del dataframe */
.dataframe-container {
    background: #0d1b2a;
    border: 1px solid #1e3a55;
    border-radius: 12px;
    padding: 1rem;
}

/* Alerta de progreso */
.progress-bar-container {
    background: #0e1f35;
    border: 1px solid #1e3a55;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 1rem;
}
.progress-label {
    font-size: 0.75rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6a8fa8;
    margin-bottom: 0.6rem;
}
.progress-bar-track {
    background: #0a1628;
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #00d4ff, #7b61ff);
    transition: width 0.6s ease;
}
.progress-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #00d4ff;
    margin-top: 0.4rem;
}

/* Botón */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff22, #7b61ff22);
    border: 1px solid #7b61ff66;
    color: #c0d8f0;
    border-radius: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-size: 0.82rem;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00d4ff44, #7b61ff44);
    border-color: #7b61ff;
    color: #fff;
    box-shadow: 0 0 20px #7b61ff44;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR — PARÁMETROS DE ENTRADA
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙ Parámetros de Entrada</div>', unsafe_allow_html=True)

    volumen_total = st.number_input(
        "Volumen Total (Predios)",
        min_value=100, max_value=500_000,
        value=5000, step=100,
        help="Número total de predios a procesar",
    )

    funcionarios = st.slider(
        "Funcionarios Asignados",
        min_value=1, max_value=50,
        value=4,
        help="Cantidad de personal operativo",
    )

    rendimiento = st.slider(
        "Rendimiento (Predios/Funcionario/Día)",
        min_value=1, max_value=30,
        value=7,
        help="Capacidad individual diaria de cada funcionario",
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📅 Configuración</div>', unsafe_allow_html=True)

    dias_habiles = st.number_input(
        "Días Hábiles por Mes",
        min_value=15, max_value=26,
        value=22,
    )

    fecha_inicio = st.selectbox(
        "Mes de Inicio",
        ["Febrero", "Marzo", "Abril"],
        index=0,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.caption("Sistema de Planificación Catastral v2.0")


# ─────────────────────────────────────────────
# LÓGICA DE CÁLCULO
# ─────────────────────────────────────────────
predios_dia_total = funcionarios * rendimiento
dias_totales = volumen_total / predios_dia_total if predios_dia_total > 0 else 0
meses_totales = dias_totales / dias_habiles
predios_mes = predios_dia_total * dias_habiles
eficiencia_pct = min((predios_dia_total / max(volumen_total, 1)) * 100 * 22, 100)


# ─────────────────────────────────────────────
# ENCABEZADO PRINCIPAL
# ─────────────────────────────────────────────
st.markdown('<div class="main-header">Capacidad Operativa Catastral</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistema de Planificación y Matriz de Ejecución</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TARJETAS DE MÉTRICAS
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-icon">🗺️</div>
        <div class="metric-label">Volumen Total</div>
        <div class="metric-value">{volumen_total:,}</div>
        <div class="metric-delta">▸ Predios a procesar</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card purple">
        <div class="metric-icon">⚡</div>
        <div class="metric-label">Predios / Día</div>
        <div class="metric-value">{predios_dia_total:,}</div>
        <div class="metric-delta">▸ {funcionarios} func. × {rendimiento} pred./día</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-icon">📆</div>
        <div class="metric-label">Días Requeridos</div>
        <div class="metric-value">{dias_totales:.1f}</div>
        <div class="metric-delta">▸ {meses_totales:.1f} meses hábiles</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card orange">
        <div class="metric-icon">📊</div>
        <div class="metric-label">Predios / Mes</div>
        <div class="metric-value">{int(predios_mes):,}</div>
        <div class="metric-delta">▸ Base {dias_habiles} días hábiles</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# BARRA DE PROGRESO DE CAPACIDAD
# ─────────────────────────────────────────────
meses_disponibles = 7  # Feb–Ago
capacidad_total = predios_mes * meses_disponibles
cobertura_pct = min((capacidad_total / max(volumen_total, 1)) * 100, 150)
color_status = "#00e5a0" if cobertura_pct >= 100 else "#ff9500" if cobertura_pct >= 70 else "#ff4444"
status_txt = "✅ Plan viable" if cobertura_pct >= 100 else "⚠️ Capacidad limitada" if cobertura_pct >= 70 else "❌ Insuficiente"

c1, c2 = st.columns([3, 1])
with c1:
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-label">Cobertura del Plan (Feb – Ago) &nbsp;|&nbsp; {status_txt}</div>
        <div class="progress-bar-track">
            <div class="progress-bar-fill" style="width:{min(cobertura_pct,100):.1f}%; background: linear-gradient(90deg, #00d4ff, {color_status});"></div>
        </div>
        <div class="progress-value" style="color:{color_status};">{cobertura_pct:.1f}% &nbsp; — &nbsp; Capacidad instalada: {int(capacidad_total):,} predios en 7 meses</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    diferencia = capacidad_total - volumen_total
    signo = "+" if diferencia >= 0 else ""
    st.metric(
        label="Diferencia vs Meta",
        value=f"{signo}{int(diferencia):,}",
        delta=f"{'Superávit' if diferencia >= 0 else 'Déficit'} de predios",
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MATRIZ DE PLANIFICACIÓN
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Matriz de Planificación Operativa</div>', unsafe_allow_html=True)

MESES = ["Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto"]

ACTIVIDADES = [
    "Reconocimiento Predial",
    "Levantamiento Topográfico",
    "Verificación de Linderos",
    "Captura de Atributos Físicos",
    "Actualización Cartográfica",
    "Diagnóstico Socioeconómico",
    "Validación Documental",
    "Georreferenciación de Predios",
    "Inspección de Mejoras",
    "Clasificación del Suelo",
    "Revisión de Avalúos",
    "Notificación a Propietarios",
    "Resolución de Inconsistencias",
    "Actualización Base de Datos",
    "Control de Calidad Catastral",
    "Homologación de Información",
    "Generación de Informes",
    "Validación IGAC",
    "Cierre de Procesos",
    "Entrega y Certificación Final",
]

# Distribución de carga mensual (valores en predios)
np.random.seed(42)
total_meses = len(MESES)

# Distribuir el volumen de forma semi-aleatoria pero realista
pesos_base = np.array([0.10, 0.18, 0.20, 0.18, 0.14, 0.11, 0.09])
pesos_base = pesos_base / pesos_base.sum()

data = {}
for i, mes in enumerate(MESES):
    carga_mes = int(volumen_total * pesos_base[i])
    # Distribuir entre actividades según su fase
    pesos_act = np.random.dirichlet(np.ones(20) * 2)
    data[mes] = np.round(pesos_act * carga_mes).astype(int)

df = pd.DataFrame(data, index=ACTIVIDADES)
df.index.name = "Actividad / Proceso"

# Asegurar que los totales sean coherentes
for mes in MESES:
    df[mes] = df[mes].clip(lower=0)

# Aplicar estilo heatmap con colores personalizados
def style_heatmap(val):
    if val == 0:
        return "background-color: #0a1628; color: #2a4060;"
    max_val = df.values.max()
    ratio = val / max_val if max_val > 0 else 0
    if ratio < 0.25:
        r, g, b = 13, 50, 80
        color = f"#{r:02x}{g:02x}{b:02x}"
        text = "#4a8aaa"
    elif ratio < 0.50:
        r, g, b = 0, 90, 130
        color = f"#{r:02x}{g:02x}{b:02x}"
        text = "#80d0f0"
    elif ratio < 0.75:
        r, g, b = 60, 0, 140
        color = f"#{r:02x}{g:02x}{b:02x}"
        text = "#c0a0ff"
    else:
        r, g, b = 100, 0, 180
        color = f"#{r:02x}{g:02x}{b:02x}"
        text = "#e8d0ff"
    return f"background-color: {color}; color: {text}; font-weight: 600;"

styled_df = (
    df.style
    .applymap(style_heatmap)
    .format("{:,}")
    .set_properties(**{
        "text-align": "right",
        "font-size": "13px",
        "padding": "6px 12px",
        "border": "1px solid #1e3a55",
    })
    .set_table_styles([
        {"selector": "thead th", "props": [
            ("background-color", "#0a1628"),
            ("color", "#00d4ff"),
            ("font-family", "Rajdhani, sans-serif"),
            ("font-size", "13px"),
            ("letter-spacing", "0.1em"),
            ("text-transform", "uppercase"),
            ("padding", "10px 12px"),
            ("border-bottom", "2px solid #00d4ff44"),
        ]},
        {"selector": "tbody th", "props": [
            ("background-color", "#0d1b2a"),
            ("color", "#a0bcd0"),
            ("font-size", "12px"),
            ("padding", "7px 12px"),
            ("border-right", "2px solid #1e3a55"),
            ("white-space", "nowrap"),
        ]},
        {"selector": "table", "props": [
            ("width", "100%"),
            ("border-collapse", "collapse"),
        ]},
    ])
)

st.dataframe(styled_df, use_container_width=True, height=560)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TOTALES POR MES
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Resumen por Mes</div>', unsafe_allow_html=True)

totales = df.sum()
cols_mes = st.columns(len(MESES))
colores = ["blue", "purple", "green", "orange", "blue", "purple", "green"]

for i, (mes, col) in enumerate(zip(MESES, cols_mes)):
    with col:
        val = int(totales[mes])
        pct = (val / volumen_total * 100) if volumen_total > 0 else 0
        st.markdown(f"""
        <div class="metric-card {colores[i]}" style="padding: 1rem;">
            <div class="metric-label" style="font-size:0.62rem;">{mes}</div>
            <div class="metric-value" style="font-size: 1.7rem;">{val:,}</div>
            <div class="metric-delta">{pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color: #2a4060; font-size: 0.75rem; letter-spacing: 0.15em; 
     text-transform: uppercase; padding: 2rem 0 1rem;">
    Sistema de Planificación Catastral · Gestión Operativa · 2025
</div>
""", unsafe_allow_html=True)
