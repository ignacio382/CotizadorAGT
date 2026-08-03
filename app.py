import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="AGT - Cotizador Multimodal Profesional", page_icon="🌐", layout="wide")

# Estilos visuales con la identidad de AGT optimizados para pantalla e impresión directa limpia
st.markdown("""
<style>
    /* ---------------- ESTILOS DE PANTALLA (WEB) ---------------- */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 6px;
        border-bottom: 2px solid #0B2240;
        margin-bottom: 12px;
        flex-wrap: nowrap;
    }
    .logo-right { 
        max-width: 340px; 
        height: auto; 
        border-radius: 2px; 
    }
    .quote-title-left { 
        font-size: 20px; 
        font-weight: bold; 
        color: #0B2240; 
        font-family: 'Segoe UI', sans-serif;
        white-space: nowrap;
    }
    .section-header { 
        font-size: 15px; 
        font-weight: bold; 
        color: #0B2240; 
        border-left: 5px solid #FF6B00; 
        padding-left: 10px; 
        margin-top: 15px; 
        margin-bottom: 10px;
    }
    .clause-box { background-color: #FFFDF5; border: 1px solid #FFEBAA; padding: 12px; border-radius: 6px; font-size: 13.0px; color: #333333; line-height: 1.4; }
    
    .total-row-container {
        display: flex; justify-content: flex-end; align-items: center; gap: 15px;
        margin-top: 20px; margin-bottom: 20px; padding: 10px 20px;
        background-color: #0B2240; border-radius: 6px; max-width: 400px; margin-left: auto;
    }
    .total-label-text { font-size: 16px; font-weight: bold; color: #ffffff; letter-spacing: 1px; }
    .total-price-text { font-size: 24px; font-weight: bold; color: #FF6B00; }
    
    .print-only-block { display: none; }

    /* ---------------- REGLAS DE IMPRESIÓN DIRECTA NATIVA (PDF) ---------------- */
    @media print {
        div[data-testid="stSidebar"], div[data-testid="stHeader"], footer, header, .print-section, iframe, 
        .stCheckbox, button, .stWidget, div[role="radiogroup"], div[data-testid="stHorizontalBlock"] { 
            display: none !important; 
        }
        
        @page {
            margin: 1.2cm !important;
            size: auto;
        }
        
        .print-only-block { 
            display: block !important; 
            width: 100% !important;
        }
        
        body, p, div, span, td, th {
            font-size: 9.5pt !important; 
            color: #111111 !important;
            font-family: 'Segoe UI', Arial, sans-serif !important;
            background-color: transparent !important;
            background: transparent !important;
        }
        
        .header-container { 
            display: flex !important; 
            justify-content: space-between !important;
            align-items: center !important;
            border-bottom: 2px solid #0B2240 !important; 
            margin-bottom: 25px !important; 
            padding-bottom: 8px !important;
            page-break-inside: avoid !important;
        }
        .logo-right { 
            display: block !important; 
            width: 340px !important; 
            max-width: 340px !important;
            height: auto !important;
        }
        .quote-title-left { 
            display: block !important; 
            font-size: 18pt !important; 
        }
        
        .section-header { 
            display: flex !important; 
            border-left: 4px solid #FF6B00 !important; 
            font-size: 11pt !important; 
            margin-top: 15px !important; 
            margin-bottom: 8px !important; 
            padding-left: 8px !important;
            page-break-after: avoid !important;
        }
        
        .data-grid-print {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 10px 30px !important;
            margin-bottom: 15px !important;
            width: 100% !important;
        }
        .data-item-print {
            border-bottom: 1px solid #E2E8F0 !important;
            padding-bottom: 3px !important;
            line-height: 1.2 !important;
        }
        
        .stDataFrame, table { 
            display: table !important; 
            width: 100% !important;
            margin-bottom: 15px !important;
            page-break-inside: auto !important;
        }
        tr { page-break-inside: avoid !important; page-break-after: auto !important; }
        td, th { padding: 4px 6px !important; font-size: 9.5pt !important; border: 1px solid #CBD5E1 !important; }

        .clause-box { 
            display: block !important; 
            background-color: #FFFDF5 !important; 
            border: 1px solid #FFEBAA !important; 
            padding: 10px !important; 
            margin-top: 10px !important;
            page-break-inside: avoid !important;
        }
        .total-row-container { 
            display: flex !important; 
            background-color: #0B2240 !important; 
            padding: 6px 15px !important; 
            margin-top: 12px !important;
            page-break-inside: avoid !important;
        }
        .total-price-text { color: #FF6B00 !important; font-size: 16pt !important; }
    }
</style>
""", unsafe_allow_html=True)

