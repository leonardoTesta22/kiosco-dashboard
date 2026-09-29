import streamlit as st
from supabase import create_client

# Configuración de la página para celulares y PC
st.set_page_config(page_title="Control Kiosco - Panel Dueño", page_icon="📊", layout="wide")

# Credenciales de Supabase
SUPABASE_URL = "https://xxiuwpqaycngdbnphaap.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4aXV3cHFheWNuZ2RibnBoYWFwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MDY0NTcwNCwiZXhwIjoyMTA2MjIxNzA0fQ.rkdxUKmK3D6rC5EcSk9V6McI0H4z9xZMKedSh6nWS6M" # Pegá tu clave anon acá

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

st.title("📊 Panel de Control del Kiosco")
st.write("Monitoreo en tiempo real de ventas, caja y remitos.")

# Botón para refrescar datos
if st.button("🔄 Actualizar Datos"):
    st.cache_data.clear()

# Crear pestañas principales
tab1, tab2, tab3 = st.tabs(["💵 Resumen de Ventas", "📦 Estado de Stock", "🧾 Remitos y Egresos"])

# --- TAB 1: VENTAS ---
with tab1:
    st.header("Resumen General de Caja")
    res_ventas = supabase.table("ventas").select("*").execute()
    ventas = res_ventas.data

    if ventas:
        total_recaudado = sum(v["total"] for v in ventas)
        cant_ventas = len(ventas)
        
        col1, col2 = st.columns(2)
        col1.metric("Total Recaudado", f"${total_recaudado:.2f}")
        col2.metric("Ventas Realizadas", cant_ventas)

        st.subheader("Historial de Ventas")
        st.dataframe(ventas, use_container_width=True)
    else:
        st.info("No hay ventas registradas aún.")

# --- TAB 2: STOCK ---
with tab2:
    st.header("Inventario de Productos")
    res_prods = supabase.table("productos").select("*").execute()
    productos = res_prods.data

    if productos:
        st.dataframe(productos, use_container_width=True)
    else:
        st.info("No hay productos cargados.")

# --- TAB 3: EGRESOS / REMITOS ---
with tab3:
    st.header("Gastos y Pagos a Proveedores")
    res_egresos = supabase.table("egresos").select("*").execute()
    egresos = res_egresos.data

    if egresos:
        total_egresos = sum(e["monto_total"] for e in egresos)
        st.metric("Total Egresos", f"${total_egresos:.2f}")
        st.dataframe(egresos, use_container_width=True)
    else:
        st.info("No hay egresos registrados.")