# -*- encoding:utf-8 -*-
# streamlit run streamlit_app.py
import streamlit as st
import utils.util as util
from io import StringIO
import pandas as pd
import re

st.set_page_config(
    page_title='Valida Arquivos de Importação',
    page_icon=':shopping_bags:', # This is an emoji shortcode. Could be a URL too.
)

tab1, tab2 = st.tabs(["Envio de Arquivo","Consulta Arquivos Enviados"])
with tab1:
    # Set the title that appears at the top of the page.
    '''
    # Valida Arquivo de Importação
    '''

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
        #tipoarquivoEscolhido = st.selectbox('Tipo de Arquivo',['Despesas','Contratos de Terceiros','Saldos','Receitas'],index=None,placeholder="Selecione o Tipo de Arquivo")
        arquivo = st.file_uploader("Arquivo da ser verificado",type="csv",help="Envie um arquivo de cada vez")        
        processou = st.form_submit_button("Processar")     
        
        if processou:
            if arquivo: #and secretariaEscolhida and contratoEscolhido and oficio and linha and tipoarquivoEscolhido:
                with st.spinner('Processando...'):
                    try:
                        string_data = StringIO(arquivo.getvalue().decode("utf-8"))
                        #Início das validações
                        #Valida se o cabeçalho é de um arquivo de Despesas
                        cabecalhoDespesas = 'COD_OS;COD_UNIDADE;COD_CONTRATO;ANO_MES_REF;TIPO;CODIGO;CNPJ;RAZAO;CPF;NOME;NUM_DOCUMENTO;SERIE;DESCRICAO;DATA_EMISSAO;DATA_VENCIMENTO;DATA_PAGAMENTO;DATA_APURACAO;VALOR_DOCUMENTO;VALOR_PAGO;DESPESA;RUBRICA;BANCO;AGENCIA;CONTA_CORRENTE;PMT_PAGA;QTDE_PMT;IDENT_BANCARIO;FLAG_JUSTIFICATIVA'
                        cabecalhoDespesas = cabecalhoDespesas.rstrip('\r\n').upper()
                        cabecalhoDespesas = cabecalhoDespesas.split(";")                    
                        cabecalhoArquivo = string_data.readline()
                        cabecalhoArquivo = cabecalhoArquivo.rstrip('\r\n').upper()
                        cabecalhoArquivo = cabecalhoArquivo.split(";")
                        cabecalhoArquivo.pop(0)
                        string_data.close()
                        
                        if cabecalhoArquivo == cabecalhoDespesas:
                            st.write('O cabeçalho é compatível com o modelo DESPESAS GNOSIS.')
                            #Valida se os campos DATA estão no formato XXXX-XX-XX
                            df = pd.read_csv(arquivo, sep=';',header=0,index_col=False,dtype=str)                                                  
                            df = df.dropna(how='all')                            
                            #df['LINHA'] = df.index + 1
                            df[['DATA_EMISSAO_VALIDADA','DATA_VENCIMENTO_VALIDADA','DATA_PAGAMENTO_VALIDADA','DATA_APURACAO_VALIDADA']] = df[['DATA_EMISSAO','DATA_VENCIMENTO','DATA_PAGAMENTO','DATA_APURACAO']].apply([util.validar_data])
                            # Validar se as imagens estão no Painel
                            verificador = util.verificarPDF(st.secrets['base_url'], df['COD_OS'][0])
                            df['TEM_IMAGEM'] = df[['DESCRICAO']].apply([verificador.verificar])                            
                            validou = 1
                        else:
                            # Erro: 'O arquivo não tem o layout de Despesas ou não é compatível com o modelo DESPESAS GNOSIS.
                            st.error(util.erros["03"])
                            diferentes = [elemento for elemento in cabecalhoArquivo if elemento not in cabecalhoDespesas]                 
                            st.write('Colunas diferentes: ',diferentes)
                            
                    except UnicodeDecodeError:
                        # O arquivo NÃO está no formato UTF-8!
                        st.error(util.erros["02"])

                    arquivo.close()
                    st.success('Processamento concluído!')
            else:
                st.error('Todos os campos devem ser preenchidos!')
    if validou:
        st.download_button(label="Download do arquivo CSV",data=df.to_csv(sep=';',index=False),mime='text/csv',file_name="VALIDADO_"+arquivo.name)
            
with tab2:    
    '''
    # Consulta Arquivos Enviados
    '''
    st.write("Calma garoto! Um dia você chega lá!")