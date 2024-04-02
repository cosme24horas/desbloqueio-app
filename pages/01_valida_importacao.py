import streamlit as st
import utils.util as util

st.set_page_config(
    page_title='Valida Arquivos de Importação',
    page_icon=':shopping_bags:', # This is an emoji shortcode. Could be a URL too.
)

# Set the title that appears at the top of the page.
'''
# Valida Arquivo de Importação
'''

secretarias = util.carregaSecretarias()
instituicoes = util.carregaInstituicoes()
contratos = util.carregaContratos()

with st.form('Valida Importação'):
    secretariaEscolhida = st.selectbox('Secretaria',secretarias,index=None,placeholder="Selecione a Secretaria")
   # instituicaoEscolhida = st.selectbox('Instituição',instituicoes,index=None,placeholder="Selecione a Instituição")
    contratoEscolhido = st.selectbox('Contrato de Gestão / Termo de Colaboração',contratos,index=None,placeholder="Selecione o Contrato")
    oficio = st.text_input("Ofício da Instituição")
    linha = st.text_input("Linha da planilha de Desbloqueio")
    arquivo = st.file_uploader("Arquivo da ser verificado",type="csv",help="Arquivo a ser processado")
    st.form_submit_button("Processar")