# FILTRO INVISIBLE DE PERFIL COMERCIAL (SOLO EN SIDEBAR)
st.sidebar.markdown("### 👥 Perfil Comercial")
destinatario = st.sidebar.selectbox("Tipo de Destinatario", ["Cliente", "Agente"])

# Cabecera Unificada
st.markdown(f"""
<div class="header-container">
    <div class="quote-title-left">COTIZACIÓN DE EMBARQUE MULTI-OPCIÓN</div>
    <div>
        <img class="logo-right" src="https://raw.githubusercontent.com/ignacio382/CotizadorAGT/main/5_2.png" onerror="this.src='https://i.imgur.com/8K59cM2.png'" alt="AGT Logo">
    </div>
</div>
""", unsafe_allow_html=True)

all_incoterms = ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "DDU", "FAS", "FOB", "CFR", "CIF"]

# ---------------- CONTROLES INTERACTIVOS (SÓLO PANTALLA) ----------------
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header">1. Información General</div>', unsafe_allow_html=True)
    ref_num = st.text_input("Número de Referencia", value="AGT-2026-4821")
    fecha_cotizacion = st.date_input("Fecha de Emisión", value=datetime.today())
    operacion = st.selectbox("Tipo de Operación", ["Exportacion", "Importacion"])
    incoterm = st.selectbox("Condición de Venta / Incoterm", options=all_incoterms, index=10) # FOB por defecto
    modalidad = st.selectbox("Vía de Transporte", ["Maritimo", "Aereo", "Terrestre"])
    
    if modalidad == "Aereo": eq_options = ["Aereo"]
    elif modalidad == "Terrestre": eq_options = ["FTL", "LTL"]
    else: eq_options = ["FCL", "LCL"]
    tipo_eq = st.selectbox("Modalidad de Carga", options=eq_options)
    
    # NUEVA FUNCIONALIDAD: SELECTOR DE CANTIDAD DE OPCIONES SIMULTÁNEAS
    cant_opciones = st.radio("Estructura de Cotización", ["1 Opción Única", "2 Opciones en Simultáneo (Comparativa)"], horizontal=True)

    st.markdown('<div class="section-header">Configuración Operativa: Opción 1</div>', unsafe_allow_html=True)
    nombre_transporte_1 = st.text_input("Línea Marítima / Carrier (Opción 1)", value="Maersk")
    ruta_1 = st.text_input("Ruta Proyectada (Opción 1)", value="Buenos Aires – Callao (vía Santos)")
    tt_days_1 = st.number_input("Transit Time Días (Opción 1)", min_value=0, value=24)
    free_days_1 = st.number_input("Días Libres Destino (Opción 1)", min_value=0, value=6)
    
    if cant_opciones == "2 Opciones en Simultáneo (Comparativa)":
        st.markdown('<div class="section-header">Configuración Operativa: Opción 2</div>', unsafe_allow_html=True)
        nombre_transporte_2 = st.text_input("Línea Marítima / Carrier (Opción 2)", value="Maersk")
        ruta_2 = st.text_input("Ruta Proyectada (Opción 2)", value="Rosario – Callao (vía Itapoa)")
        tt_days_2 = st.number_input("Transit Time Días (Opción 2)", min_value=0, value=32)
        free_days_2 = st.number_input("Días Libres Destino (Opción 2)", min_value=0, value=6)

