from datetime import datetime
import pandas as pd
import requests
import os
import json
import re
import streamlit as st #

# Dicionário de erros
erros = {
    "01": "Todos os campos devem ser preenchidos!",
    "02": "O arquivo NÃO está no formato UTF-8!",
    "03": "O arquivo não tem o layout de Despesas ou não é compatível com o modelo DESPESAS GNOSIS."
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

def validar_data(data):
    padrao = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if data and re.match(padrao, data):
        return "Sim"
    else:
        return "Não"

class verificarPDF:
    def __init__(self, base_url,instituicao):        
        self.base_url = base_url  # URL base para a verificação dos arquivos PDF.        
        self.instituicao = instituicao # Código da instituição
        self.url_formatada = ""

    def formatar_url(self,nome_imagem):
        self.coluna_imagem = nome_imagem.strip().replace(" ", "%20")
        if not self.coluna_imagem.endswith('.pdf'):
            self.coluna_imagem = self.coluna_imagem + '.pdf'
        self.url_formatada = self.base_url.format(numero_da_instituicao=self.instituicao, nome_do_pdf=self.coluna_imagem)        

    def verificar(self,nome_imagem):
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