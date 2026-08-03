import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="AGT - Cotizador Multimodal Profesional", page_icon="🌐", layout="wide")

# Estilos visuales con la identidad de AGT optimizados para pantalla e impresión directa legible
st.markdown("""
<style>
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
        max-width: 180px; 
        height: auto; 
        border-radius: 2px; 
    }
    .quote-title-left { 
        font-size: 18px; 
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
    .print-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px; margin-bottom: 10px; font-size: 13.0px; }
    
    .total-row-container {
        display: flex; justify-content: flex-end; align-items: center; gap: 15px;
        margin-top: 20px; margin-bottom: 20px; padding: 10px 20px;
        background-color: #0B2240; border-radius: 6px; max-width: 400px; margin-left: auto;
    }
    .total-label-text { font-size: 16px; font-weight: bold; color: #ffffff; letter-spacing: 1px; }
    .total-price-text { font-size: 24px; font-weight: bold; color: #FF6B00; }

    /* REGLAS DE IMPRESIÓN DIRECTA ULTRA COMPACTA Y SIN RECUADROS */
    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], footer, header, .print-section, iframe, .stCheckbox, 
        button, .step-up, .step-down, div[data-testid="stInputNumber-StepUp"], div[data-testid="stInputNumber-StepDown"] { 
            display: none !important; 
        }
        
        @page {
            margin: 0.6cm !important;
        }
        
        div[data-testid="stBlock"], div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"], .stWidget {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            gap: 0 !important;
        }

        .element-container {
            margin-bottom: 1px !important;
            padding-bottom: 1px !important;
        }
        
        body, p, div, span, td, th {
            font-size: 11.5pt !important; 
            color: #111111 !important;
            font-family: 'Segoe UI', Arial, sans-serif !important;
        }
        
        input, select, textarea, div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput div, .stNumberInput div {
            border: none !important;
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            font-size: 11.5pt !important;
            font-weight: bold !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        div[data-baseweb="select"] button, div[role="button"] {
            display: none !important;
        }
        
        .header-container { 
            display: flex !important; 
            justify-content: space-between !important;
            align-items: center !important;
            border-bottom: 2px solid #0B2240 !important; 
            margin-bottom: 10px !important; 
            padding-bottom: 6px !important;
        }
        .logo-right { 
            display: block !important; 
            max-width: 180px !important; 
            height: auto !important;
        }
        .quote-title-left { display: block !important; font-size: 18pt !important; }
        .section-header { display: flex !important; border-left: 5px solid #FF6B00 !important; font-size: 12pt !important; margin-top: 8px !important; margin-bottom: 4px !important; }
        .clause-box { display: block !important; background-color: #FFFDF5 !important; border: 1px solid #FFEBAA !important; padding: 8px !important; }
        .total-row-container { display: flex !important; background-color: #0B2240 !important; padding: 8px 15px !important; margin-top: 10px !important; }
        .total-price-text { color: #FF6B00 !important; font-size: 18pt !important; }
    }
</style>
""", unsafe_allow_html=True)

# FILTRO INVISIBLE DE PERFIL COMERCIAL (SOLO EN SIDEBAR)
st.sidebar.markdown("### 👥 Perfil Comercial")
destinatario = st.sidebar.selectbox("Tipo de Destinatario", ["Cliente", "Agente"])

# Cabecera
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

with col2:
    st.markdown('<div class="section-header">2. Tarifas</div>', unsafe_allow_html=True)
    flete_intl = st.number_input("Flete Internacional Base (USD)", min_value=0.0, value=1850.0)
    gastos_term = st.number_input("Gastos Terminal / Depósito (USD)", min_value=0.0, value=650.0)
    apply_delivery = st.checkbox("¿Aplica Flete Interno / Delivery?", value=True)
    
    if apply_delivery:
        del_from = st.text_input("Origen del Flete Local", value="Puerto de Buenos Aires" if modalidad == "Maritimo" else "Aeropuerto de Ezeiza")
        del_to = st.text_input("Destino del Flete Local", value="Planta Industrial del Cliente")
        delivery_cost = st.number_input("Valor del Delivery (USD)", min_value=0.0, value=450.0)
    else:
        delivery_cost, del_from, del_to = 0.0, "N/A", "N/A"

    # MÓDULO INTERACTIVO DE CUSTOMS BROKER & TAXES
    st.markdown('<div class="section-header">3. Servicios de Aduana</div>', unsafe_allow_html=True)
    apply_broker = st.checkbox("¿Aplica Customs Broker?", value=False)
    
    broker_cost = 0.0
    pa_code = "N/A"
    apply_taxes = False
    
    if apply_broker:
        pa_code = st.text_input("HS Code / PA", value="8471.30.12")
        label_valor = "Valor FOB de la Mercadería (USD)" if operacion == "Exportacion" else "Valor CIF de la Mercadería (USD)"
        valor_mercaderia = st.number_input(label_valor, min_value=0.0, value=25000.0, step=1000.0)
        
        honorarios_calculados = valor_mercaderia * 0.007
        honorarios_finales = max(275.0, honorarios_calculados)
        gastos_despacho_fijos = 150.0
        digitalizacion_fija = 65.0
        
        broker_total_item = honorarios_finales + gastos_despacho_fijos + digitalizacion_fija
        broker_cost = broker_total_item
        
        tipo_honorario_lbl = "0.7% Valor FOB (Min 275)" if operacion == "Exportacion" else "0.7% Valor CIF (Min 275)"
        st.caption(f"📋 **Despacho:** Hon: USD {honorarios_finales:,.2f} | Gastos: USD 150.00 | Dig: USD 65.00")
        
        apply_taxes = st.checkbox("¿Aplica liquidación de Duties & Taxes?", value=False)
        if apply_taxes:
            st.markdown("**Duties & Taxes (Campos de entrada libres):**")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                input_duty = st.number_input("Duty / Arancel (%)", min_value=0.0, value=16.0, step=0.5)
                input_vat = st.number_input("VAT / IVA (%)", min_value=0.0, value=10.5, step=0.5)
            with col_t2:
                input_add_vat = st.number_input("Additional VAT (%)", min_value=0.0, value=10.0, step=0.5)
                input_other = st.number_input("Other taxes (%)", min_value=0.0, value=8.5, step=0.5)
            
            tax_duty = valor_mercaderia * (input_duty / 100)
            tax_vat = valor_mercaderia * (input_vat / 100)
            tax_add_vat = valor_mercaderia * (input_add_vat / 100)
            tax_other = valor_mercaderia * (input_other / 100)
            
            st.caption(f"💵 **Duties & Taxes Informativo:** USD {(tax_duty + tax_vat + tax_add_vat + tax_other):,.2f} (No se incluirá en el total)")

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

