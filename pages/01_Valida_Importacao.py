# -*- encoding:utf-8 -*-
import streamlit as st
import utils.util as util
from io import StringIO

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

    with st.form('Valida Importação',clear_on_submit=False):
        secretariaEscolhida = st.selectbox('Secretaria',secretarias,index=None,placeholder="Selecione a Secretaria")    
        contratoEscolhido = st.selectbox('Contrato de Gestão / Termo de Colaboração',contratos,index=None,placeholder="Selecione o Contrato")
        oficio = st.text_input("Ofício da Instituição")
        linha = st.text_input("Linha da planilha de Desbloqueio")
        tipoarquivoEscolhido = st.selectbox('Tipo de Arquivo',['Despesas','Contratos de Terceiros','Saldos','Receitas'],index=None,placeholder="Selecione o Tipo de Arquivo")
        arquivo = st.file_uploader("Arquivo da ser verificado",type="csv",help="Envie um arquivo de cada vez")
        processou = st.form_submit_button("Processar")       
        
        if processou:
            if arquivo and secretariaEscolhida and contratoEscolhido and oficio and linha and tipoarquivoEscolhido:
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
                        
                        if cabecalhoArquivo == cabecalhoDespesas:
                            st.write('O cabeçalho é compatível com o modelo DESPESAS GNOSIS.')
                        else:
                            st.error('O arquivo não tem o layout de Despesas ou não é compatível com o modelo DESPESAS GNOSIS.')
                            diferentes = [elemento for elemento in cabecalhoDespesas if elemento not in cabecalhoArquivo]
                            st.write('Colunas diferentes: ',diferentes)

                        #Valida de os campos DATA estão no formato XXXX-XX-XX

                        ##for linha in string_data.readline():
                        #linha = string_data.readline()
                        #st.write(linha)

                        string_data.close()
                    except:
                        st.error("O arquivo NÃO está no formato UTF-8!")

                    arquivo.close()        
                    st.success('Processamento concluído!')
            else:
                st.error('Todos os campos devem ser preenchidos!')
                   
with tab2:    
    '''
    # Consulta Arquivos Enviados
    '''
    st.write("Calma garoto! Um dia você chega lá!")

