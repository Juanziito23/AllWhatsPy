from audio_awp import AWPAudio
from contatos_awp import AWPContatos
from mensagem_awp import AWPMensagem
from criptografia_awp import AWPCriptografia
from utilidades_awp import AWPUtilidades
# from errors_awp import AWPConnectionError
from decorators_awp import aprovarConexao
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
    )
from tkinter import messagebox
from  PIL import Image
from urllib import parse
import urllib.request
import os
import logging
import time 


class AllWhatsPy: 
    logging.basicConfig(level=logging.INFO, encoding='utf-8', filename='eventAWP.log', format='%(asctime)s - %(levelname)s - %(message)s')
    flag_connection = False
    
    
    def __init__(self, inicializarTitulo:bool=True):
        self.__tempo_inicial = time.time()
        AllWhatsPy.__tituloAWP(inicializarTitulo)
        self._get_logging(f"{' AllWhatsPy - AWP ':=^40}")
        
        
        self.ctt = AWPContatos(self)
        self.msg = AWPMensagem(self)
        self.audio = AWPAudio(self)
        self.utilidade = AWPUtilidades(self)
        self.criptografia = AWPCriptografia(self)
    
        self._generator_info_contato_acessado = self.__informacoes_contato_acessado()
    
        self._drive = None
        self._marktime = None   
        self.dados_nome_usuario = None

        self.atual_funcao = None

    def __del__(self):
        self._get_logging(f'Tempo de Execução AWP: {self.tempo_execucao}')
        self._get_logging(f"{'':=^40}")


    def __exit__(self, exc_type, exc_value, traceback): #pesquisar como fazer ocorrer caso o algoritmo reaja com um erro
        if exc_type is not None or exc_value is not None or traceback is not None:
            self._get_logging(f"{'':=^40}")
            self._get_logging(f'Ocorreu um erro durante a execução de {f"AllWhatsPy.{self.atual_funcao}()"}. Tempo de Execução AWP: {self.tempo_execucao}')
            self._get_logging(f"{'':=^40}")

    
    class InferenciaAWP:
        lista_contatos: list = list()
        contato: str = ""
        mensagem: str = ""
        contatosInexistentes: list = list()


    class _ArmazemXPATH:
        textbox_xpath: str = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        var_aux_xpath: str = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]'
        var_aux2_xpath: str = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p'


    @property 
    def tempo_execucao(self):  
        return f'{time.time()-self.__tempo_inicial:.4f}s'
        

    @staticmethod
    def __tituloAWP(item):
        if item:
            print(f"{' AllWhatsPy - AWP ':=^40}")
            print('https://github.com/DevLucasLourenco/AllWhatsPy')


    def conexao(self, server_host: bool=False, popup=False, calibragem: tuple[bool, int]=(True, 10)):
        self.__driveConfigGoogle(server_host)

        # Aguardo na realização do login com QR Code
        while True:
            try:
                self._drive.find_element(By.XPATH, self._ArmazemXPATH.var_aux_xpath)

                if server_host:
                    self._get_logging(f'Conexão por Server efetuada.')
                    self._get_logging(f'<Nome da Pasta: AllWhatsPyHost> | <Usuário: {self.dados_nome_usuario}>')

                else:
                    self._get_logging('Conexao Efetuada.')
                
                if popup:
                        messagebox.showinfo('Validado','Conexão Efetuada!')
                
                self.__config_calibragem(calibragem)
                break

            except:
                self._get_logging('Aguardando Login...')
                time.sleep(5)

        self.flag_connection = True              
        
    @aprovarConexao
    def desconectar(self):
        self._get_logging('Desconectando Whatsapp...')

        # xpath para abrir os botões de opção, identificar as opções e confirmar respectivamente
        dc_xpath_abrir = '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/div/span'
        dc_xpath_opcoes = '//*[@id="app"]/div/div/div[3]/header/div[2]/div/span/div[4]/span/div'
        dc_xpath_confirmar = '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[3]/div/div[2]/div/div'
        
        # clicar nos botões de opção
        self._drive.find_element(By.XPATH, dc_xpath_abrir).click()
        time.sleep(1)
        
        opcoes = self._drive.find_element(By.XPATH, dc_xpath_opcoes)
        lista_opcoes = opcoes.find_elements(By.TAG_NAME, 'li')
        time.sleep(1)

        # encontrar a opção de desconetar e clicar nela
        for item in lista_opcoes:
            if item.get_attribute('data-testid') == 'mi-logout menu-item':
                item.click()

        # confirmar desconexão
        self._drive.find_element(By.XPATH, dc_xpath_confirmar).click()
    
        
        self._drive.close()
        self._get_logging('Whatsapp Encerrado')    


    def explodir_server(self):
        ... 
        

    def __informacoes_contato_acessado(self): # método 'Generator' usado para coexistir com a classe AWPContato. Nela, será usada para alcançar os dados do contato acessado.
        xpath_aux = '//*[@id="main"]/header/div[2]/div/div'
        self._marktime_func(xpath_aux)

        
        while True:
            # Etapa 1
            ctt = self._drive.find_element(By.XPATH, xpath_aux)
            nome = ctt.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div/span[1]').text

            self.InferenciaAWP.contato = nome
            self.InferenciaAWP.lista_contatos.append(nome)
            yield 
            
            
            # Etapa 2
            self._get_logging(f"Atual Contato: {self.InferenciaAWP.contato}")
            self._get_logging(f"Lista de contatos acessados nesta instância: ({'; '.join(self.InferenciaAWP.lista_contatos)})")
            yield 


    def __driveConfigGoogle(self, validacao_server):        
        os.environ['WDM_LOG'] = '0'
        servico = Service(ChromeDriverManager().install())  

        if validacao_server:
            self.dados_nome_usuario = os.getlogin()
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-data-dir=C://users/{self.dados_nome_usuario}/AllWhatsPyHost')

        self._drive = webdriver.Chrome(service=servico, options=options)
        self._drive.maximize_window()
        self._drive.get(r'https://web.whatsapp.com/')
        self._marktime = WebDriverWait(self._drive, 90)
    

    def __config_calibragem(self, calibragem):
        if isinstance(calibragem, tuple) or isinstance(calibragem, list):
            if calibragem[0]:
                self._get_logging(f'Aguardando {calibragem[1]} segundos para calibragem.')
                time.sleep(calibragem[1])

        elif isinstance(calibragem, bool):
            if not calibragem:
                pass
            else:
                time.sleep(10)
        else:
            raise ValueError('Insira um valor válido para o parâmetro calibragem')


    def _flag_status(self):
        return self.flag_connection


    def _get_logging(self, item_log):
        logging.info(item_log) 
        
        
    def _marktime_func(self, objeto):
        res = self._marktime.until(
                    EC.presence_of_element_located(
                        (By.XPATH, objeto)
                        )
                    )
        return res
    
    
    def _tratamento_log_func(self, metodo):
        return f'{__class__.__name__}'+'.'+f'{metodo.__name__}'+'()'


    def _alterar_funcao_em_execucao(self, atual_funcao):
        self.atual_funcao = atual_funcao