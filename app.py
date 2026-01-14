import streamlit as st
import pandas as pd

st.title("📊 Sistema de Viabilidade 2026")

# Nomes exatos dos arquivos que você subiu
ARQUIVO_VIABILIDADE = "Cópia de VIABILIDADE COMERCIAL 2026 - ATUALIZADA.xlsm"
ARQUIVO_PRECOS = "TABELA PREÇOS MANUAL - ALFA E AUTO 2026.xlsm"

@st.cache_data
def carregar_dados():
    # O motor 'openpyxl' é necessário para ler arquivos .xlsm
    viabilidade = pd.read_excel(ARQUIVO_VIABILIDADE, sheet_name=None, engine='openpyxl')
    precos = pd.read_excel(ARQUIVO_PRECOS, sheet_name=None, engine='openpyxl')
    return viabilidade, precos

try:
    dados_v, dados_p = carregar_dados()
    st.success("Arquivos carregados com sucesso!")
    
    # Exemplo: Mostrando as abas disponíveis para você escolher
    abas = list(dados_v.keys())
    aba_selecionada = st.selectbox("Selecione a aba de análise", abas)
    st.write(dados_v[aba_selecionada].head())

except FileNotFoundError:
    st.error(f"Erro: Arquivo não encontrado! Verifique se os nomes no GitHub estão iguais a: \n1. {ARQUIVO_VIABILIDADE}\n2. {ARQUIVO_PRECOS}")
except Exception as e:
    st.error(f"Ocorreu um erro técnico: {e}")

st.info("Lembre-se: Pagamentos em dinheiro não são permitidos pelo sistema.")