# CÁLCULOS OPERATIVOS
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
            subtotal_item = max(70.0 * cantidad, precio_base * ton_m3 * cantidad)
        elif "tn min usd 4" in unidad:
            subtotal_item = max(4.0 * cantidad, precio_base * ton_m3 * cantidad)
        elif "x bulto min usd 20" in unidad:
            subtotal_item = max(20.0, precio_base * cantidad)
        elif "3% s/AWB min usd 50" in unidad:
            subtotal_item = max(50.0, flete_intl * 0.03)
        elif "x guía min usd 20" in unidad:
            subtotal_item = max(20.0 * cantidad, (0.02 * peso_kg + 10) * cantidad)
            
        iva_item = subtotal_item * 0.21 if row['AplicaIVA'] else 0.0
        fijos_total += subtotal_item
        fijos_iva += iva_item
        
        rows_to_render.append({
            "Concepto": concepto, "Unidad": unidad, "Moneda": "USD",
            "Tarifa Base": f"USD {precio_base:,.2f}", "Subtotal": f"USD {subtotal_item:,.2f}",
            "IVA (21%)": f"USD {iva_item:,.2f}" if row['AplicaIVA'] else "Exento"
        })

if apply_broker:
    tipo_h_lbl = "0.7% FOB (Min 275)" if operacion == "Exportacion" else "0.7% CIF (Min 275)"
    rows_to_render.append({"Concepto": "Hon. Despacho", "Unidad": tipo_h_lbl, "Moneda": "USD", "Tarifa Base": "Variable", "Subtotal": f"USD {max(275.0, valor_mercaderia*0.007):,.2f}", "IVA (21%)": "Exento"})
    rows_to_render.append({"Concepto": "Gastos de despacho", "Unidad": "x Operación", "Moneda": "USD", "Tarifa Base": "USD 150.00", "Subtotal": "USD 150.00", "IVA (21%)": "Exento"})
    rows_to_render.append({"Concepto": "Digitalización", "Unidad": "x Operación", "Moneda": "USD", "Tarifa Base": "USD 65.00", "Subtotal": "USD 65.00", "IVA (21%)": "Exento"})

st.markdown('<div class="section-header">4. Conceptos Fijos Locales</div>', unsafe_allow_html=True)
if rows_to_render:
    st.dataframe(pd.DataFrame(rows_to_render), use_container_width=True, hide_index=True)
else:
    st.info("No se registran cargos fijos adicionales parametrizados para este perfil.")

# El total final contempla fijos, flete, terminal y distribución; Duties & Taxes NO se suman al total a demanda del usuario
gran_total = fijos_total + fijos_iva + flete_intl + gastos_term + delivery_cost + broker_cost
fecha_validez = fecha_cotizacion + timedelta(days=5)

st.markdown(f'''
<div class="total-row-container">
    <div class="total-label-text">TOTAL</div>
    <div class="total-price-text">USD {gran_total:,.2f}</div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="section-header">5. Términos Legales y Validez del Servicio</div>', unsafe_allow_html=True)

clausula_final = f"VALIDEZ TEMPORAL: Esta propuesta es válida hasta el {fecha_validez.strftime('%d/%m/%Y')} (5 días desde su emisión).<br>"
clausula_final += f"TRANSPORTE ASIGNADO: Medio coordinado vía {nombre_transporte}.<br>"
clausula_final += f"CRONOGRAMA ESTIMADO: ETD: {etd_date.strftime('%d/%m/%Y')} | ETA: {eta_date.strftime('%d/%m/%Y')}.<br>"

if modalidad == "Maritimo":
    clausula_final += f"TIEMPOS DE DESTINO: Transit Time estimado en {tt_days} días con un período de {free_days} días libres en destino.<br>"
if apply_delivery:
    clausula_final += f"ENTREGA TERRESTRE: Delivery programado desde {del_from} hasta {del_to} por un importe de USD {delivery_cost:,.2f}.<br>"
if apply_broker:
    clausula_final += f"DESPACHO DE ADUANA: Coordinado bajo modalidad {operacion} por cuenta de AGT Broker (Posición Arancelaria: {pa_code}).<br>"

# Inyección condicional de la cláusula tributaria protectora
if apply_broker and apply_taxes:
    clausula_final += "IMPUESTOS: Duties and taxes no incluidos en la cotización comercial.<br>"

clausula_final += "REGULACIONES: Las cotizaciones están sujetas a variaciones de recargos BAF/CAF por parte de los carriers y espacio disponible al momento de la reserva."

st.markdown(f'<div class="clause-box">{clausula_final}</div>', unsafe_allow_html=True)

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
