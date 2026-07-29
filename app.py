import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="AGT - Cotizador Multimodal Profesional", page_icon="🌐", layout="wide")

# Estilos visuales con la identidad de AGT (Azul Marino #0B2240 y Naranja #FF6B00)
st.markdown("""
<style>
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-img {
        max-width: 100%;
        height: auto;
        border-radius: 4px;
    }
    .main-title { font-size: 26px; font-weight: bold; color: #0B2240; text-align: center; margin-top: 10px; margin-bottom: 5px; }
    .subtitle { font-size: 14px; color: #FF6B00; font-style: italic; font-weight: bold; text-align: center; margin-bottom: 30px;}
    .section-header { font-size: 18px; font-weight: bold; color: #0B2240; border-left: 6px solid #FF6B00; padding-left: 12px; margin-top: 25px; margin-bottom: 15px;}
    .total-box { background-color: #0B2240; color: white; padding: 25px; border-radius: 8px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
    .total-amount { font-size: 36px; font-weight: bold; color: #FF6B00; margin-top: 5px; display: block; }
    .clause-box { background-color: #FFFDF5; border: 1px solid #FFEBAA; padding: 20px; border-radius: 6px; font-size: 14px; color: #333333; line-height: 1.6; }

    /* Reglas para ocultar la interfaz interactiva al momento de imprimir o guardar PDF */
    @media print {
        .stButton, .stNumberInput, .stSelectbox, .stTextInput, footer, header, .print-section, iframe, .stCheckbox, div[data-testid="stHeader"] { display: none !important; }
        div[data-testid="stSidebar"] { display: none !important; }
        .main-title, .section-header, .total-box, .clause-box, .logo-container, .logo-img { display: block !important; }
    }
</style>
""", unsafe_allow_html=True)

