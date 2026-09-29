import streamlit as st
from supabase import create_client

# Configuración de la página para celulares y PC
st.set_page_config(page_title="Control Kiosco - Panel Dueño", page_icon="📊", layout="wide")

# Credenciales de Supabase
SUPABASE_URL = "https://xxiuwpqaycngdbnphaap.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4aXV3cHFheWNuZ2RibnBoYWFwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MDY0NTcwNCwiZXhwIjoyMTA2MjIxNzA0fQ.rkdxUKmK3D6rC5EcSk9V6McI0H4z9xZMKedSh6nWS6M"  # Tu clave de Supabase completa

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# --- FILTRO DE SUCURSALES (BARRA LATERAL) ---
st.sidebar.title("🏢 Filtro de Sucursal")
kiosco_seleccionado = st.sidebar.selectbox(
    "Seleccionar Kiosco:",
    ["Todos los Kioscos", "Kiosco 1", "Kiosco 2"]
)

st.title("📊 Panel de Control del Kiosco")
st.write(f"Monitoreo en tiempo real — **{kiosco_seleccionado}**")

# Botón para refrescar datos
if st.button("🔄 Actualizar Datos"):
    st.cache_data.clear()
    st.rerun()

# Crear pestañas principales
tab1, tab2, tab3 = st.tabs(["💵 Resumen de Ventas", "📦 Estado de Stock", "📜 Remitos y Egresos"])

# --- TAB 1: VENTAS ---
with tab1:
    st.header("Resumen General de Caja")
    
    # Consulta según filtro de sucursal
    query_ventas = supabase.table("ventas").select("*")
    if kiosco_seleccionado != "Todos los Kioscos":
        query_ventas = query_ventas.eq("kiosco_id", kiosco_seleccionado)
        
    res_ventas = query_ventas.execute()
    ventas = res_ventas.data

    if ventas:
        total_recaudado = sum(v["total"] for v in ventas if v.get("total"))
        cant_ventas = len(ventas)
        
        col1, col2 = st.columns(2)
        col1.metric("Total Recaudado", f"${total_recaudado:,.2f}")
        col2.metric("Ventas Realizadas", cant_ventas)
        
        st.subheader("Historial de Ventas")
        st.dataframe(ventas, use_container_width=True)
    else:
        st.info("No hay registro de ventas para el filtro seleccionado.")

# --- TAB 2: STOCK ---
with tab2:
    st.header("Inventario de Productos")
    
    query_prods = supabase.table("productos").select("*")
    if kiosco_seleccionado != "Todos los Kioscos":
        query_prods = query_prods.eq("kiosco_id", kiosco_seleccionado)
        
    res_prods = query_prods.execute()
    prods = res_prods.data

    if prods:
        st.dataframe(prods, use_container_width=True)
    else:
        st.info("No hay productos registrados para esta sucursal.")

# --- TAB 3: EGRESOS ---
with tab3:
    st.header("Gastos y Pagos a Proveedores")
    
    query_egresos = supabase.table("egresos").select("*")
    if kiosco_seleccionado != "Todos los Kioscos":
        query_egresos = query_egresos.eq("kiosco_id", kiosco_seleccionado)
        
    res_egresos = query_egresos.execute()
    egresos = res_egresos.data

    if egresos:
        total_gastos = sum(e["monto_total"] for e in egresos if e.get("monto_total"))
        st.metric("Gastos Totales", f"${total_gastos:,.2f}")
        
        st.subheader("Detalle de Remitos / Egresos")
        st.dataframe(egresos, use_container_width=True)
    else:
        st.info("No hay egresos registrados para la sucursal seleccionada.")