with col2:
    st.markdown('<div class="section-header">2. Tarifas por Tipo de Equipo (Flete Base)</div>', unsafe_allow_html=True)
    
    st.markdown("**Matriz Tarifaria: Opción 1 (USD)**")
    flete_20_op1 = st.number_input("Flete 1x20ST (Opción 1)", min_value=0.0, value=2447.0)
    flete_40_op1 = st.number_input("Flete 1x40ST (Opción 1)", min_value=0.0, value=2597.0)
    flete_40hq_op1 = st.number_input("Flete 1x40HQ (Opción 1)", min_value=0.0, value=2597.0)
    
    if cant_opciones == "2 Opciones en Simultáneo (Comparativa)":
        st.markdown("**Matriz Tarifaria: Opción 2 (USD)**")
        flete_20_op2 = st.number_input("Flete 1x20ST (Opción 2)", min_value=0.0, value=2668.0)
        flete_40_op2 = st.number_input("Flete 1x40ST (Opción 2)", min_value=0.0, value=2818.0)
        flete_40hq_op2 = st.number_input("Flete 1x40HQ (Opción 2)", min_value=0.0, value=2818.0)

    st.markdown('<div class="section-header">3. Recargos y Gastos Fijos de Terminal</div>', unsafe_allow_html=True)
    gastos_term = st.number_input("Gastos Terminal / Depósito Aprox. (USD)", min_value=0.0, value=0.0)
    delivery_cost = st.number_input("Valor del Delivery Terrestre si aplica (USD)", min_value=0.0, value=0.0)

    st.markdown('<div class="section-header">Concepto Fijo Adicional Manual</div>', unsafe_allow_html=True)
    manual_concepto = st.text_input("Nombre de Gasto Extra (ej: Telex Release)", value="Telex release")
    manual_precio = st.number_input("Monto Neto Gasto Extra (USD)", min_value=0.0, value=75.0)

# --- DETECTAR SI ES FOB MARÍTIMO ---
is_fob_maritimo = (incoterm == "FOB" and modalidad == "Maritimo")

# ---------------- GENERACIÓN DE MATRIZ DE CONCEPTOS FIJOS ----------------
rows_to_render = []
fijos_total_calc = 0.0

if is_fob_maritimo:
    if operacion == "Exportacion":
        # Se inyecta el Profit Share Exento requerido con la leyenda formal de las imágenes
        rows_to_render.append({
            "Concepto": "Profit Share AGT *Tarifas netas, nuestro Profit Share es USD 50/cont / *Flete Collect / *Sujeto a disponibilidad y espacio.",
            "Unidad": "x Contenedor", "Moneda": "USD", "Tarifa Base": "USD 50.00", "Subtotal": "USD 50.00", "IVA (21%)": "Exento"
        })
        fijos_total_calc += 50.0
    else:
        rows_to_render.append({
            "Concepto": "Profit Share AGT (Importación)",
            "Unidad": "x Contenedor", "Moneda": "USD", "Tarifa Base": "USD 50.00", "Subtotal": "USD 50.00", "IVA (21%)": "Exento"
        })
        fijos_total_calc += 50.0

if manual_concepto.strip() != "" and manual_precio > 0:
    rows_to_render.append({
        "Concepto": manual_concepto.strip(), "Unidad": "x Embarque", "Moneda": "USD",
        "Tarifa Base": f"USD {manual_precio:,.2f}", "Subtotal": f"USD {manual_precio:,.2f}", "IVA (21%)": "Exento"
    })
    fijos_total_calc += manual_precio

st.markdown('<div class="section-header">4. Desglose de Gastos Locales Complementarios</div>', unsafe_allow_html=True)
if rows_to_render:
    st.dataframe(pd.DataFrame(rows_to_render), use_container_width=True, hide_index=True)

