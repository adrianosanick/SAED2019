import serial
import pandas as pd
import time
# FRAME -> :111222333444555666#

class Comunicacao:
    def __init__(self):
        self.port = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.5)
        self.port.flushInput() 
        self.stop_comm = True
        self.tam_frame = 20
        self.flag_comm = False
        self.frame_antigo = ''
        
    def escreve_valor_temperatura(self):
        try:
            if self.frame_antigo != self.frame_recebido:
                self.frame_antigo = self.frame_recebido
                self.dados_temp = pd.read_csv("arquivos/temperatura.csv",skiprows = 1,header=None,dtype = str)
                self.dados_temp.columns = ['C0', 'C1','C2','C3','C4','C5']
                print('atualiza temperatura')
                self.dados_temp.loc[0,'C0'] = int(self.frame_recebido[1:4],16)
                self.dados_temp.loc[0,'C1'] = int(self.frame_recebido[4:7],16)
                self.dados_temp.loc[0,'C2'] = int(self.frame_recebido[7:10],16)
                self.dados_temp.loc[0,'C3'] = int(self.frame_recebido[10:13],16)
                self.dados_temp.loc[0,'C4'] = int(self.frame_recebido[13:16],16)
                self.dados_temp.loc[0,'C5'] = int(self.frame_recebido[16:19],16)
                self.dados_temp.to_csv("arquivos/temperatura.csv", index=False)
        except:
            print('problemas para escrever arquivos/temperatura.csv')

    def escreve_valor_comm(self):
        try:
            self.dados_comm = pd.read_csv("arquivos/comunicacao.csv",skiprows = 1,header=None,dtype = str)
            self.dados_comm.columns = ['C0']
            self.frame_recebido = self.dados_comm.loc[0,'C0']
        except:
            print('erro escreve_valor_comm')

    def ler_valor_frame_recebido(self):
        self.frame_recebido = self.port.read(self.tam_frame).decode('ascii','ignore')
        #self.frame_recebido = ':012021004032021027#'

    def verifica_valor_recebido(self):
        if self.frame_recebido != '':
            self.flag_comm = True
            if self.frame_recebido[0] == ':' and self.frame_recebido[-1] == '#' and len(self.frame_recebido) == self.tam_frame:
                print('OK:                    ',self.frame_recebido)
                try:
                    #self.escreve_valor_comm()
                    self.escreve_valor_temperatura()
                    self.port.flushInput()
                except:
                    print('erro na escrita arquivos')
            else:
                print('erro frame:>>>>>',self.frame_recebido)
                self.port.flushInput()
        else:
            self.flag_comm = False
            print('frame vazio')
            self.port.flushInput()

    def rotinaRxTx(self):
    	while True:
            #self.escreve_valor_comm()
            self.ler_valor_frame_recebido()
            self.verifica_valor_recebido()

    def get_frame_recebido(self):
        return self.frame_recebido

    def get_flag_comm(self):
        return self.flag_comm
    
    def set_flag_stop_comm(self,valor):
        self.stop_comm = valor


comm = Comunicacao()
comm.rotinaRxTx()
