class Validadora:
    def __init__(self, base_url,instituicao):
        self.base_url = base_url  # URL base para a verificação dos arquivos PDF.        
        self.instituicao = instituicao # Código da instituição
        self.url_formatada = ""
        self.arquivos = {}

    def formatar_url(self,nome_imagem):
        self.coluna_imagem = nome_imagem.strip().replace(" ", "%20")
        if not self.coluna_imagem.endswith('.pdf'):
            self.coluna_imagem = self.coluna_imagem + '.pdf'
        self.url_formatada = self.base_url.format(numero_da_instituicao=self.instituicao, nome_do_pdf=self.coluna_imagem)        

    def validarPDF(self,nome_imagem):
        if not nome_imagem:
            return "Campo não preenchido"
        
        st.write(type(nome_imagem))
        
        self.formatar_url(nome_imagem)

        if self.arquivos.get(self.url_formatada):
            return self.arquivos.get(self.url_formatada)

        try:
            response = requests.head(self.url_formatada, timeout=10)
            # Avaliação do status do arquivo baseado no tamanho indicado no cabeçalho.
            if response.status_code == 200:
                #self.arquivos[self.url_formatada] = 'Sim' #status = 'Sim'
                if int(response.headers.get('Content-Length', 1)) == 0:
                    status = 'Corrompido'
                    #self.arquivos[self.url_formatada] = 'Corrompido' #status = 'Corrompido'
                else:
                    status = 'Sim'                  
            else:
                status = 'Não'
                #self.arquivos[self.url_formatada] = 'Não' #status = 'Não'
        except requests.RequestException as e:
            status = f'Erro de verificação: {str(e)}'

        self.arquivos[self.url_formatada] = status    
        return status
        #return str(self.arquivos[self.url_formatada])
    
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