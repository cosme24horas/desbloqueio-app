# -*- encoding:utf-8 -*-
# streamlit run streamlit_app.py

import streamlit as st
import utils.util as util
from io import StringIO
import pandas as pd
import re
import datetime

limite = 2000

st.set_page_config(
    page_title='Valida Arquivos de Importação',
    page_icon='https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f5a5.svg'
)

tipoArquivo = ['Despesas', 'Contratos de Terceiros', 'Saldos', 'Bens Patrimoniados']

tab1, tab2 = st.tabs(["Envio de Arquivo", "Consulta Arquivos Enviados"])

with tab1:
    secretarias = util.carregaSecretarias()
    instituicoes = util.carregaInstituicoes()
    contratos = util.carregaContratos()
    validou = ""

    with st.form('Valida Importação', clear_on_submit=False):
        tipoarquivoEscolhido = st.selectbox('Tipo de Arquivo', tipoArquivo, index=None, placeholder="Selecione o Tipo de Arquivo")
        arquivo = st.file_uploader("Arquivo a ser verificado", type="csv", help="Envie um arquivo de cada vez")
        processou = st.form_submit_button("Processar")

        if processou:
            if arquivo and tipoarquivoEscolhido:
                with st.spinner('Processando...'):
                    try:
                        string_data = StringIO(arquivo.getvalue().decode("utf-8-sig"))
                        cabecalhoArquivo = string_data.readline().strip()
                        string_data.seek(0)
                        
                        meuModelo = util.Modelo()
                        cabecalhoArquivo = meuModelo.trataCabecalho(cabecalhoArquivo)

                        df = pd.read_csv(string_data, sep=';', header=0, index_col=False, dtype=str)
                        df = df.dropna(how='all')
                        st.write("Prévia do arquivo original:")
                        st.dataframe(df)
                        tamanho = len(df)

                        # Convertendo para string para garantir que não haja problemas
                        df['COD_OS'] = df['COD_OS'].astype(str)
                        verificador = util.Validadora(st.secrets['base_url'], df['COD_OS'][0])
                        
                        if tipoarquivoEscolhido == "Despesas":
                            cabecalhoDespesas = meuModelo.retornaCabecalhoDespesas()
                            if meuModelo.contemCabecalho(cabecalhoDespesas, cabecalhoArquivo):
                                st.write('O cabeçalho é compatível com o modelo DESPESAS GNOSIS.')
                                df[['DATA_EMISSAO_VALIDADA', 'DATA_VENCIMENTO_VALIDADA', 'DATA_PAGAMENTO_VALIDADA', 'DATA_APURACAO_VALIDADA']] = df[['DATA_EMISSAO', 'DATA_VENCIMENTO', 'DATA_PAGAMENTO', 'DATA_APURACAO']].applymap(verificador.validarData)
                                df['ANO_MES_REF_VALIDADA'] = df['ANO_MES_REF'].apply(verificador.validarDataAbreviada)

                                if tamanho < limite:
                                    df['TEM_IMAGEM'] = df['DESCRICAO'].apply(verificador.validarPDF)
                                else:
                                    st.warning("Não foi possível verificar a existência dos documentos. O arquivo possui mais de 2000 linhas.")    
                                validou = 1
                            else:
                                st.error(util.erros["03"])
                                diferentes = [elemento for elemento in cabecalhoDespesas if elemento not in cabecalhoArquivo]
                                st.write('Colunas diferentes:', diferentes)

                        elif tipoarquivoEscolhido == "Contratos de Terceiros":
                            cabecalhoContratos = meuModelo.retornaCabecalhoContratosTerceiros()
                            if meuModelo.contemCabecalho(cabecalhoContratos, cabecalhoArquivo):
                                st.write('O cabeçalho é compatível com o modelo ANEXO.')
                                df['REF_ANO_MES_VALIDADA'] = df['REF_ANO_MES'].apply(verificador.validarData)
                                df[['CONTRATO_ANO_MES_INICIO_VALIDADA', 'CONTRATO_ANO_MES_FIM_VALIDADA', 'REF_TRI_VALIDADA']] = df[['CONTRATO_ANO_MES_INICIO', 'CONTRATO_ANO_MES_FIM', 'REF_TRI']].applymap(verificador.validarDataAbreviada)
                                
                                if tamanho < limite:                                
                                    df['TEM_IMAGEM'] = df['IMG_CONTRATO'].apply(verificador.validarPDF)
                                else:
                                    st.warning("Não foi possível verificar a existência dos documentos. O arquivo possui mais de 2000 linhas.")

                                validou = 1
                            else:
                                st.error(util.erros["04"])
                                diferentes = [elemento for elemento in cabecalhoArquivo if elemento not in cabecalhoContratos]
                                st.write('Colunas diferentes:', diferentes)

                        elif tipoarquivoEscolhido == "Saldos":
                            cabecalhoSaldos = meuModelo.retornaCabecalhoSaldos()
                            if meuModelo.contemCabecalho(cabecalhoSaldos, cabecalhoArquivo):
                                st.write('O cabeçalho é compatível com o modelo SALDO IPCEP.')
                                df['ANO_MES_REF_VALIDADA'] = df['ANO_MES_REF'].apply(verificador.validarDataAbreviada)
                                df['TEM_IMAGEM'] = df['EXTRATO'].apply(verificador.validarPDF)
                                validou = 1
                            else:
                                st.error(util.erros["05"])
                                diferentes = [elemento for elemento in cabecalhoArquivo if elemento not in cabecalhoSaldos]
                                st.write('Colunas diferentes:', diferentes)

                        elif tipoarquivoEscolhido == "Bens Patrimoniados":
                            cabecalhoBens = meuModelo.retornaCabecalhoBens()
                            if meuModelo.contemCabecalho(cabecalhoBens, cabecalhoArquivo):
                                st.write('O cabeçalho é compatível com o modelo BENS CEP28.')
                                df['ANO_MES_REF_VALIDADA'] = df['ANO_MES_REF'].apply(verificador.validarDataAbreviada)
                                df['DATA_AQUISICAO_VALIDADA'] = df['DATA_AQUISICAO'].apply(verificador.validarData)
                                df['TEM_IMAGEM'] = df['IMG_NF'].apply(verificador.validarPDF)
                                validou = 1
                            else:
                                st.error(util.erros["05"])
                                diferentes = [elemento for elemento in cabecalhoArquivo if elemento not in cabecalhoBens]
                                st.write('Colunas diferentes:', diferentes)

                        else:
                            st.warning("Função em desenvolvimento! 😢", icon="⚠️")
                        
                        st.success('Processamento concluído!')

                    except UnicodeDecodeError:
                        st.error(util.erros["02"])
                    except Exception as e:
                        st.error(f"Erro inesperado: {e}")

            else:
                st.error('Todos os campos devem ser preenchidos!')

    if validou:
        nomeArquivo = f"VALIDADO_{str(df['COD_OS'][0])}_{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M')}.csv"
        st.download_button(label="Download do arquivo CSV", data=df.to_csv(sep=';', index=False), mime='text/csv', file_name=nomeArquivo)

with tab2:
    st.write("Calma garoto! Um dia você chega lá!")