# ---------------- COMPACTACIÓN EXCLUSIVA PARA EL PDF IMPRESO ----------------
# Se arma una cuadrícula limpia eliminando los selectores web para que queden las opciones presentadas de forma impecable
html_opciones_print = f"""
<div class="data-item-print"><b>OPCIÓN 1 - VÍA {nombre_transporte_1.upper()}</b></div>
<div class="data-item-print"><b>Ruta:</b> {ruta_1} | <b>Transit Time:</b> {tt_days_1} días | <b>Días Libres:</b> {free_days_1} días</div>
<div class="data-item-print"><b>Tarifas Flete:</b> 20' ST: USD {flete_20_op1:,.2f} | 40' ST: USD {flete_40_op1:,.2f} | 40' HQ: USD {flete_40hq_op1:,.2f}</div>
"""

if cant_opciones == "2 Opciones en Simultáneo (Comparativa)":
    html_opciones_print += f"""
    <br>
    <div class="data-item-print"><b>OPCIÓN 2 - VÍA {nombre_transporte_2.upper()}</b></div>
    <div class="data-item-print"><b>Ruta:</b> {ruta_2} | <b>Transit Time:</b> {tt_days_2} días | <b>Días Libres:</b> {free_days_2} días</div>
    <div class="data-item-print"><b>Tarifas Flete:</b> 20' ST: USD {flete_20_op2:,.2f} | 40' ST: USD {flete_40_op2:,.2f} | 40' HQ: USD {flete_40hq_op2:,.2f}</div>
    """

st.markdown(f"""
<div class="print-only-block">
    <div class="section-header">1. Información de Referencia</div>
    <div class="data-grid-print">
        <div class="data-item-print"><b>Cotización ID:</b> {ref_num}</div>
        <div class="data-item-print"><b>Fecha de Emisión:</b> {fecha_cotizacion.strftime('%d/%m/%Y')}</div>
        <div class="data-item-print"><b>Régimen Incoterm:</b> {incoterm} ({operacion})</div>
        <div class="data-item-print"><b>Modalidad:</b> {tipo_eq} {modalidad}</div>
    </div>
    <div class="section-header">2. Cotización de Fletes Internacionales</div>
    {html_opciones_print}
</div>
""", unsafe_allow_html=True)

# Cálculo indicativo sobre la opción máxima para el casillero global obligatorio de Streamlit
gran_total_indicativo = max(flete_40hq_op1, flete_40hq_op2 if 'flete_40hq_op2' in locals() else 0.0) + fijos_total_calc + gastos_term + delivery_cost
fecha_validez = fecha_cotizacion + timedelta(days=14)

st.markdown(f'''
<div class="total-row-container">
    <div class="total-label-text">TOTAL ESTIMADO MAX</div>
    <div class="total-price-text">USD {gran_total_indicativo:,.2f}</div>
</div>
''', unsafe_allow_html=True)

# Cláusulas legales de Lucio limpias y ordenadas
st.markdown('<div class="section-header">5. Términos Legales y Condiciones del Embarque</div>', unsafe_allow_html=True)

clausula_final = f"VALIDEZ TEMPORAL: Esta propuesta se encuentra sujeta a términos Spot con validez regular de mercado.<br>"
clausula_final += "CONDICIONES DE CARGA: Válido exclusivamente para el transporte y manipulación de Carga General Comercial.<br>"
clausula_final += "EXCLUSIONES OPERATIVAS: No se incluyen gastos portuarios en destino, seguro internacional de mercaderías, almacenajes, estadías ni ningún otro concepto que no se encuentre expresamente listado en esta propuesta.<br>"
clausula_final += "DESPACHO ADUANERO: Los servicios de despacho de aduana no están contemplados en la presente cotización comercial corporativa.<br>"
clausula_final += "REGULACIONES: Las cotizaciones están sujetas a variaciones de recargos BAF/CAF por parte de las líneas marítimas asignadas y a la efectiva disponibilidad de espacio físico en los buques al momento de procesar el booking."

st.markdown(f'<div class="clause-box">{clausula_final}</div>', unsafe_allow_html=True)

components.html(
    """
    <button style="background-color: #FF6B00; color: white; border: none; padding: 12px 24px; border-radius: 4px; cursor: pointer; font-size: 15px; font-family: 'Segoe UI', sans-serif; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%;" onclick="window.parent.print()">🖨️ Imprimir Cotización / Guardar en PDF</button>
    """,
    height=60,
)
