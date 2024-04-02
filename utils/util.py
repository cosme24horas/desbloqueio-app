import json

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