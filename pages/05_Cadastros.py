import streamlit as st
import utils.util as util
import pandas as pd

st.set_page_config(
    page_title='Cadastros',
    page_icon=':shopping_bags:', # This is an emoji shortcode. Could be a URL too.
)

tab1, tab2 = st.tabs(["Instrumentos Contratuais","Outros"])

with tab1:
    # Set the title that appears at the top of the page.
    '''
    # Instrumentos Contratuais
    '''
    contratos = util.carregaInstrumentos()
    
    df = pd.json_normalize(contratos['VW_CONTRATO_V2'])
    st.dataframe(df) 
           
with tab2:    
    '''
    # Outros ...
    '''
    st.write("Calma garoto! Um dia você chega lá!")
