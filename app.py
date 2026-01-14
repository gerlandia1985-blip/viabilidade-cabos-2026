import streamlit as st
import pandas as pd

# Configuração visual
st.set_page_config(page_title="Calculadora de Viabilidade 2025", layout="wide")

# Carregamento de dados
@st.cache_data
def load_data():
    df = pd.read_csv('base_referencia_viabilidade.csv')
    return df

try:
    df_ref = load_data()
except:
    st.error("Erro: Arquivo 'base_referencia_viabilidade.csv' não encontrado!")
    st.stop()

# Cabeçalho
st.title("🚀 Simulador de Viabilidade Comercial")
st.subheader("Cálculo dinâmico baseado em Matéria-Prima e Descontos")

# Sidebar para Custos de Matéria-Prima
st.sidebar.header("💰 Custos de Matéria-Prima")
cobre_input = st.sidebar.number_input("Cobre (R$/kg)", value=52.00, step=1.0)
pvc_input = st.sidebar.number_input("PVC (R$/kg)", value=8.90, step=0.1)
embalagem_input = st.sidebar.number_input("Embalagem/Etiqueta (R$)", value=16.80, step=0.5)

# Formulário de Venda
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        marca = st.selectbox("Marca", options=sorted(df_ref['MARCA'].unique()))
    with col2:
        cabos_filtrados = df_ref[df_ref['MARCA'] == marca]['CABO'].unique()
        cabo = st.selectbox("Bitola (mm)", options=cabos_filtrados)
    with col3:
        quantidade = st.number_input("Qtd (Rolos/Peças)", min_value=1, value=1)
    with col4:
        desconto = st.slider("Desconto (%)", 0, 30, 0)

# Lógica de Cálculo
dados_prod = df_ref[(df_ref['MARCA'] == marca) & (df_ref['CABO'] == cabo)].iloc[0]

# Custo Novo = (PesoCu * PreçoCu) + (PesoPVC * PreçoPVC) + Fixo
custo_mp = (dados_prod['COBRE (kg)'] * cobre_input) + (dados_prod['PVC (kg)'] * pvc_input)
custo_total_unit = custo_mp + embalagem_input

# Venda
preco_base = dados_prod['PRECO_VENDA_REF']
preco_final = preco_base * (1 - (desconto / 100))
lucro_unit = preco_final - custo_total_unit
margem = (lucro_unit / preco_final) * 100

# Resultados
st.markdown("---")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Custo Unitário", f"R$ {custo_total_unit:.2f}")
with kpi2:
    st.metric("Preço de Venda (Líquido)", f"R$ {preco_final:.2f}", f"-{desconto}%")
with kpi3:
    color = "normal" if margem > 15 else "inverse"
    st.metric("Margem Bruta", f"{margem:.2f}%", delta=f"{lucro_unit:.2f} R$/un")

# Alertas de Aprovação (Parâmetros da sua planilha)
limite = 25 if marca == "ALFA" else 15
if margem >= limite:
    st.success(f"✅ PEDIDO APROVADO: Margem acima do esperado para {marca} ({limite}%).")
else:
    st.error(f"❌ PEDIDO REPROVADO: Margem abaixo do mínimo de {limite}%.")

# Detalhamento Técnico
with st.expander("Ver Ficha Técnica de Consumo"):
    st.write(f"**Cobre:** {dados_prod['COBRE (kg)']} kg | **PVC:** {dados_prod['PVC (kg)']} kg")