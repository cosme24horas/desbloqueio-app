# -*- encoding:utf-8 -*-
# streamlit run streamlit_app.py
import streamlit as st
import utils.util as util
from io import StringIO
import pandas as pd
import re
import datetime

st.set_page_config(
    page_title='Valida Arquivos de Alteração',
    page_icon='https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f5a5.svg', # This is an emoji shortcode. Could be a URL too    
)

tab1, tab2 = st.tabs(["Envio de Arquivo","Consulta Arquivos Enviados"])
with tab1:    
    secretarias = util.carregaSecretarias()
    instituicoes = util.carregaInstituicoes()
    contratos = util.carregaContratos()
    validou = False
    listaIMG = ['IMG_CONTRATO','EXTRATO','IMG_NF','DESCRICAO','Descricao','DESCRIÇÃO']

    with st.form('Valida Importação',clear_on_submit=False):
        instituicaoEscolhida = st.selectbox('Instituição',instituicoes,index=None,placeholder="Selecione a Instituição")
        #secretariaEscolhida = st.selectbox('Secretaria',secretarias,index=None,placeholder="Selecione a Secretaria")
        #contratoEscolhido = st.selectbox('Contrato de Gestão / Termo de Colaboração',contratos,index=None,placeholder="Selecione o Contrato")
        #oficio = st.text_input("Ofício da Instituição")
        #ano_referencia = st.selectbox('Ano referência',['2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024'],index=None,placeholder="Selecione o ano referência")
        #mes_referencia = st.selectbox('Mês referência',['01 - Janeiro','02 - Fevereiro','03 - Março','04 - Abril','05 - Maio','06 - Junho','07 - Julho','08 - Agosto','09 - Setembro','10 - Outubro','11 - Novembro','12 - Dezembro'],index=None,placeholder="Selecione o mês referência")
        #linha = st.text_input("Linha da planilha de Desbloqueio")
        arquivo = st.file_uploader("Arquivo da ser verificado",type=['csv','xls','xlsx'],help="Envie um arquivo de cada vez")
        processou = st.form_submit_button("Processar")
        
        if processou:
            if instituicaoEscolhida and arquivo: #and secretariaEscolhida and contratoEscolhido and oficio and linha :
                with st.spinner('Processando...'):                    
                    cod_os = instituicaoEscolhida.split(" ")[0]
                    if arquivo.name.endswith('.xlsx') or arquivo.name.endswith('.xls'):                        
                        df = pd.read_excel(arquivo)                        
                    else:
                        string_data = StringIO(arquivo.getvalue().decode("utf-8-sig"))                        
                        df = pd.read_csv(arquivo, sep=';',header=0,index_col=False,dtype=str)
                        string_data.close()
                    
                    # Verificar se o arquivo tem uma coluna "ATRIBUTO"
                    if 'ATRIBUTO' in df.columns:
                        df = df.dropna(how='all')                            
                        st.write("Prévia do arquivo original: ")
                        st.dataframe(df)                        
                        df_filtrado = df[df["ATRIBUTO"].isin(listaIMG)]

                        # Pode não encontrar coluna de imagem
                        if not df_filtrado.empty:
                            st.write("Filtrando o DataFrame:")
                            st.write(df_filtrado)

                            # Esta verificação está incorreta. Corrigir.
                            for column in listaIMG:
                                st.write("Coluna: "+column)
                                                           
                                if df_filtrado["ATRIBUTO"] == column:
                                    st.write("Coluna encontrada: "+column)
                                    for nome_imagem in df_filtrado[column].unique():
                                        verificador = util.Validadora(st.secrets['base_url'], cod_os[0])
                                        st.write(nome_imagem)
                                        #st.write(verificador.validarPDF(nome_imagem))
                                validou = True                        
                            st.success('Processamento concluído!')
                        else:
                            st.error('O arquivo não tem imagens a serem alteradas!')    
                    else:
                        st.error('O arquivo não tem o layout de Alteração!')    
            else:
                st.error('Todos os campos devem ser preenchidos!')
    if validou:        
        nomeArquivo = "VALIDADO_"+cod_os[0]+"_"+datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")+".csv"
        st.download_button(label="Download do arquivo CSV",data=df.to_csv(sep=';',index=False),mime='text/csv',file_name=nomeArquivo)
        arquivo.close()            
with tab2:    
    '''
    # Consulta Arquivos Enviados
    '''
    st.write("Calma! Você nasceu de 7 meses??")