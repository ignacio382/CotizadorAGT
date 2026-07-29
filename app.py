import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="AGT - Cotizador Multimodal Profesional", page_icon="🌐", layout="wide")

# Estilos visuales optimizados (Logo a la derecha, cabecera compacta y total simplificado)
st.markdown("""
<style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 10px;
        border-bottom: 2px solid #0B2240;
        margin-bottom: 20px;
    }
    .logo-right {
        max-width: 280px;
        height: auto;
        border-radius: 2px;
    }
    .quote-title-left {
        font-size: 24px;
        font-weight: bold;
        color: #0B2240;
        font-family: 'Segoe UI', sans-serif;
    }
    .section-header { 
        font-size: 16px; 
        font-weight: bold; 
        color: #0B2240; 
        border-left: 5px solid #FF6B00; 
        padding-left: 10px; 
        margin-top: 20px; 
        margin-bottom: 12px;
    }
    .clause-box { background-color: #FFFDF5; border: 1px solid #FFEBAA; padding: 15px; border-radius: 6px; font-size: 13.5px; color: #333333; line-height: 1.5; }
    .print-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; margin-bottom: 12px; font-size: 13.5px; }

    /* Contenedor compacto para el TOTAL */
    .total-row-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 15px;
        margin-top: 25px;
        margin-bottom: 25px;
        padding: 12px 25px;
        background-color: #0B2240;
        border-radius: 6px;
        max-width: 450px;
        margin-left: auto;
    }
    .total-label-text {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        letter-spacing: 1px;
    }
    .total-price-text {
        font-size: 26px;
        font-weight: bold;
        color: #FF6B00;
    }

    @media print {
        .stButton, .stNumberInput, .stSelectbox, .stTextInput, .stDateInput, footer, header, .print-section, iframe, .stCheckbox, div[data-testid="stHeader"], div[data-testid="stSidebar"] { display: none !important; }
        .header-container, .section-header, .clause-box, .print-card, .total-row-container, .logo-right { display: flex !important; }
    }
</style>
""", unsafe_allow_html=True)

# CONTROL DE IMPRESIÓN (INTERRUPTOR DE SEGURIDAD EN SIDEBAR)
st.sidebar.markdown("### 🖨️ Panel de Impresión")
modo_impresion = st.sidebar.checkbox("Activar Modo Vista de Impresión (PDF)", value=False)

# Cabecera Compacta: Título de Cotización a la izquierda y Logo chico a la derecha
st.markdown("""
<div class="header-container">
    <div class="quote-title-left">COTIZACIÓN DE EMBARQUE INTERNACIONAL</div>
    <div>
        <img class="logo-right" src="https://raw.githubusercontent.com/ignacio382/CotizadorAGT/main/5_2.png" onerror="this.src='https://i.imgur.com/8K59cM2.png'" alt="AGT Logo">
    </div>
</div>
""", unsafe_allow_html=True)

