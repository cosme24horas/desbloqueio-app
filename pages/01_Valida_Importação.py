# -*- encoding:utf-8 -*-
# streamlit run streamlit_app.py
import streamlit as st
import utils.util as util
from io import StringIO
import pandas as pd
import re
import datetime

st.set_page_config(
    page_title='Valida Arquivos de Importação',
    page_icon='https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f5a5.svg', # This is an emoji shortcode. Could be a URL too    
)

tipoArquivo = ['Despesas','Contratos de Terceiros']

tab1, tab2 = st.tabs(["Envio de Arquivo","Consulta Arquivos Enviados"])
with tab1:
    # Valida Arquivo de Importação

    secretarias = util.carregaSecretarias()
    instituicoes = util.carregaInstituicoes()
    contratos = util.carregaContratos()       
    validou = ""

    with st.form('Valida Importação',clear_on_submit=False):
        #secretariaEscolhida = st.selectbox('Secretaria',secretarias,index=None,placeholder="Selecione a Secretaria")
        #contratoEscolhido = st.selectbox('Contrato de Gestão / Termo de Colaboração',contratos,index=None,placeholder="Selecione o Contrato")
        #oficio = st.text_input("Ofício da Instituição")
        #ano_referencia = st.selectbox('Ano referência',['2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024'],index=None,placeholder="Selecione o ano referência")
        #mes_referencia = st.selectbox('Mês referência',['01 - Janeiro','02 - Fevereiro','03 - Março','04 - Abril','05 - Maio','06 - Junho','07 - Julho','08 - Agosto','09 - Setembro','10 - Outubro','11 - Novembro','12 - Dezembro'],index=None,placeholder="Selecione o mês referência")
        #linha = st.text_input("Linha da planilha de Desbloqueio")
        tipoarquivoEscolhido = st.selectbox('Tipo de Arquivo',tipoArquivo,index=None,placeholder="Selecione o Tipo de Arquivo")
        arquivo = st.file_uploader("Arquivo da ser verificado",type="csv",help="Envie um arquivo de cada vez")
        processou = st.form_submit_button("Processar")     
        
        if processou:
            if arquivo and tipoarquivoEscolhido: #and secretariaEscolhida and contratoEscolhido and oficio and linha :
                with st.spinner('Processando...'):
                    try:
                        string_data = StringIO(arquivo.getvalue().decode("utf-8-sig"))
                        cabecalhoArquivo = string_data.readline()
                        string_data.close()                        
                        meuModelo = util.Modelo()
                        cabecalhoArquivo = meuModelo.trataCabecalho(cabecalhoArquivo)                    

                        if tipoarquivoEscolhido == "Despesas":
                            #Início das validações
                            #Valida se o cabeçalho é de um arquivo de Despesas                            
                            cabecalhoDespesas = meuModelo.retornaCabecalhoDespesas()

                            if meuModelo.contemCabecalho(cabecalhoDespesas,cabecalhoArquivo):
                                st.write('O cabeçalho é compatível com o modelo DESPESAS GNOSIS.')                        
                                df = pd.read_csv(arquivo, sep=';',header=0,index_col=False,dtype=str)                                                  
                                df = df.dropna(how='all')
                                df.fillna(0,inplace=True)
                                st.write("Prévia do arquivo original: ")
                                st.dataframe(df)
                                verificador = util.Validadora(st.secrets['base_url'], df['COD_OS'][0])
                                df[['DATA_EMISSAO_VALIDADA','DATA_VENCIMENTO_VALIDADA','DATA_PAGAMENTO_VALIDADA','DATA_APURACAO_VALIDADA']] = df[['DATA_EMISSAO','DATA_VENCIMENTO','DATA_PAGAMENTO','DATA_APURACAO']].apply([verificador.validarData])
                                # Validar se as imagens estão no Painel
                                df['TEM_IMAGEM'] = df[['DESCRICAO']].apply([verificador.validarPDF])
                                validou = 1
                            else:
                                # Erro: 'O arquivo não tem o layout de Despesas ou não é compatível com o modelo DESPESAS GNOSIS.
                                st.error(util.erros["03"])
                                diferentes = [elemento for elemento in cabecalhoDespesas if elemento not in cabecalhoArquivo]
                                st.write('Colunas diferentes: ',diferentes)
                        # Refatorar como feito em Despesas.
                        elif tipoarquivoEscolhido == "Contratos de Terceiros":
                            #Início das validações
                            #Valida se o cabeçalho é de um arquivo de Contratos de Terceiros
                            cabecalhoContratos = util.Modelos.ContratosTerceiros
                            cabecalhoContratos = cabecalhoContratos.rstrip('\r\n').upper()
                            cabecalhoContratos = cabecalhoContratos.split(";")

                            if cabecalhoArquivo == cabecalhoContratos:
                                st.write('O cabeçalho é compatível com o modelo ANEXO.')
                                #Valida se os campos DATA estão no formato XXXX-XX-XX                                
                                df = pd.read_csv(arquivo, sep=';',header=0,index_col=False,dtype=str)
                                df = df.dropna(how='all')                                
                                verificador = util.Validadora(st.secrets['base_url'], df['COD_OS'][0])
                                df[['REF_ANO_MES_VALIDADA']] = df[['REF_ANO_MES']].apply([verificador.validarData])
                                df[['CONTRATO_ANO_MES_INICIO_VALIDADA','CONTRATO_ANO_MES_FIM_VALIDADA','REF_TRI_VALIDADA']] = df[['CONTRATO_ANO_MES_INICIO','CONTRATO_ANO_MES_FIM','REF_TRI']].apply([verificador.validarDataAbreviada])
                                # Validar se as imagens estão no Painel
                                df['TEM_IMAGEM'] = df[['IMG_CONTRATO']].apply([verificador.validarPDF])                                
                                validou = 1                                
                            else:
                                # Erro: 'O arquivo não tem o layout de Contratos de Terceiros ou não é compatível com o modelo ANEXOS.'
                                st.error(util.erros["04"])
                                diferentes = [elemento for elemento in cabecalhoArquivo if elemento not in cabecalhoContratos]
                                st.write('Colunas diferentes: ',diferentes)
                        else:
                            st.warning("Função em desenvolvimento! 😢",icon="⚠️")                    
                        
                        st.success('Processamento concluído!')
                    except UnicodeDecodeError:
                        # O arquivo NÃO está no formato UTF-8!
                        st.error(util.erros["02"])
            else:
                st.error('Todos os campos devem ser preenchidos!')
    if validou:        
        nomeArquivo = "VALIDADO_"+df['COD_OS'][0]+"_"+datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")+".csv"
        st.download_button(label="Download do arquivo CSV",data=df.to_csv(sep=';',index=False),mime='text/csv',file_name=nomeArquivo)
        arquivo.close()
            
with tab2:    
    '''
    # Consulta Arquivos Enviados
    '''
    st.write("Calma garoto! Um dia você chega lá!")