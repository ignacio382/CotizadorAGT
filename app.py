import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="AGT - Cotizador Multimodal Profesional", page_icon="🌐", layout="wide")

# Estilos visuales con la identidad de AGT optimizados para espacio
st.markdown("""
<style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 8px;
        border-bottom: 2px solid #0B2240;
        margin-bottom: 15px;
    }
    .logo-right { 
        max-width: 220px; /* Logo más chico para ahorrar espacio vertical */
        height: auto; 
        border-radius: 2px; 
    }
    .quote-title-left { 
        font-size: 20px; /* Letra un poco más chica para asegurar una sola línea */
        font-weight: bold; 
        color: #0B2240; 
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.5px;
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
    .print-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px; margin-bottom: 10px; font-size: 13.0px; }
    
    .total-row-container {
        display: flex; justify-content: flex-end; align-items: center; gap: 15px;
        margin-top: 20px; margin-bottom: 20px; padding: 10px 20px;
        background-color: #0B2240; border-radius: 6px; max-width: 400px; margin-left: auto;
    }
    .total-label-text { font-size: 16px; font-weight: bold; color: #ffffff; letter-spacing: 1px; }
    .total-price-text { font-size: 24px; font-weight: bold; color: #FF6B00; }

    @media print {
        .stButton, .stNumberInput, .stSelectbox, .stTextInput, .stDateInput, footer, header, .print-section, iframe, .stCheckbox, div[data-testid="stHeader"], div[data-testid="stSidebar"] { display: none !important; }
        .header-container, .section-header, .clause-box, .print-card, .total-row-container, .logo-right { display: flex !important; }
    }
</style>
""", unsafe_allow_html=True)

# FILTROS DE ESTRUCTURA Y DESTINATARIO INVISIBLE (SIDEBAR)
st.sidebar.markdown("### 👥 Perfil Comercial")
destinatario = st.sidebar.selectbox("Tipo de Destinatario", ["Cliente", "Agente"])
modo_impresion = st.sidebar.checkbox("Activar Modo Vista de Impresión (PDF)", value=False)

# Cabecera optimizada en una sola línea
st.markdown(f"""
<div class="header-container">
    <div class="quote-title-left">COTIZACIÓN DE EMBARQUE</div>
    <div>
        <img class="logo-right" src="https://raw.githubusercontent.com/ignacio382/CotizadorAGT/main/5_2.png" onerror="this.src='https://i.imgur.com/8K59cM2.png'" alt="AGT Logo">
    </div>
</div>
""", unsafe_allow_html=True)