# Base de datos limpia de AGT
raw_data = [
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

    ["DAP", "Aereo", "Importacion", "Aereo", "Res. 3244/11", "Por Awb parcial", "USD", 20.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Desconsolidación", "Por Bulto Min. USD 20", "USD", 0.50],
    ["DAP", "Aereo", "Importacion", "Aereo", "Handling aerolínea", "Por AWB", "USD", 210.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Manejo de documentación", "Por AWB", "USD", 95.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Carga DGR (si aplica)", "Por Awb (MIN)", "USD", 180.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Transfer fee (if necessary)", "5%, Min. USD 150", "USD", 150.00],

    ["DAP", "Terrestre", "Importacion", "FTL", "Documentación Terrestre Gral.", "Por CTR/Camión", "USD", 85.00],
    ["DAP", "Terrestre", "Importacion", "FTL", "Peajes Internacionales", "Por Viaje", "USD", 120.00],
    ["DAP", "Terrestre", "Importacion", "LTL", "Manejo de guía CRT", "Por Remisión", "USD", 45.00],
    ["DAP", "Terrestre", "Importacion", "LTL", "Consolidación en Depósito", "Por Pallet", "USD", 25.00],
]

all_incoterms = ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"]
all_modalities = ["Maritimo", "Aereo", "Terrestre"]
all_equipos = ["FCL", "LCL", "FCL / LCL", "Aereo", "FTL", "LTL"]

filled_rows = []
existing_keys = set((r[0], r[1], r[2], r[3], r[4]) for r in raw_data)

for inc in all_incoterms:
    for mod in all_modalities:
        for eq in all_equipos:
            template_mod = mod
            template_inc = inc if inc in ["CFR", "DAP"] else "DAP"
            template_eq = eq
            
            if template_mod == "Aereo":
                matches = [r for r in raw_data if r[1] == "Aereo"]
            elif template_mod == "Terrestre":
                matches = [r for r in raw_data if r[1] == "Terrestre" and (template_eq in r[3] or "LTL" in r[3] if template_eq == "LTL" else "FTL" in r[3])]
                if not matches:
                    matches = [r for r in raw_data if r[1] == "Terrestre" and r[3] == "LTL"]
            else:
                target_eq = "LCL" if template_eq == "LCL" else "FCL"
                matches = [r for r in raw_data if r[0] == template_inc and r[1] == "Maritimo" and r[3] == target_eq]
                
            for m in matches:
                if (inc, mod, "Importacion", eq, m[4]) not in existing_keys:
                    filled_rows.append([inc, mod, "Importacion", eq, m[4], m[5], m[6], m[7]])
                    existing_keys.add((inc, mod, "Importacion", eq, m[4]))

for r in raw_data:
    filled_rows.append(r)

df = pd.DataFrame(filled_rows, columns=["Incoterm", "Modalidad", "Operacion", "TipoEquipamiento", "Concepto", "Unidad", "Moneda", "Compra"])

# Inicializaciones base por defecto para evitar NameError en modos no marítimos
tt_days = 0
free_days = 0

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header">1. Parámetros e Información General</div>', unsafe_allow_html=True)
    if not modo_impresion:
        ref_num = st.text_input("Número de Referencia", value="AGT-2026-4821")
        fecha_cotizacion = st.date_input("Fecha de Emisión", value=datetime.today())
        incoterm = st.selectbox("Regla Incoterm", options=all_incoterms, index=4)
        modalidad = st.selectbox("Tipo de Transporte / Vía", options=all_modalities, index=0)
        
        if modalidad == "Aereo": eq_options = ["Aereo"]
        elif modalidad == "Terrestre": eq_options = ["FTL", "LTL", "FCL / LCL"]
        else: eq_options = ["FCL", "LCL", "FCL / LCL"]
        tipo_eq = st.selectbox("Tipo de Equipamiento", options=eq_options)
        
        container_size = "N/A"
        if modalidad == "Maritimo" and ("FCL" in tipo_eq or "FTL" in tipo_eq):
            container_size = st.selectbox("Modelo del Contenedor", ["20' Standard", "40' HQ / Standard", "Reefer (RF)"])
            
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
        
        if modalidad == "Maritimo":
            nombre_transporte = st.text_input("Línea Marítima / Buque", value="Hapag-Lloyd - SAN CLEMENTE V.260W")
        elif modalidad == "Aereo":
            nombre_transporte = st.text_input("Línea Aérea / Vuelo", value="Lufthansa - LH511")
        else:
            nombre_transporte = st.text_input("Empresa de Transporte / Patente", value="Transportes Int. - CTR-765")
            
        etd_date = st.date_input("Fecha Salida (ETD)", value=datetime.today() + timedelta(days=7))
        eta_date = st.date_input("Fecha Llegada (ETA)", value=datetime.today() + timedelta(days=21))
        
        if modalidad == "Maritimo":
            tt_days = st.number_input("Transit Time (Días)", min_value=0, value=14)
            free_days = st.number_input("Días Libres en Destino", min_value=0, value=7)
    else:
        ref_num = st.session_state.get('ref_num', "AGT-2026-4821")
        fecha_cotizacion = st.session_state.get('fecha_cotizacion', datetime.today())
        incoterm = st.session_state.get('incoterm', "DAP")
        modalidad = st.session_state.get('modalidad', "Maritimo")
        tipo_eq = st.session_state.get('tipo_eq', "FCL")
        container_size = st.session_state.get('container_size', "40' HQ / Standard")
        cantidad = st.session_state.get('cantidad', 1)
        nombre_transporte = st.session_state.get('nombre_transporte', "Hapag-Lloyd - SAN CLEMENTE V.260W")
        etd_date = st.session_state.get('etd_date', datetime.today() + timedelta(days=7))
        eta_date = st.session_state.get('eta_date', datetime.today() + timedelta(days=21))
        tt_days = st.session_state.get('tt_days', 0)
        free_days = st.session_state.get('free_days', 0)
        
        st.markdown(f"""
        <div class="print-card">
            <b>Referencia:</b> {ref_num}<br>
            <b>Fecha Emisión:</b> {fecha_cotizacion.strftime('%d/%m/%Y')}<br>
            <b>Incoterm:</b> {incoterm} | <b>Vía:</b> {modalidad} ({tipo_eq})<br>
            <b>Equipo:</b> {container_size} | <b>Cantidad:</b> {cantidad}<br>
            <b>Transporte:</b> {nombre_transporte}<br>
            <b>Cronograma:</b> ETD: {etd_date.strftime('%d/%m/%Y')} | ETA: {eta_date.strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-header">2. Componentes de Tarifas y Flete Internacional</div>', unsafe_allow_html=True)
    if not modo_impresion:
        flete_intl = st.number_input("Flete Internacional Base (USD)", min_value=0.0, value=1850.0)
        gastos_term = st.number_input("Gastos Portuarios / Terminal (USD)", min_value=0.0, value=650.0)
        profit_share = st.number_input("Profit Share Neto AGT (USD)", min_value=0.0, value=50.0)
        apply_delivery = st.checkbox("¿Aplica Flete Interno / Delivery?", value=True)
        
        if apply_delivery:
            del_from = st.text_input("Origen del Flete Local", value="Puerto de Buenos Aires" if modalidad == "Maritimo" else "Aeropuerto de Ezeiza")
            del_to = st.text_input("Destino del Flete Local", value="Planta Industrial del Cliente")
            delivery_cost = st.number_input("Valor del Delivery (USD)", min_value=0.0, value=450.0)
        else:
            delivery_cost = 0.0
            del_from, del_to = "N/A", "N/A"
            
        st.session_state['ref_num'] = ref_num
        st.session_state['fecha_cotizacion'] = fecha_cotizacion
        st.session_state['incoterm'] = incoterm
        st.session_state['modalidad'] = modalidad
        st.session_state['tipo_eq'] = tipo_eq
        st.session_state['container_size'] = container_size
        st.session_state['cantidad'] = cantidad
        st.session_state['nombre_transporte'] = nombre_transporte
        st.session_state['etd_date'] = etd_date
        st.session_state['eta_date'] = eta_date
        st.session_state['tt_days'] = tt_days
        st.session_state['free_days'] = free_days
        st.session_state['flete_intl'] = flete_intl
        st.session_state['gastos_term'] = gastos_term
        st.session_state['profit_share'] = profit_share
        st.session_state['delivery_cost'] = delivery_cost
        st.session_state['apply_delivery'] = apply_delivery
        st.session_state['del_from'] = del_from
        st.session_state['del_to'] = del_to
    else:
        flete_intl = st.session_state.get('flete_intl', 1850.0)
        gastos_term = st.session_state.get('gastos_term', 650.0)
        profit_share = st.session_state.get('profit_share', 50.0)
        delivery_cost = st.session_state.get('delivery_cost', 450.0)
        apply_delivery = st.session_state.get('apply_delivery', True)
        del_from = st.session_state.get('del_from', "Puerto de Buenos Aires")
        del_to = st.session_state.get('del_to', "Planta Industrial")
        
        st.markdown(f"""
        <div class="print-card">
            <b>Flete Internacional Base:</b> USD {flete_intl:,.2f}<br>
            <b>Gastos Terminal:</b> USD {gastos_term:,.2f}<br>
            <b>Profit Share AGT:</b> USD {profit_share:,.2f}<br>
            <b>Delivery Local:</b> USD {delivery_cost:,.2f} (Desde {del_from} hasta {del_to})
        </div>
        """, unsafe_allow_html=True)

# Módulo Despacho de Aduana Especial si es DDP
despacho_total = 0.0
if incoterm == "DDP":
    st.markdown('<div class="section-header">3. Módulo Despacho de Aduana (DDP)</div>', unsafe_allow_html=True)
    if not modo_impresion:
        honorarios = st.number_input("Honorarios Despachante (USD)", min_value=0.0, value=200.0)
        gastos_despacho = st.number_input("Gastos Operativos (USD)", min_value=0.0, value=120.0)
        digitalizacion = st.number_input("Tasa Digitalización SIM (USD)", min_value=0.0, value=45.0)
        
        duty_pct = st.number_input("Duty (%)", min_value=0.0, max_value=100.0, value=14.0) / 100.0
        iva_pct = st.number_input("IVA (%)", min_value=0.0, max_value=100.0, value=21.0) / 100.0
        iva_adicional = st.number_input("IVA Adicional (%)", min_value=0.0, max_value=100.0, value=20.0) / 100.0
        other_taxes = st.number_input("Otros Impuestos (%)", min_value=0.0, max_value=100.0, value=3.0) / 100.0
        
        valor_cif = flete_intl + 20000.0
        duties_calculated = valor_cif * (duty_pct + iva_pct + iva_adicional + other_taxes)
        despacho_total = honorarios + gastos_despacho + digitalizacion + duties_calculated
        st.session_state['despacho_total'] = despacho_total
    else:
        despacho_total = st.session_state.get('despacho_total', 0.0)
        st.markdown(f"""
        <div class="print-card">
            <b>Despacho de Aduana + Impuestos Nacionalización:</b> USD {despacho_total:,.2f}
        </div>
        """, unsafe_allow_html=True)

# Filtrado de Base de Datos
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
    filtered_df['Compra_Formatted'] = filtered_df['Compra'].apply(lambda x: f"USD {x:,.2f}")
    filtered_df['Total_Formatted'] = filtered_df['Total'].apply(lambda x: f"USD {x:,.2f}")
    
    st.dataframe(
        filtered_df[['Concepto', 'Unidad', 'Moneda', 'Compra_Formatted', 'Total_Formatted']].rename(
            columns={'Compra_Formatted': 'Compra', 'Total_Formatted': 'Total'}
        ), 
        use_container_width=True, 
        hide_index=True
    )
    fijos_total = filtered_df['Total'].sum()
else:
    fijos_total = 0.0
    st.info("No se registran cargos fijos adicionales para este perfil.")

# Totales Consolidados y Validez
gran_total = fijos_total + flete_intl + gastos_term + delivery_cost + profit_share + despacho_total
fecha_validez = fecha_cotizacion + timedelta(days=5)

# TOTAL REDISEÑADO COMPACTO ALINEADO A LA DERECHA
st.markdown(f'''
<div class="total-row-container">
    <div class="total-label-text">TOTAL</div>
    <div class="total-price-text">USD {gran_total:,.2f}</div>
</div>
''', unsafe_allow_html=True)

# Cláusulas legales operativas
st.markdown('<div class="section-header">5. Términos Legales y Validez del Servicio</div>', unsafe_allow_html=True)
clausula_final = f"• **VALIDEZ TEMPORAL:** Esta propuesta es válida hasta el **{fecha_validez.strftime('%d/%m/%Y')}** (5 días desde su emisión).\n"
clausula_final += f"• **TRANSPORTE ASIGNADO:** Medio coordinado vía *{nombre_transporte}*.\n"
clausula_final += f"• **CRONOGRAMA ESTIMADO:** ETD: **{etd_date.strftime('%d/%m/%Y')}** | ETA: **{eta_date.strftime('%d/%m/%Y')}**.\n"

if modalidad == "Maritimo":
    clausula_final += f"• **TIEMPOS DE DESTINO:** Transit Time estimado en **{tt_days} días** con un período de **{free_days} días libres** en destino.\n"
if apply_delivery:
    clausula_final += f"• **ENTREGA TERRESTRE:** Delivery programado desde *{del_from}* hasta *{del_to}* por un importe de USD {delivery_cost:,.2f}.\n"
clausula_final += "• **REGULACIONES:** Las cotizaciones están sujetas a variaciones de recargos BAF/CAF por parte de los carriers y espacio disponible al momento de la reserva."

st.markdown(f'<div class="clause-box">{clausula_final.replace("\n", "<br>")}</div>', unsafe_allow_html=True)

# Sección de Impresión Forzada vía Parent Iframe Javascript
st.markdown('<div class="section-header print-section">6. Acciones de Exportación e Impresión</div>', unsafe_allow_html=True)
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
