
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AGT - Cotizador Inteligente", page_icon="✈️", layout="wide")

# Custom CSS for Brand Identity
st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: bold; color: #0B2240; }
    .subtitle { font-size: 14px; color: #FF6B00; font-style: italic; font-weight: bold; margin-bottom: 25px;}
    .section-header { font-size: 18px; font-weight: bold; color: #0B2240; border-left: 4px solid #FF6B00; padding-left: 8px; margin-top: 20px; margin-bottom: 15px;}
    .total-box { background-color: #0B2240; color: white; padding: 20px; border-radius: 6px; text-align: center; }
    .total-amount { font-size: 30px; font-weight: bold; color: #FF6B00; }
    .clause-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 4px; font-size: 13px; color: #333333; }
</style>
""", unsafe_allow_html=True)

# Application Data Base Setup
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
    ["DAP", "Maritimo", "Importacion", "LCL", "Desconociliación", "TN/M3 Min USD 70", "USD", 35.00],
    ["DAP", "Maritimo", "Importacion", "LCL", "Logistics fee", "Por BL", "USD", 20.00],
    ["DAP", "Maritimo", "Importacion", "LCL", "AGP", "TN Min USD 4", "USD", 4.00],
    ["DAP", "Maritimo", "Importacion", "LCL", "Emisión de BL", "Por BL", "USD", 35.00],
    ["DAP", "Maritimo", "Importacion", "LCL", "Certificación de flete", "Por BL", "USD", 45.00],
    ["DAP", "Maritimo", "Importacion", "LCL", "Handling marítima", "Por BL", "USD", 35.00],
    ["DAP", "Maritimo", "Importacion", "LCL", "Manejo de documentación", "Por BL", "USD", 95.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Res. 3244/11", "Por Awb parcial", "USD", 20.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Desconsolidación", "Por Bulto Min. USD 20", "USD", 0.50],
    ["DAP", "Aereo", "Importacion", "Aereo", "Handling aerolínea", "Por AWB", "USD", 210.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Manejo de documentación", "Por AWB", "USD", 95.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Carga DGR (si aplica)", "Por Awb (MIN)", "USD", 180.00],
    ["DAP", "Aereo", "Importacion", "Aereo", "Transfer fee (if necessary)", "5%, Min. USD 150", "USD", 150.00],
    ["DDP", "Aereo", "Importacion", "Aereo", "Res. 3244/11", "Por Awb parcial", "USD", 20.00],
    ["DDP", "Aereo", "Importacion", "Aereo", "Desconsolidación", "Por Bulto Min. USD 20", "USD", 0.50],
    ["DDP", "Aereo", "Importacion", "Aereo", "Handling aerolínea", "Por AWB", "USD", 210.00],
    ["DDP", "Aereo", "Importacion", "Aereo", "Manejo de documentación", "Por AWB", "USD", 95.00],
    ["DDP", "Aereo", "Importacion", "Aereo", "Carga DGR (si aplica)", "Por Awb (MIN)", "USD", 180.00],
    ["DDP", "Aereo", "Importacion", "Aereo", "Transfer fee (if necessary)", "5%, Min. USD 150", "USD", 150.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "THC 20'", "Por Contenedor", "USD", 295.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "THC 40'", "Por Contenedor", "USD", 335.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "THC RF", "Por Contenedor", "USD", 350.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Toll", "Por Contenedor", "USD", 170.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Libre deuda", "Por Contenedor", "USD", 95.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Logistics fee", "Por Contenedor", "USD", 65.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Limpieza de contenedor", "Por Contenedor", "USD", 25.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Certificación de flete (opcional)", "Por BL", "USD", 45.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Ingreso SIM", "Por BL", "USD", 65.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Forwarding Fee", "Por BL", "USD", 95.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Handling", "Por Contenedor", "USD", 75.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "B/L Fee", "x BL", "USD", 65.00],
    ["DDP", "Maritimo", "Importacion", "FCL", "Comisión bancaria (si aplica)", "5%, Min. USD 150", "USD", 150.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "Desconsolidación", "TN/M3 Min USD 70", "USD", 35.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "Logistics fee", "Por BL", "USD", 20.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "AGP", "TN Min USD 4", "USD", 4.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "Emisión de BL (Opcional)", "Por BL", "USD", 35.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "Certificación de flete (Opcional)", "Por BL", "USD", 45.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "Handling marítima", "Por BL", "USD", 35.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "Manejo de documentación", "Por BL", "USD", 95.00],
    ["DDP", "Maritimo", "Importacion", "LCL", "Comisión bancaria (si aplica)", "5%, Min. USD 150", "USD", 150.00],
    ["DDU", "Aereo", "Importacion", "Aereo", "Res. 3244/11", "Por Awb parcial", "USD", 20.00],
    ["DDU", "Aereo", "Importacion", "Aereo", "Desconsolidación", "Por Bulto Min. USD 20", "USD", 0.50],
    ["DDU", "Aereo", "Importacion", "Aereo", "Handling aerolínea", "Por AWB", "USD", 210.00],
    ["DDU", "Aereo", "Importacion", "Aereo", "Manejo de documentación", "Por AWB", "USD", 95.00],
    ["DDU", "Aereo", "Importacion", "Aereo", "Carga DGR (si aplica)", "Por Awb (MIN)", "USD", 180.00],
    ["DDU", "Aereo", "Importacion", "Aereo", "Transfer fee (if necessary)", "5%, Min. USD 150", "USD", 150.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "THC 20'", "Por Contenedor", "USD", 295.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "THC 40'", "Por Contenedor", "USD", 335.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "THC RF", "Por Contenedor", "USD", 350.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Toll", "Por Contenedor", "USD", 170.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Libre deuda", "Por Contenedor", "USD", 95.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Logistics fee", "Por Contenedor", "USD", 65.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Limpieza de contenedor", "Por Contenedor", "USD", 25.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Certificación de flete", "Por BL", "USD", 45.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Ingreso SIM", "Por BL", "USD", 65.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Forwarding Fee", "Por BL", "USD", 95.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "Handling", "Por Contenedor", "USD", 75.00],
    ["DDU", "Maritimo", "Importacion", "FCL", "B/L Fee", "Por BL", "USD", 65.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "THC 20'", "Por Contenedor", "USD", 295.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "THC 40'", "Por Contenedor", "USD", 335.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "THC RF", "Por Contenedor", "USD", 370.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "Toll", "Por Contenedor", "USD", 170.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "Logistics fee", "Por Contenedor", "USD", 75.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "Handling marítima/Gate in", "Por Contenedor", "USD", 65.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "Emisión de BL", "Por BL", "USD", 75.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "Manejo de documentación", "Por BL", "USD", 95.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "Ingreso SIM", "Por BL", "USD", 65.00],
    ["EXW", "Maritimo", "Exportacion", "FCL", "Precinto", "Por Contenedor", "USD", 25.00],
    ["EXW", "Maritimo", "Exportacion", "LCL", "Consolidación", "TN/M3 Min USD 70", "USD", 35.00],
    ["EXW", "Maritimo", "Exportacion", "LCL", "Emisión BL", "Por BL", "USD", 65.00],
    ["EXW", "Maritimo", "Exportacion", "LCL", "Manejo de documentación", "Por BL", "USD", 95.00],
    ["EXW", "Maritimo", "Exportacion", "LCL", "Gate", "Por BL", "USD", 45.00],
    ["EXW", "Maritimo", "Exportacion", "LCL", "VGM", "Por BL", "USD", 25.00],
    ["EXW", "Aereo", "Exportacion", "Aereo", "Res. 3244/11", "Por Awb parcial", "USD", 20.00],
    ["EXW", "Aereo", "Exportacion", "Aereo", "TCA*", "s/AWB Min. USD 20", "USD", 20.00],
    ["EXW", "Aereo", "Exportacion", "Aereo", "Emisión de AWB", "Por AWB", "USD", 35.00],
    ["EXW", "Aereo", "Exportacion", "Aereo", "Manejo de documentación", "Por AWB", "USD", 95.00],
    ["EXW", "Aereo", "Exportacion", "Aereo", "Carga DGR (si aplica)", "Por Awb (MIN)", "USD", 180.00],
    ["FCA", "Aereo", "Exportacion", "Aereo", "Res. 3244/11", "Por Awb parcial", "USD", 20.00],
    ["FCA", "Aereo", "Exportacion", "Aereo", "TCA*", "s/AWB Min. USD 20", "USD", 20.00],
    ["FCA", "Aereo", "Exportacion", "Aereo", "Emisión de AWB", "Por AWB", "USD", 35.00],
    ["FCA", "Aereo", "Exportacion", "Aereo", "Manejo de documentación", "Por AWB", "USD", 95.00],
    ["FCA", "Aereo", "Exportacion", "Aereo", "Carga DGR (si aplica)", "Por Awb (MIN)", "USD", 180.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "THC 20'", "Por Contenedor", "USD", 295.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "THC 40'", "Por Contenedor", "USD", 335.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "THC RF", "Por Contenedor", "USD", 370.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "Toll", "Por Contenedor", "USD", 170.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "Logistics fee", "Por Contenedor", "USD", 75.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "Handling marítima/Gate in", "Por Contenedor", "USD", 65.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "Emisión de BL", "Por BL", "USD", 75.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "Manejo de documentación", "Por BL", "USD", 95.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "Ingreso SIM", "Por BL", "USD", 65.00],
    ["FCA", "Maritimo", "Exportacion", "FCL", "Precinto", "Por Contenedor", "USD", 25.00],
    ["FCA", "Maritimo", "Exportacion", "LCL", "Consolidación", "TN/M3 Min USD 70", "USD", 35.00],
    ["FCA", "Maritimo", "Exportacion", "LCL", "Emisión BL", "Por BL", "USD", 65.00],
    ["FCA", "Maritimo", "Exportacion", "LCL", "Manejo de documentación", "Por BL", "USD", 95.00],
    ["FCA", "Maritimo", "Exportacion", "LCL", "Gate", "Por BL", "USD", 45.00],
    ["FCA", "Maritimo", "Exportacion", "LCL", "VGM", "Por BL", "USD", 25.00]
]

df = pd.DataFrame(raw_data, columns=["Incoterm", "Modalidad", "Operacion", "Tipo", "Concepto", "Unidad", "Moneda", "Compra"])

# Header UI
st.markdown('<div class="main-title">AGT - ARGENTINA GLOBAL TRADE SRL</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">FORWARDER & LOGÍSTICA INTERNACIONAL - COTIZADOR INTERACTIVO</div>', unsafe_allow_html=True)

# Main Grid Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header">1. Filtros y Parámetros Operativos</div>', unsafe_allow_html=True)
    
    ref_num = st.text_input("Número de Cotización (Correlativo)", value="AGT-2026-0943")
    
    incoterm = st.selectbox("Incoterm", options=sorted(list(set(df['Incoterm'].tolist())) + ["FOB"]))
    modalidad = st.selectbox("Modalidad de Transporte", options=list(set(df['Modalidad'].tolist())))
    operacion = st.selectbox("Tipo de Operación", options=list(set(df['Operacion'].tolist())))
    tipo = st.selectbox("Tipo / Equipamiento", options=["FCL", "LCL", "Aereo"])
    
    cantidad = st.number_input("Cantidad de Contenedores / Bultos", min_value=1, value=1)
    peso = st.number_input("Peso Total (Kg)", min_value=0.0, value=42.0)
    volumen = st.number_input("Volumen Total (M3)", min_value=0.0, value=0.5)

with col2:
    st.markdown('<div class="section-header">2. Fletes y Costos Variables (A completar)</div>', unsafe_allow_html=True)
    
    flete_intl = st.number_input("Flete Internacional Base (USD)", min_value=0.0, value=1250.0)
    gastos_term = st.number_input("Gastos de Terminal Portuaria / Aérea (USD)", min_value=0.0, value=650.0)
    delivery_cost = st.number_input("Costo de Delivery / Pick Up (USD)", min_value=0.0, value=250.0)
    seguro = st.number_input("Seguro Obligatorio (USD)", min_value=0.0, value=80.0)
    honorarios = st.number_input("Honorarios Despachante Aduana (USD)", min_value=0.0, value=150.0)
    profit = st.number_input("Profit Share Compartido Mínimo (USD)", min_value=0.0, value=50.0)

# Filter database items based on user inputs
filtered_df = df[
    (df['Incoterm'] == incoterm) & 
    (df['Modalidad'] == modalidad) & 
    (df['Tipo'] == tipo)
].copy()

st.markdown('<div class="section-header">3. Conceptos Fijos Automáticos (Desde Base de Datos)</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    filtered_df['Total Concepto'] = filtered_df['Compra'] * cantidad
    st.dataframe(filtered_df[['Concepto', 'Unidad', 'Moneda', 'Compra', 'Total Concepto']], use_container_width=True)
    fijos_total = filtered_df['Total Concepto'].sum()
else:
    st.info("No se registran conceptos fijos automáticos específicos para este Incoterm/Modalidad en la Base de Datos. Se utilizarán exclusivamente variables.")
    fijos_total = 0.0

# Summary block calculations
total_general = fijos_total + flete_intl + gastos_term + delivery_cost + seguro + honorarios + profit

st.markdown('<div class="section-header">4. Resumen y Totalización Financiera</div>', unsafe_allow_html=True)
c_t1, c_t2, c_t3 = st.columns(3)
c_t1.metric("Total Conceptos Fijos", f"USD {fijos_total:,.2f}")
c_t2.metric("Total Costos Variables", f"USD {(flete_intl + gastos_term + delivery_cost + seguro + honorarios + profit):,.2f}")

with c_t3:
    st.markdown(f'''
    <div class="total-box">
        Total Cotización ({ref_num})<br>
        <span class="total-amount">USD {total_general:,.2f}</span>
    </div>
    ''', unsafe_allow_html=True)

# Clause & notes text processing block based on Incoterm selection
st.markdown('<div class="section-header">5. Cláusulas y Observaciones Específicas del Incoterm</div>', unsafe_allow_html=True)

clauses = "• **VÁLIDO SÓLO PARA CARGA GENERAL**\n• **SUJETO A DISPONIBILIDAD Y ESPACIO EN BODEGA**\n"

if incoterm in ["CFR", "FOB"]:
    clauses += "• Flete bajo condición *Collect.\n• **NO INCLUIDO EL DESPACHO ADUANERO**. Usualmente los exportadores cuentan con sus propios despachantes.\n• Tarifas NET/NET por favor considere nuestro profit share."
elif incoterm == "DAP" and modalidad == "Aereo":
    clauses += f"• DELIVERY: USD {delivery_cost} (0.6% ad valorem obligatorio, MIN USD 80).\n• Desde Aeropuerto de Ezeiza.\n• No incluye gastos de terminal aérea por almacenamiento/manipuleo diario."
elif incoterm == "DAP" and modalidad == "Maritimo":
    clauses += f"• Gastos de terminal portuaria: USD {gastos_term} cobrado al costo en caso de no ser pagado por el consignee.\n• Unstuffing: N/A (Debería ser pagado por consignee).\n• DELIVERY: USD {delivery_cost} desde Puerto de Buenos Aires."
elif incoterm in ["DDU", "DDP"]:
    clauses += "• Aduana en Argentina posee regulaciones especiales muy estrictas; cargos adicionales pesados. No embarcar sin confirmación expresa.\n• Cargos no incluyen documentación extraordinaria por requisitos sanitarios o aduaneros específicos."
elif incoterm == "EXW":
    clauses += f"• PICK UP: USD {delivery_cost} hacia Puerto/Aeropuerto de Buenos Aires.\n• Stuffing del contenedor y gastos de depósito fiscal no incluidos por defecto."

st.markdown(f'<div class="clause-box">{clauses.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