all_incoterms = ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"]

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header">1. Información General</div>', unsafe_allow_html=True)
    if not modo_impresion:
        ref_num = st.text_input("Número de Referencia", value="AGT-2026-4821")
        fecha_cotizacion = st.date_input("Fecha de Emisión", value=datetime.today())
        operacion = st.selectbox("Tipo de Operación", ["Importacion", "Exportacion"])
        incoterm = st.selectbox("Condición de Venta / Incoterm", options=all_incoterms, index=4)
        modalidad = st.selectbox("Vía de Transporte", ["Maritimo", "Aereo", "Terrestre"])
        
        if modalidad == "Aereo": eq_options = ["Aereo"]
        elif modalidad == "Terrestre": eq_options = ["FTL", "LTL"]
        else: eq_options = ["FCL", "LCL"]
        tipo_eq = st.selectbox("Modalidad de Carga", options=eq_options)
        
        container_size = "N/A"
        if modalidad == "Maritimo" and tipo_eq == "FCL":
            container_size = st.selectbox("Modelo del Contenedor (THC)", ["20' Standard", "40' HQ / Standard", "Reefer (RF)"])
            
        cantidad = st.number_input("Cantidad de Unidades (Contenedores/Bultos/CRT)", min_value=1, value=1)
        
        ton_m3 = 1.0
        peso_kg = 0.0
        if tipo_eq == "LCL":
            ton_m3 = st.number_input("Volumen / Toneladas del envío (w/m)", min_value=0.1, value=1.0, step=0.1)
        if modalidad == "Aereo":
            peso_kg = st.number_input("Peso Bruto Tarifado (Kg)", min_value=1.0, value=100.0, step=5.0)

        if modalidad == "Maritimo":
            nombre_transporte = st.text_input("Línea Marítima / Buque", value="Hapag-Lloyd - SAN CLEMENTE V.260W")
            tt_days = st.number_input("Transit Time (Días)", min_value=0, value=14)
            free_days = st.number_input("Días Libres en Destino", min_value=0, value=7)
        elif modalidad == "Aereo":
            nombre_transporte = st.text_input("Línea Aérea / Vuelo", value="Lufthansa - LH511")
            tt_days, free_days = 0, 3
        else:
            nombre_transporte = st.text_input("Empresa Terrestre / Patente", value="Transportes Int. - CTR-765")
            tt_days, free_days = 0, 0
            
        etd_date = st.date_input("Fecha Salida (ETD)", value=datetime.today() + timedelta(days=7))
        eta_date = st.date_input("Fecha Llegada (ETA)", value=datetime.today() + timedelta(days=21))
    else:
        ref_num = st.session_state.get('ref_num', "AGT-2026-4821")
        fecha_cotizacion = st.session_state.get('fecha_cotizacion', datetime.today())
        operacion = st.session_state.get('operacion', "Importacion")
        incoterm = st.session_state.get('incoterm', "DAP")
        modalidad = st.session_state.get('modalidad', "Maritimo")
        tipo_eq = st.session_state.get('tipo_eq', "FCL")
        container_size = st.session_state.get('container_size', "40' HQ / Standard")
        cantidad = st.session_state.get('cantidad', 1)
        ton_m3 = st.session_state.get('ton_m3', 1.0)
        peso_kg = st.session_state.get('peso_kg', 0.0)
        nombre_transporte = st.session_state.get('nombre_transporte', "Hapag-Lloyd - Buque Ficticio")
        etd_date = st.session_state.get('etd_date', datetime.today() + timedelta(days=7))
        eta_date = st.session_state.get('eta_date', datetime.today() + timedelta(days=21))
        tt_days = st.session_state.get('tt_days', 0)
        free_days = st.session_state.get('free_days', 0)
        
        st.markdown(f"""
        <div class="print-card">
            <b>Referencia:</b> {ref_num}<br>
            <b>Fecha Emisión:</b> {fecha_cotizacion.strftime('%d/%m/%Y')}<br>
            <b>Operación:</b> {operacion} | <b>Condición de Venta:</b> {incoterm}<br>
            <b>Vía:</b> {modalidad} ({tipo_eq})<br>
            <b>Equipo/Medida:</b> {container_size if modalidad=='Maritimo' and tipo_eq=='FCL' else f'{ton_m3} w/m' if tipo_eq=='LCL' else f'{peso_kg} Kg' if modalidad=='Aereo' else 'Estandar'} | <b>Cantidad:</b> {cantidad}<br>
            <b>Medio asignado:</b> {nombre_transporte}<br>
            <b>Cronograma:</b> ETD: {etd_date.strftime('%d/%m/%Y')} | ETA: {eta_date.strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-header">2. Tarifas Flotantes y Distribución</div>', unsafe_allow_html=True)
    if not modo_impresion:
        flete_intl = st.number_input("Flete Internacional Base (USD)", min_value=0.0, value=1850.0)
        gastos_term = st.number_input("Gastos Terminal / Depósito (USD)", min_value=0.0, value=650.0)
        apply_delivery = st.checkbox("¿Aplica Flete Interno / Delivery?", value=True)
        
        if apply_delivery:
            del_from = st.text_input("Origen del Flete Local", value="Puerto de Buenos Aires" if modalidad == "Maritimo" else "Aeropuerto de Ezeiza")
            del_to = st.text_input("Destino del Flete Local", value="Planta Industrial del Cliente")
            delivery_cost = st.number_input("Valor del Delivery (USD)", min_value=0.0, value=450.0)
        else:
            delivery_cost, del_from, del_to = 0.0, "N/A", "N/A"
            
        st.session_state['ref_num'] = ref_num
        st.session_state['fecha_cotizacion'] = fecha_cotizacion
        st.session_state['operacion'] = operacion
        st.session_state['incoterm'] = incoterm
        st.session_state['modalidad'] = modalidad
        st.session_state['tipo_eq'] = tipo_eq
        st.session_state['container_size'] = container_size
        st.session_state['cantidad'] = cantidad
        st.session_state['ton_m3'] = ton_m3
        st.session_state['peso_kg'] = peso_kg
        st.session_state['nombre_transporte'] = nombre_transporte
        st.session_state['etd_date'] = etd_date
        st.session_state['eta_date'] = eta_date
        st.session_state['tt_days'] = tt_days
        st.session_state['free_days'] = free_days
        st.session_state['flete_intl'] = flete_intl
        st.session_state['gastos_term'] = gastos_term
        st.session_state['delivery_cost'] = delivery_cost
        st.session_state['apply_delivery'] = apply_delivery
        st.session_state['del_from'] = del_from
        st.session_state['del_to'] = del_to
    else:
        flete_intl = st.session_state.get('flete_intl', 1850.0)
        gastos_term = st.session_state.get('gastos_term', 650.0)
        delivery_cost = st.session_state.get('delivery_cost', 450.0)
        apply_delivery = st.session_state.get('apply_delivery', True)
        del_from = st.session_state.get('del_from', "Puerto de Buenos Aires")
        del_to = st.session_state.get('del_to', "Planta Industrial")
        
        st.markdown(f"""
        <div class="print-card">
            <b>Flete Internacional Base:</b> USD {flete_intl:,.2f}<br>
            <b>Gastos Terminal/Carrier:</b> USD {gastos_term:,.2f}<br>
            <b>Flete Doméstico / Delivery:</b> USD {delivery_cost:,.2f} (Desde {del_from} hasta {del_to})
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

# ----------------- BASE DE DATOS TARIFARIO -----------------
tarifario_AGT = [
    ["Agente", "Maritimo", "Importacion", "FCL", "THC", "x contenedor", 295.00, 335.00, 350.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Toll", "x contenedor", 170.00, 170.00, 170.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Libre deuda", "x contenedor", 95.00, 95.00, 95.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Logistics fee", "x contenedor", 65.00, 65.00, 65.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Limpieza de contenedor", "x contenedor", 25.00, 25.00, 25.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Certificación de flete", "x BL", 45.00, 45.00, 45.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Ingreso SIM", "x BL", 65.00, 65.00, 65.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Forwarding Fee", "x BL", 95.00, 95.00, 95.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "Handling", "x contenedor", 75.00, 75.00, 75.00, False],
    ["Agente", "Maritimo", "Importacion", "FCL", "B/L fee", "x BL", 65.00, 65.00, 65.00, False],

    ["Cliente", "Maritimo", "Importacion", "FCL", "THC", "x contenedor", 295.00, 335.00, 350.00, False],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Toll", "x contenedor", 170.00, 170.00, 170.00, False],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Libre deuda", "x contenedor", 95.00, 95.00, 95.00, True],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Logistics fee", "x contenedor", 65.00, 65.00, 65.00, True],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Limpieza de contenedor", "x contenedor", 25.00, 25.00, 25.00, True],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Certificación de flete (opcional)", "x BL", 45.00, 45.00, 45.00, True],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Ingreso SIM", "x BL", 65.00, 65.00, 65.00, True],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Forwarding Fee", "x BL", 95.00, 95.00, 95.00, True],
    ["Cliente", "Maritimo", "Importacion", "FCL", "Handling", "x contenedor", 75.00, 75.00, 75.00, True],
    ["Cliente", "Maritimo", "Importacion", "FCL", "B/L fee", "x BL", 65.00, 65.00, 65.00, True],

    ["Agente", "Maritimo", "Importacion", "LCL", "Desconsolidación", "tn/m3 min usd 70", 35.00, 35.00, 35.00, False],
    ["Agente", "Maritimo", "Importacion", "LCL", "Logistics fee", "x BL", 20.00, 20.00, 20.00, False],
    ["Agente", "Maritimo", "Importacion", "LCL", "AGP", "tn min usd 4", 4.00, 4.00, 4.00, False],
    ["Agente", "Maritimo", "Importacion", "LCL", "Emisión de BL", "x BL", 35.00, 35.00, 35.00, False],
    ["Agente", "Maritimo", "Importacion", "LCL", "Certificación de flete", "x BL", 45.00, 45.00, 45.00, False],
    ["Agente", "Maritimo", "Importacion", "LCL", "Handling marítima", "x BL", 35.00, 35.00, 35.00, False],
    ["Agente", "Maritimo", "Importacion", "LCL", "Manejo de documentación", "x BL", 95.00, 95.00, 95.00, False],

    ["Cliente", "Maritimo", "Importacion", "LCL", "Desconsolidación", "tn/m3 min usd 70", 35.00, 35.00, 35.00, True],
    ["Cliente", "Maritimo", "Importacion", "LCL", "Logistics fee", "x BL", 20.00, 20.00, 20.00, True],
    ["Cliente", "Maritimo", "Importacion", "LCL", "AGP", "tn min usd 4", 4.00, 4.00, 4.00, True],
    ["Cliente", "Maritimo", "Importacion", "LCL", "Emisión de BL", "x BL", 35.00, 35.00, 35.00, True],
    ["Cliente", "Maritimo", "Importacion", "LCL", "Certificación de flete", "x BL", 45.00, 45.00, 45.00, True],
    ["Cliente", "Maritimo", "Importacion", "LCL", "Handling marítima", "x BL", 35.00, 35.00, 35.00, True],
    ["Cliente", "Maritimo", "Importacion", "LCL", "Manejo de documentación", "x BL", 95.00, 95.00, 95.00, True],

    ["Agente", "Maritimo", "Exportacion", "FCL", "THC", "x contenedor", 295.00, 335.00, 370.00, False],
    ["Agente", "Maritimo", "Exportacion", "FCL", "Toll", "x contenedor", 170.00, 170.00, 170.00, False],
    ["Agente", "Maritimo", "Exportacion", "FCL", "Logistics fee", "x contenedor", 75.00, 75.00, 75.00, False],
    ["Agente", "Maritimo", "Exportacion", "FCL", "Handling marítima/Gate in", "x contenedor", 65.00, 65.00, 65.00, False],
    ["Agente", "Maritimo", "Exportacion", "FCL", "Emisión de BL", "x BL", 75.00, 75.00, 75.00, False],
    ["Agente", "Maritimo", "Exportacion", "FCL", "Manejo de documentación", "x BL", 95.00, 95.00, 95.00, False],
    ["Agente", "Maritimo", "Exportacion", "FCL", "Ingreso SIM", "x BL", 65.00, 65.00, 65.00, False],
    ["Agente", "Maritimo", "Exportacion", "FCL", "Precinto", "x contenedor", 25.00, 25.00, 25.00, False],
    
    ["Cliente", "Maritimo", "Exportacion", "FCL", "THC", "x contenedor", 295.00, 335.00, 370.00, True],
    ["Cliente", "Maritimo", "Exportacion", "FCL", "Toll", "x contenedor", 170.00, 170.00, 170.00, True],
    ["Cliente", "Maritimo", "Exportacion", "FCL", "Logistics fee", "x contenedor", 75.00, 75.00, 75.00, True],
    ["Cliente", "Maritimo", "Exportacion", "FCL", "Handling marítima/Gate in", "x contenedor", 65.00, 65.00, 65.00, True],
    ["Cliente", "Maritimo", "Exportacion", "FCL", "Emisión de BL", "x BL", 75.00, 75.00, 75.00, True],
    ["Cliente", "Maritimo", "Exportacion", "FCL", "Manejo de documentación", "x BL", 95.00, 95.00, 95.00, True],
    ["Cliente", "Maritimo", "Exportacion", "FCL", "Ingreso SIM", "x BL", 65.00, 65.00, 65.00, True],
    ["Cliente", "Maritimo", "Exportacion", "FCL", "Precinto", "x contenedor", 25.00, 25.00, 25.00, True],

    ["Agente", "Maritimo", "Exportacion", "LCL", "Consolidación", "tn/m3 min usd 70", 35.00, 35.00, 35.00, False],
    ["Agente", "Maritimo", "Exportacion", "LCL", "Emisión BL", "x BL", 65.00, 65.00, 65.00, False],
    ["Agente", "Maritimo", "Exportacion", "LCL", "Manejo de documentación", "x BL", 95.00, 95.00, 95.00, False],
    ["Agente", "Maritimo", "Exportacion", "LCL", "Gate", "x BL", 45.00, 45.00, 45.00, False],
    ["Agente", "Maritimo", "Exportacion", "LCL", "VGM", "x BL", 25.00, 25.00, 25.00, False],

    ["Cliente", "Maritimo", "Exportacion", "LCL", "Consolidación", "tn/m3 min usd 70", 35.00, 35.00, 35.00, True],
    ["Cliente", "Maritimo", "Exportacion", "LCL", "Emisión BL", "x BL", 65.00, 65.00, 65.00, True],
    ["Cliente", "Maritimo", "Exportacion", "LCL", "Manejo de documentación", "x BL", 95.00, 95.00, 95.00, True],
    ["Cliente", "Maritimo", "Exportacion", "LCL", "Gate", "x BL", 45.00, 45.00, 45.00, True],
    ["Cliente", "Maritimo", "Exportacion", "LCL", "VGM", "x BL", 25.00, 25.00, 25.00, True],

    ["Agente", "Aereo", "Importacion", "Aereo", "Res. 3244/11", "x guía/parcial", 20.00, 20.00, 20.00, False],
    ["Agente", "Aereo", "Importacion", "Aereo", "Desconsolidación", "x bulto min usd 20", 0.50, 0.50, 0.50, False],
    ["Agente", "Aereo", "Importacion", "Aereo", "IATA Collection fee", "3% s/AWB min usd 50", 0.03, 0.03, 0.03, False],
    ["Agente", "Aereo", "Importacion", "Aereo", "Handling aerolínea", "x guía", 210.00, 210.00, 210.00, False],
    ["Agente", "Aereo", "Importacion", "Aereo", "Manejo de documentación", "x guía", 95.00, 95.00, 95.00, False],
    ["Agente", "Aereo", "Importacion", "Aereo", "Carga DGR (en caso de aplicar)", "x guía (MIN)", 180.00, 180.00, 180.00, False],

    ["Cliente", "Aereo", "Importacion", "Aereo", "Res. 3244/11", "x guía/parcial", 20.00, 20.00, 20.00, False],
    ["Cliente", "Aereo", "Importacion", "Aereo", "Desconsolidación", "x bulto min usd 20", 0.50, 0.50, 0.50, True],
    ["Cliente", "Aereo", "Importacion", "Aereo", "IATA Collection fee", "3% s/AWB min usd 50", 0.03, 0.03, 0.03, False],
    ["Cliente", "Aereo", "Importacion", "Aereo", "Handling aerolínea", "x guía", 210.00, 210.00, 210.00, True],
    ["Cliente", "Aereo", "Importacion", "Aereo", "Manejo de documentación", "x guía", 95.00, 95.00, 95.00, True],
    ["Cliente", "Aereo", "Importacion", "Aereo", "Carga DGR (en caso de aplicar)", "x guía (MIN)", 180.00, 180.00, 180.00, True],

    ["Agente", "Aereo", "Exportacion", "Aereo", "TCA*", "x guía min usd 20", 0.02, 0.02, 0.02, False],
    ["Agente", "Aereo", "Exportacion", "Aereo", "Emisión de AWB", "x guía", 35.00, 35.00, 35.00, False],
    ["Agente", "Aereo", "Exportacion", "Aereo", "Manejo de documentación", "x guía", 95.00, 95.00, 95.00, False],
    ["Agente", "Aereo", "Exportacion", "Aereo", "Carga DGR (si aplica)", "x guía (MIN)", 180.00, 180.00, 180.00, False],

    ["Cliente", "Aereo", "Exportacion", "Aereo", "Res. 3244/11", "x guía/parcial", 20.00, 20.00, 20.00, False],
    ["Cliente", "Aereo", "Exportacion", "Aereo", "TCA*", "x guía min usd 20", 0.02, 0.02, 0.02, True],
    ["Cliente", "Aereo", "Exportacion", "Aereo", "Emisión de AWB", "x guía", 35.00, 35.00, 35.00, True],
    ["Cliente", "Aereo", "Exportacion", "Aereo", "Manejo de documentación", "x guía", 95.00, 95.00, 95.00, True],
    ["Cliente", "Aereo", "Exportacion", "Aereo", "Carga DGR (si aplica)", "x guía (MIN)", 180.00, 180.00, 180.00, True],

    ["Agente", "Terrestre", "Importacion", "FTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, False],
    ["Agente", "Terrestre", "Importacion", "FTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, False],
    ["Agente", "Terrestre", "Importacion", "LTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, False],
    ["Agente", "Terrestre", "Importacion", "LTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, False],
    ["Agente", "Terrestre", "Exportacion", "FTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, False],
    ["Agente", "Terrestre", "Exportacion", "FTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, False],
    ["Agente", "Terrestre", "Exportacion", "LTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, False],
    ["Agente", "Terrestre", "Exportacion", "LTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, False],

    ["Cliente", "Terrestre", "Importacion", "FTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, True],
    ["Cliente", "Terrestre", "Importacion", "FTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, True],
    ["Cliente", "Terrestre", "Importacion", "LTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, True],
    ["Cliente", "Terrestre", "Importacion", "LTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, True],
    ["Cliente", "Terrestre", "Exportacion", "FTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, True],
    ["Cliente", "Terrestre", "Exportacion", "FTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, True],
    ["Cliente", "Terrestre", "Exportacion", "LTL", "Manejo de documentación", "x CRT", 125.00, 125.00, 125.00, True],
    ["Cliente", "Terrestre", "Exportacion", "LTL", "Emisión de CRT", "x CRT", 25.00, 25.00, 25.00, True],
]

df_base = pd.DataFrame(tarifario_AGT, columns=["Destinatario", "Modalidad", "Operacion", "TipoEquipamiento", "Concepto", "UnidadBase", "Precio20", "Precio40", "PrecioRF", "AplicaIVA"])

filtered_df = df_base[
    (df_base['Destinatario'] == destinatario) & 
    (df_base['Modalidad'] == modalidad) & 
    (df_base['Operacion'] == operacion) & 
    (df_base['TipoEquipamiento'] == tipo_eq)
].copy()

fijos_total = 0.0
fijos_iva = 0.0
rows_to_render = []

if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        concepto = row['Concepto']
        unidad = row['UnidadBase']
        
        precio_base = row['Precio20']
        if modalidad == "Maritimo" and tipo_eq == "FCL":
            if container_size == "40' HQ / Standard": precio_base = row['Precio40']
            elif container_size == "Reefer (RF)": precio_base = row['PrecioRF']
            
        subtotal_item = precio_base * cantidad
        
        if "tn/m3 min usd 70" in unidad:
            calculo_wm = precio_base * ton_m3 * cantidad
            subtotal_item = max(70.0 * cantidad, calculo_wm)
        elif "tn min usd 4" in unidad:
            calculo_agp = precio_base * ton_m3 * cantidad
            subtotal_item = max(4.0 * cantidad, calculo_agp)
        elif "x bulto min usd 20" in unidad:
            calculo_aereo = precio_base * cantidad
            subtotal_item = max(20.0, calculo_aereo)
        elif "3% s/AWB min usd 50" in unidad:
            subtotal_item = max(50.0, flete_intl * 0.03)
        elif "x guía min usd 20" in unidad:
            calculo_tca = (0.02 * peso_kg + 10) * cantidad
            subtotal_item = max(20.0 * cantidad, calculo_tca)
            
        iva_item = subtotal_item * 0.21 if row['AplicaIVA'] else 0.0
        
        fijos_total += subtotal_item
        fijos_iva += iva_item
        
        rows_to_render.append({
            "Concepto": concepto,
            "Unidad": unidad,
            "Moneda": "USD",
            "Tarifa Base": f"USD {precio_base:,.2f}",
            "Subtotal": f"USD {subtotal_item:,.2f}",
            "IVA (21%)": f"USD {iva_item:,.2f}" if row['AplicaIVA'] else "Exento"
        })

# Título de sección simplificado
st.markdown('<div class="section-header">4. Conceptos Fijos Loces</div>', unsafe_allow_html=True)
if rows_to_render:
    st.dataframe(pd.DataFrame(rows_to_render), use_container_width=True, hide_index=True)
else:
    st.info("No se registran cargos fijos adicionales parametrizados para este perfil.")

# Totales Consolidados finales
gran_total = fijos_total + fijos_iva + flete_intl + gastos_term + delivery_cost
fecha_validez = fecha_cotizacion + timedelta(days=5)

# TOTAL REDISEÑADO COMPACTO ALINEADO A LA DERECHA
st.markdown(f'''
<div class="total-row-container">
    <div class="total-label-text">TOTAL {"+ IVA" if destinatario=="Cliente" else ""}</div>
    <div class="total-price-text">USD {gran_total:,.2f}</div>
</div>
''', unsafe_allow_html=True)

# Cláusulas legales operativas
st.markdown('<div class="section-header">5. Términos Legales y Validez del Servicio</div>', unsafe_allow_html=True)
clausula_final = f"• **VALIDEZ TEMPORAL:** Esta propuesta es válida hasta el **{fecha_validez.strftime('%d/%m/%Y')}** (5 días desde su emisión).\n"
clausula_final += f"• **TRANSPORTE ASIGNADO:** Medio coordinado vía *{nombre_transporte}*.\n"
clausula_final += f"• **CRONOGRAMA ESTIMADO:** ETD: **{etd_date.strftime('%d/%m/%Y')}** | ETA: **{eta_date.strftime('%d/%m/%Y')}**.\n"

if modalidad == "Maritimo":
    clausula_final += f"• **TIEMPOS DE DESTINO:** Transit Time estimado en **{st.session_state.get('tt_days', 14)} días** con un período de **{st.session_state.get('free_days', 7)} días libres** en destino.\n"
if apply_delivery:
    clausula_final += f"• **ENTREGA TERRESTRE:** Delivery programado desde *{st.session_state.get('del_from', 'Origen')}* hasta *{st.session_state.get('del_to', 'Destino')}* por un importe de USD {delivery_cost:,.2f}.\n"
clausula_final += "• **REGULACIONES:** Las cotizaciones están sujetas a variaciones de recargos BAF/CAF por parte de los carriers y espacio disponible al momento de la reserva."

st.markdown('<div class="clause-box">' + clausula_final.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)

# SECCIÓN DE BOTÓN DIRECTO SIN TÍTULOS REPETITIVOS
components.html(
    """
    <style>
        .print-btn {
            background-color: #FF6B00; color: white; border: none; padding: 12px 24px;
            border-radius: 4px; cursor: pointer; font-size: 15px; font-family: 'Segoe UI', sans-serif;
            font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%;
        }
        .print-btn:hover { background-color: #e05e00; }
    </style>
    <button class="print-btn" onclick="window.parent.print()">🖨️ Imprimir Cotización / Guardar en PDF</button>
    """,
    height=60,
)