# Renderizado de tu Logo Oficial (vinculado a tu archivo de GitHub)
st.markdown("""
<div class="logo-container">
    <img class="logo-img" src="https://raw.githubusercontent.com/ignacio382/CotizadorAGT/main/5_2.png" onerror="this.src='https://i.imgur.com/8K59cM2.png'" alt="AGT Logo">
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">ARGENTINA GLOBAL TRADE SRL</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">FORWARDER & LOGÍSTICA INTERNACIONAL</div>', unsafe_allow_html=True)

# Base de datos indexada limpia y específica de AGT
raw_data = [
    # CFR Marítimo Exportación FCL
    ["CFR", "Maritimo", "Exportacion", "FCL", "THC 20'", "Por Contenedor", "USD", 295.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "THC 40'", "Por Contenedor", "USD", 335.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "THC RF", "Por Contenedor", "USD", 350.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "Toll", "Por Contenedor", "USD", 170.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "Logistics fee", "Por Contenedor", "USD", 65.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "Handling marítima/Gate in", "Por Contenedor", "USD", 45.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "Emisión de BL", "Por BL", "USD", 65.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "Manejo de documentación", "Por BL", "USD", 95.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "Ingreso SIM", "Por BL", "USD", 50.00],
    ["CFR", "Maritimo", "Exportacion", "FCL", "Precinto", "Por Contenedor", "USD", 10.00],
    
    # DAP Marítimo Importación FCL
    ["DAP", "Maritimo", "Importacion", "FCL", "THC 20'", "Por Contenedor", "USD", 295.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "THC 40'", "Por Contenedor", "USD", 335.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "THC RF", "Por Contenedor", "USD", 350.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Toll", "Por Contenedor", "USD", 170.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Libre deuda", "Por Contenedor", "USD", 95.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Logistics fee", "Por Contenedor", "USD", 65.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Limpieza de contenedor", "Por Contenedor", "USD", 25.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Certificación de flete", "Por BL", "USD", 45.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Ingreso SIM", "Por BL", "USD", 65.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Forwarding Fee", "Por BL", "USD", 95.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "Handling", "Por Contenedor", "USD", 75.00],
    ["DAP", "Maritimo", "Importacion", "FCL", "B/L fee", "Por BL", "USD", 65.00],

    # DAP / DDP / DDU Aéreo Importación
    ["DAP", "Aereo", "Importacion", "Aereo", "Res. 3244/11", "Por Awb parcial", "USD", 20.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Desconsolidación", "Por Bulto Min. USD 20", "USD", 0.50],
    ["DAP", "Aereo", "Importacion", "Aereo", "Handling aerolínea", "Por AWB", "USD", 210.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Manejo de documentación", "Por AWB", "USD", 95.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Carga DGR (si aplica)", "Por Awb (MIN)", "USD", 180.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Transfer fee (if necessary)", "5%, Min. USD 150", "USD", 150.00],
]

# Rellenar combinaciones lógicas dinámicas evitando mezclar Marítimo con Aéreo
all_incoterms = ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"]
all_modalities = ["Maritimo", "Aereo", "Terrestre"]
all_equipos = ["FCL", "LCL", "FCL / LCL", "Aereo", "FTL", "LTL"]

filled_rows = []
existing_keys = set((r[0], r[1], r[2], r[3], r[4]) for r in raw_data)

for inc in all_incoterms:
    for mod in all_modalities:
        for eq in all_equipos:
            template_mod = mod if mod in ["Maritimo", "Aereo"] else "Maritimo"
            template_inc = inc if inc in ["CFR", "DAP"] else "DAP"
            template_eq = "FCL" if eq in ["FCL", "FCL / LCL", "FTL"] else ("LCL" if eq in ["LCL", "LTL"] else "Aereo")
            
            # Forzar a que si el transporte es Aéreo, busque plantillas puramente aéreas
            if template_mod == "Aereo":
                matches = [r for r in raw_data if r[1] == "Aereo"]
            else:
                matches = [r for r in raw_data if r[0] == template_inc and r[1] == "Maritimo" and r[3] == template_eq]
                
            if not matches:
                matches = [r for r in raw_data if r[0] == "DAP" and r[1] == "Maritimo" and r[3] == "FCL"]
                
            for m in matches:
                if (inc, mod, "Importacion", eq, m[4]) not in existing_keys:
                    filled_rows.append([inc, mod, "Importacion", eq, m[4], m[5], m[6], m[7]])
                    existing_keys.add((inc, mod, "Importacion", eq, m[4]))

for r in raw_data:
    filled_rows.append(r)

df = pd.DataFrame(filled_rows, columns=["Incoterm", "Modalidad", "Operacion", "TipoEquipamiento", "Concepto", "Unidad", "Moneda", "Compra"])

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header">1. Parámetros e Información General</div>', unsafe_allow_html=True)
    ref_num = st.text_input("Número de Referencia", value="AGT-2026-4821")
    
    fecha_cotizacion = st.date_input("Fecha de Emisión de Cotización", value=datetime.today())
    fecha_validez = fecha_cotizacion + timedelta(days=5)
    st.caption(f"📅 **Validez automática de la propuesta (5 días corridos):** Hasta el {fecha_validez.strftime('%d/%m/%Y')}")
    
    incoterm = st.selectbox("Regla Incoterm", options=all_incoterms, index=4)
    modalidad = st.selectbox("Tipo de Transporte / Vía", options=all_modalities, index=0)
    
    # Filtrado dinámico de opciones de equipamiento según vía elegida para evitar errores
    if modalidad == "Aereo":
        eq_options = ["Aereo"]
    elif modalidad == "Terrestre":
        eq_options = ["FTL", "LTL", "FCL / LCL"]
    else:
        eq_options = ["FCL", "LCL", "FCL / LCL"]
        
    tipo_eq = st.selectbox("Tipo de Equipamiento / Modalidad de Carga", options=eq_options)
    
    container_size = "N/A"
    if modalidade != "Aereo" and ("FCL" in tipo_eq or "FTL" in tipo_eq):
        container_size = st.selectbox("Modelo del Contenedor (Filtro THC)", ["20' Standard", "40' HQ / Standard", "Reefer (RF)"])
        
    cantidad = st.number_input("Cantidad de Contenedores / Bultos", min_value=1, value=1)
    
    if modalidad == "Maritimo":
        st.markdown("**⏱️ Datos de Tránsito Marítimo:**")
        tt_days = st.number_input("Transit Time (TT en días)", min_value=0, value=14)
        free_days = st.number_input("Días Libres de Demoras en Destino", min_value=0, value=7)

with col2:
    st.markdown('<div class="section-header">2. Componentes de Tarifas y Flete Internacional</div>', unsafe_allow_html=True)
    flete_intl = st.number_input("Flete Internacional Base (USD)", min_value=0.0, value=1850.0)
    gastos_term = st.number_input("Gastos Portuarios / Terminal Aérea o Terrestre (USD)", min_value=0.0, value=650.0)
    profit_share = st.number_input("Profit Share Neto AGT / Margen Operativo (USD)", min_value=0.0, value=50.0)
    
    st.markdown("**🚚 Segmento de Distribución Terrestre / Delivery:**")
    apply_delivery = st.checkbox("¿Aplica Flete Interno / Delivery / Pick Up?", value=True)
    if apply_delivery:
        del_from = st.text_input("Origen del Flete Local (Desde)", value="Puerto de Buenos Aires" if modalidad == "Maritimo" else "Aeropuerto de Ezeiza")
        del_to = st.text_input("Destino del Flete Local (Hasta)", value="Planta Industrial del Cliente")
        delivery_cost = st.number_input("Valor del Delivery (USD)", min_value=0.0, value=450.0)
    else:
        delivery_cost = 0.0

# Módulo Despacho de Aduana Especial si es DDP
despacho_total = 0.0
if incoterm == "DDP":
    st.markdown('<div class="section-header">3. Módulo Despacho de Aduana (Requisito Incoterm DDP)</div>', unsafe_allow_html=True)
    c_ad1, c_ad2 = st.columns(2)
    with c_ad1:
        st.markdown("**Gastos de Nacionalización / Despachante:**")
        honorarios = st.number_input("Honorarios del Despachante (USD)", min_value=0.0, value=200.0)
        gastos_despacho = st.number_input("Gastos Operativos de Despacho (USD)", min_value=0.0, value=120.0)
        digitalizacion = st.number_input("Tasa de Digitalización SIM / Aduanera (USD)", min_value=0.0, value=45.0)
        despacho_total = honorarios + gastos_despacho + digitalizacion
        
    with c_ad2:
        st.markdown("**Duties and Taxes (HTS / Clasificación Arancelaria):**")
        hts_code = st.text_input("Posición Arancelaria HTS / NCM", value="8471.30.12")
        duty_pct = st.number_input("Derechos de Importación / Duty (%)", min_value=0.0, max_value=100.0, value=14.0) / 100.0
        iva_pct = st.number_input("IVA General (%)", min_value=0.0, max_value=100.0, value=21.0) / 100.0
        iva_adicional = st.number_input("IVA Adicional (%)", min_value=0.0, max_value=100.0, value=20.0) / 100.0
        other_taxes = st.number_input("Otros Impuestos / Tasas Estadísticas (%)", min_value=0.0, max_value=100.0, value=3.0) / 100.0
        
        valor_cif = flete_intl + 20000.0
        duties_calculated = valor_cif * (duty_pct + iva_pct + iva_adicional + other_taxes)
        st.caption(f"💵 **Impuestos Provisionales Calculados (Est.):** USD {duties_calculated:,.2f}")
        despacho_total += duties_calculated

# Filtrado estricto por Modalidad y Tipo de Equipamiento
filtered_df = df[
    (df['Incoterm'] == incoterm) & 
    (df['Modalidad'] == modalidad) & 
    (df['TipoEquipamiento'] == tipo_eq)
].copy()

if container_size != "N/A" and not filtered_df.empty:
    def match_thc(row_concept):
        if "THC" in row_concept:
            if container_size == "20' Standard" and "20'" in row_concept: return True
            if container_size == "40' HQ / Standard" and "40'" in row_concept: return True
            if container_size == "Reefer (RF)" and "RF" in row_concept: return True
            return False
        return True
    filtered_df = filtered_df[filtered_df['Concepto'].apply(match_thc)]

st.markdown('<div class="section-header">4. Conceptos Fijos Locales desde Base de Datos</div>', unsafe_allow_html=True)
if not filtered_df.empty:
    filtered_df['Total'] = filtered_df['Compra'] * cantidad
    st.dataframe(filtered_df[['Concepto', 'Unidad', 'Moneda', 'Compra', 'Total']], use_container_width=True, hide_index=True)
    fijos_total = filtered_df['Total'].sum()
else:
    fijos_total = 0.0
    st.info("No se registran cargos fijos adicionales automáticos para este perfil.")

# Totales Consolidados
gran_total = fijos_total + flete_intl + gastos_term + delivery_cost + profit_share + despacho_total

st.markdown('<div class="section-header">5. Consolidación de Liquidación y Totales</div>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Fijos Locales + Flete", f"USD {(fijos_total + flete_intl + gastos_term + profit_share):,.2f}")
m2.metric("Logística Interna / Delivery", f"USD {delivery_cost:,.2f}")
if incoterm == "DDP":
    m3.metric("Módulo Aduana & Taxes (DDP)", f"USD {despacho_total:,.2f}")

st.markdown(f'''
<div class="total-box">
    Valor Total Proyectado de Cotización ({ref_num})<br>
    <span class="total-amount">USD {gran_total:,.2f}</span>
</div>
''', unsafe_allow_html=True)

# Cláusulas legales operativas
st.markdown('<div class="section-header">6. Términos Legales, Validez y Validez del Servicio</div>', unsafe_allow_html=True)
clausula_final = f"• **VALIDEZ TEMPORAL:** Esta propuesta es válida hasta el **{fecha_validez.strftime('%d/%m/%Y')}** (5 días desde su emisión).\n"
if modalidad == "Maritimo":
    clausula_final += f"• **TIEMPOS DE DESTINO:** Transit Time estimado en **{tt_days} días** con un período de **{free_days} días libres** en puerto de destino.\n"
if apply_delivery:
    clausula_final += f"• **ENTREGA TERRESTRE:** Servicio de delivery programado desde *{del_from}* hasta *{del_to}* por un importe cerrado de USD {delivery_cost:,.2f}.\n"
clausula_final += "• **REGULACIONES:** Las cotizaciones están sujetas a variaciones de recargos BAF/CAF por parte de los carriers y espacio disponible al momento de la reserva."

st.markdown(f'<div class="clause-box">{clausula_final.replace("\n", "<br>")}</div>', unsafe_allow_html=True)

# Sección de Impresión Forzada vía Parent Iframe Javascript
st.markdown('<div class="section-header print-section">7. Acciones de Exportación e Impresión</div>', unsafe_allow_html=True)

components.html(
    """
    <style>
        .print-btn {
            background-color: #FF6B00;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 15px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 100%;
        }
        .print-btn:hover {
            background-color: #e05e00;
        }
    </style>
    <button class="print-btn" onclick="window.parent.print()">🖨️ Imprimir Cotización / Guardar en PDF</button>
    """,
    height=60,
)
st.markdown('<div class="print-note print-section">Nota técnica: Si tu navegador bloquea las ventanas emergentes del servidor de Streamlit, recuerda que puedes usar el atajo de teclado nativo de tu sistema en cualquier momento: **Ctrl + P** en Windows o **Cmd + P** en Mac.</div>', unsafe_allow_html=True)
