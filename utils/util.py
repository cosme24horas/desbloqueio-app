import pandas as pd
import requests
import json
import re
## DEBUG ##
#import streamlit as st

# Dicionário de erros
erros = {
    "01": "Todos os campos devem ser preenchidos!",
    "02": "O arquivo NÃO está no formato UTF-8!",
    "03": "O arquivo não tem o layout de Despesas ou não é compatível com o modelo DESPESAS GNOSIS.",
    "04": "O arquivo não tem o layout de Contratos de Terceiros ou não é compatível com o modelo ANEXOS."
}

def carregaSecretarias():
    arqSecretaria = open('data/secretarias.json')
    dadosSecretarias = json.load(arqSecretaria)
    arqSecretaria.close()
    opcoes = []

    for secretaria in dadosSecretarias["secretarias"]:
        opcoes.append(secretaria["nome_secretaria"])
    
    return opcoes

def carregaInstituicoes():
    arqInstituicoes = open("data/instituicoes.json")
    dadosInstituicoes = json.load(arqInstituicoes)
    arqInstituicoes.close()
    opcoes = []

    for instituicao in dadosInstituicoes["VW_OS"]:
        opcoes.append(instituicao["DSC_OS"])
    
    return opcoes

def carregaContratos():
    arqContratos = open("data/contratos.json")
    dadosContratos = json.load(arqContratos)
    arqContratos.close()
    opcoes = []

    for contrato in dadosContratos["VW_CONTRATO_V2"]:
        opcoes.append(contrato["DSC_CONTRATO"])
    
    opcoes.sort()
    return opcoes

def carregaInstrumentos():
    arqContratos = open("data/contratos.json")
    dadosContratos = json.load(arqContratos)
    arqContratos.close()

    return dadosContratos

class Validadora:
    def __init__(self, base_url,instituicao):
        self.base_url = base_url  # URL base para a verificação dos arquivos PDF.        
        self.instituicao = instituicao # Código da instituição
        self.url_formatada = ""

    def formatar_url(self,nome_imagem):
        self.coluna_imagem = nome_imagem.strip().replace(" ", "%20")
        if not self.coluna_imagem.endswith('.pdf'):
            self.coluna_imagem = self.coluna_imagem + '.pdf'
        self.url_formatada = self.base_url.format(numero_da_instituicao=self.instituicao, nome_do_pdf=self.coluna_imagem)        

    def validarPDF(self,nome_imagem):
        if not nome_imagem:
            return "Campo não preenchido"
        
        self.formatar_url(nome_imagem)
        try:
            response = requests.head(self.url_formatada)
            # Avaliação do status do arquivo baseado no tamanho indicado no cabeçalho.
            if response.status_code == 200:
                status = 'Sim'
                if int(response.headers.get('Content-Length', 1)) == 0:
                    status = 'Corrompido'
            else:
                status = 'Não'
        except requests.RequestException as e:
            status = f'Erro de verificação: {str(e)}'
        return str(status)
    
    def validarData(self,data = None):
        padrao = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if data is not None:
            if re.match(padrao, str(data)):
                return "Sim"
            else:
                return "Não"
        else:
            return "Não"
        
    def validarDataAbreviada(self,data = None):
        padrao = re.compile(r'^\d{4}-\d{2}')
        if data is not None:
            if re.match(padrao, str(data)):
                return "Sim"
            else:
                return "Não"
        else:
            return "Não"  


class Modelo:
    def __init__(self):    
        self.Despesas = 'COD_OS;COD_UNIDADE;COD_CONTRATO;ANO_MES_REF;TIPO;CODIGO;CNPJ;RAZAO;CPF;NOME;NUM_DOCUMENTO;SERIE;DESCRICAO;DATA_EMISSAO;DATA_VENCIMENTO;DATA_PAGAMENTO;DATA_APURACAO;VALOR_DOCUMENTO;VALOR_PAGO;DESPESA;RUBRICA;BANCO;AGENCIA;CONTA_CORRENTE;PMT_PAGA;QTDE_PMT;IDENT_BANCARIO;FLAG_JUSTIFICATIVA'
        self.ContratosTerceiros = 'COD_OS;COD_UNIDADE;COD_CONTRATO;RAZAO_SOCIAL;CNPJ;SERVICO;VALOR_MES;VIGENCIA;CONTRATO_ANO_MES_INICIO;CONTRATO_ANO_MES_FIM;REF_TRI;REF_ANO_MES;IMG_CONTRATO'
        self.cabecalhoDespesas = []
        self.cabecalhoContratosTerceiros = []

    def retornaCabecalhoDespesas(self):     
        if not self.cabecalhoDespesas:
            self.cabecalhoDespesas = self.trataCabecalho(self.Despesas)
            return self.cabecalhoDespesas
        else:        
            return self.cabecalhoDespesas
    
    def retornaCabecalhoContratosTerceiros(self):     
        if not self.cabecalhoContratosTerceiros:
            self.cabecalhoContratosTerceiros = self.trataCabecalho(self.ContratosTerceiros)
            return self.cabecalhoContratosTerceiros
        else:        
            return self.cabecalhoContratosTerceiros
    
    def trataCabecalho(self,cabecalho):
        cabecalhoTratado = cabecalho
        cabecalhoTratado = cabecalhoTratado.replace(" ","").strip('\r\n').upper()
        cabecalhoTratado = cabecalhoTratado.split(";")
        return cabecalhoTratado
    
    def contemCabecalho(self,cabecalhoModelo,cabecalhoArquivo):
        # Verificar se o cabecalhoModelo está contido em cabecalhoArquivo.
        todosContidos = all(item in cabecalhoArquivo for item in cabecalhoModelo)
        if todosContidos:
            return True
        else:
            return False
