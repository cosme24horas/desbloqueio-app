import streamlit as st
import utils.util as util
from io import StringIO
import pandas as pd
import datetime

st.set_page_config(
    page_title='Valida Arquivos de Alteração',
    page_icon='https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f5a5.svg',  # This is an emoji shortcode. Could be a URL too
)

tab1, tab2 = st.tabs(["Envio de Arquivo", "Consulta Arquivos Enviados"])

with tab1:
    secretarias = util.carregaSecretarias()
    instituicoes = util.carregaInstituicoes()
    contratos = util.carregaContratos()
    validou = False
    listaIMG = ['IMG_CONTRATO', 'EXTRATO', 'IMG_NF', 'DESCRICAO', 'Descricao', 'DESCRIÇÃO','Descricão']

    with st.form('Valida Importação', clear_on_submit=False):
        instituicaoEscolhida = st.selectbox('Instituição', instituicoes, index=None, placeholder="Selecione a Instituição")
        arquivo = st.file_uploader("Arquivo da ser verificado", type=['csv', 'xls', 'xlsx'], help="Envie um arquivo de cada vez")
        processou = st.form_submit_button("Processar")

        if processou:
            if instituicaoEscolhida and arquivo:
                with st.spinner('Processando...'):
                    cod_os = instituicaoEscolhida.split(" ")[0]
                    if arquivo.name.endswith('.xlsx') or arquivo.name.endswith('.xls'):
                        df = pd.read_excel(arquivo)
                    else:
                        string_data = StringIO(arquivo.getvalue().decode("utf-8-sig"))
                        df = pd.read_csv(string_data, sep=';', header=0, index_col=False, dtype=str)
                        string_data.close()

                    # Verificar se o arquivo tem uma coluna "ATRIBUTO"
                    if 'ATRIBUTO' in df.columns and 'NOVO_VALOR' in df.columns:
                        df = df.dropna(how='all')
                        st.write("Prévia do arquivo original: ")
                        st.dataframe(df)
                        
                        # Filtrar linhas onde o valor na coluna "ATRIBUTO" está na lista listaIMG
                        df_filtrado = df[df["ATRIBUTO"].isin(listaIMG)]

                        if not df_filtrado.empty:
                            # Adicionar uma nova coluna para os resultados da validação
                            verificador = util.Validadora(st.secrets['base_url'], cod_os[0])
                            df_filtrado['TEM_IMAGEM'] = df_filtrado[['NOVO_VALOR']].apply([verificador.validarPDF])                            
                            validou = True
                            st.success('Processamento concluído!')
                        else:
                            st.error('O arquivo não tem imagens a serem alteradas!')
                    else:
                        st.error('O arquivo não tem as colunas necessárias ("ATRIBUTO" e "NOVO_VALOR")!')
            else:
                st.error('Todos os campos devem ser preenchidos!')

    if validou:
        nomeArquivo = f"VALIDADO_{cod_os[0]}_{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M')}.csv"
        st.download_button(label="Download do arquivo CSV", data=df_filtrado.to_csv(sep=';', index=False), mime='text/csv', file_name=nomeArquivo)
        arquivo.close()

with tab2:
    '''
    # Consulta Arquivos Enviados
    '''
    st.write("Calma! Você nasceu de 7 meses??")
