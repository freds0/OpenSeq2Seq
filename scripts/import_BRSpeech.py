#-*- coding: future_fstrings -*- 
import os
import re
import unicodedata
from tqdm import tqdm
import pandas 
import argparse
from math import ceil, floor

class Palavra:

    def __init__(self, singular, plural):
        self.singular = singular
        self.plural = plural

class Extenso:

    def __init__(self):

        self._numero_maximo = 999999999999999999999999999999999999999999999

        # Dicionários para armazenar os números por extenso
        self.unidades = {1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10 : 'dez', 
                         11 : 'onze', 12 : 'doze', 13 : 'treze', 14 : 'quatorze', 15 : 'quinze', 16 : 'dezesseis', 17 : 'dezessete', 18 : 'dezoito', 19 : 'dezenove'}

        self.dezenas = {2: 'vinte', 3: 'trinta', 4: 'quarenta', 5: 'cinquenta', 6: 'sessenta', 7: 'setenta', 8: 'oitenta', 9: 'noventa'}

        self.centenas = {1: Palavra('cem', 'cento'), 2: 'duzentos', 3: 'trezentos', 4: 'quatrocentos', 5: 'quinhentos', 6: 'seiscentos', 7: 'setecentos', 8: 'oitocentos', 9: 'novecentos'}

        # Tupla armazenando os milhares
        self.milhares = (Palavra('',''), Palavra('mil','mil'), Palavra('milhão','milhões'), \
                        Palavra('bilhão','bilhões'), Palavra('trilhão','trilhões'), Palavra('quatrilhão','quatrilhões'), \
                        Palavra('quintilhão','quintilhões'), Palavra('sextilhão','sextilhões'), Palavra('septilhão','septilhões'), \
                        Palavra('octilhão','octilhões'),Palavra('nonilhão','nonilhões'), Palavra('decilhão','decilhões'), \
                        Palavra('undecilhão','undecilhões'), Palavra('duodecilhão','duodecilhões'),Palavra('tredecilhão','tredecilhões'))


    def escrever(self, numero):
        if (numero > self._numero_maximo):
            raise Exception('Número informado maior que o número máximo suportado')
        if (numero == 0):
            return 'zero'
        extenso = ''

        # Conversão do número recebido para string
        numero_string = str(numero)
        # Busca o tamanho do número informado
        tamanho = len(numero_string)

        # Arredonda para cima para saber quantos grupos de três há
        ternarios = ceil(tamanho / 3)

        # Preenche a string do número com zeros até o tamanho divisível por 3
        numero_string = numero_string.zfill(ternarios * 3)
        
        # percorre os grupos de três números
        for n in range(1, ternarios + 1):
            # Busca a parte do número referente ao grupo atual
            parte_numero = int(numero_string[(n - 1) * 3 : n * 3])

            # Caso o grupo seja zero, não precisa de tratamento
            if parte_numero == 0:
                continue

            # Cálculo para retornar a centena
            centena = floor(parte_numero / 100)

            # Cálculo para retornar a dezena
            dezena = floor((parte_numero - (centena*100)) / 10)

            # Cálculo para retornar a unidade
            unidade = parte_numero - (centena*100) - (dezena*10)

            # Caso a centena esteja preenchida, faz o tratamento
            if (centena > 0):
                if (dezena == 0 and unidade == 0 and extenso != ''):
                    extenso += ' e '
                elif extenso != '':
                    extenso += ', '
                if (centena == 1): # Se for CEM deve busca do singular, caso a unidade ou dezena esteja preenchida, busca do plural
                    if(dezena > 0 or unidade > 0):
                        extenso += self.centenas[centena].plural
                    else:
                        extenso += self.centenas[centena].singular
                else:
                    extenso += self.centenas[centena] # Caso a centena for maior que 1, busca a string correspondente no dicionário
            
            # Caso a dezena esteja preenchida, faz o tratamento
            if (dezena > 0):
                if (extenso != ''): # Se o número por extenso já veio preenchido, adiciona "E"
                    extenso += ' e '

                if (dezena == 1): # Se a dezena for um, busca das unidades
                    dezena = 10 + unidade
                    unidade = 0 # para não executar o extenso das unidades
                    extenso += self.unidades[dezena] # Busca o extenso correspondente nas unidades
                else:
                    extenso += self.dezenas[dezena] # Se a dezena for maior que um, busca da sua posição correspondente nas dezenas

            # Caso a unidade esteja preenchida, faz o tratamento
            if (unidade > 0):
                if (extenso != ''): # Se a centena ou dezena estão preenchidas, adiciona "E"
                    extenso += ' e '
                extenso += self.unidades[unidade] # Busca o extenso correspondente nas unidades

            # Tratamento para milhares
            if n < tamanho: # Se não for o último, concatena o milhar correspondente
                if (parte_numero > 1):
                    extenso += f' {self.milhares[ternarios - n].plural}' # Maior que 1, busca o plural
                else:
                    extenso += f' {self.milhares[ternarios - n].singular}' # Se for 1, busca o singular
        return extenso.replace('um mil,', 'mil')

vocab="abcdefghijklmnopqrstuvwxyzçãàáâêéíóôõúû\-0123456789 "
punctuation = ['…', '...', '"', "'", ';', ',', ':', '.', '!', '?', ')', '(']

ordinals_numbers = {'13º':"décimo terceiro", '8º':"oitavo", '9ª':"nono", '3ª':"terceiro", '18ª':"décimo oitavo", 
                '21º':"vigésimo primeiro", '1º':"primeito", '2º':"segundo", '60ª':"sexagésima", '17ª':"décima sétima",
                '7º':"sétimo", '17º':"décimo sétimo", '15ª':"décimo quinto", 'nº':"número", '5º':"quinto", '26ª':"vigésima sexta", 
                '20ª':"vigésima", '22ª': "vigésimo segunda", '18º':"décimo oitavo", '14º':"décimo quarto", '5ª':"quinta", '3º':"terceiro", '9º':"nono", 
                '13ª':"décima terceira", '89º':"octogésimo nono", '16ª':"décima sexta", '90ª':"nonagésima", '4ª':"quarta", '7ª':"sétima", '19º':"décima nona", 
                '30º':"trigésimo", '19ª':"décima nona", '1ª':"primeira", '10º':"décimo", '30ª':"trigésima",
                '6ª':"sexta", '6º':"sexto", '12ª':"décima segunda", '2ª':"segunda", '10ª':"décima segunda", 
                '12º':"décimo segundo", '90º':"nonagésimo", '16º':"décimo sexto", '20º':"vigésimo", '4º':"quarto", '8ª':"oitava"}
def text_normalize(text):
    accents = ('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT') #portuguese
    chars = [c for c in unicodedata.normalize('NFD', text) if c not in accents]
    text = unicodedata.normalize('NFC', ''.join(chars))# Strip accent
    text = text.lower()
    text = re.sub("[^{}]".format(vocab), " ", text)
    text = re.sub("[ ]+", " ", text)
    return text

def preprocess(dataset_dir, out_dir, meta_data="metadata_train.csv"): 
  if out_dir is None:
    out_dir = dataset_dir

  normalised_lines = []
  ex = Extenso()
  
  frases_com_numeros = 0
  lines = open(os.path.join(dataset_dir,meta_data)).readlines()[1:] # by pass head
  for i in tqdm(range(len(lines))):
      #format: filename|subtitle|transcript|levenshtein
      splits= lines[i].split('|')
      text = splits[1]
      have_number = False
      text_list = []
      for word in text.split(' '):
        for p in punctuation:
          word = word.replace(p, '')
        #print(word)
        if 'º' in word or 'ª' in word:
          if word in ordinals_numbers.keys():
            word = ordinals_numbers[word]
          else:
            raise ValueError(' The ordinal number '+word+'is not in ordinals_numbers list fix this!')
        if word.isdigit():
          have_number = True
          word = ex.escrever(int(word))
        text_list.append(word)
      if have_number:
          text = ' '.join(text_list)
          frases_com_numeros += 1

      transcript = text_normalize(text)
      audiopath = os.path.abspath(os.path.join(dataset_dir,splits[0]))
      wavfilesize = os.path.getsize(audiopath)
      normalised_lines.append((audiopath, wavfilesize, transcript))

  df = pandas.DataFrame(data=normalised_lines, columns=["wav_filename", "wav_filesize", "transcript"])
  df.to_csv(os.path.join(out_dir, meta_data+"_brspeech3_openseq2seq.csv"), index=False)
  

if __name__ == "__main__":
    """
    
    Usage
    python import_brspeech.py --dataset_dir=/data/BRSpeech-ASR-beta3/

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset_dir', type=str, help='BRSpeech dataset root dir')
    parser.add_argument('-o', '--output_dir', type=str, default=None,
                        help='Output Dataset dir')
    
    args = parser.parse_args()
    numeros_ordinais = set()
    preprocess(args.dataset_dir, args.output_dir,meta_data="test_metadata.csv")
    preprocess(args.dataset_dir, args.output_dir,meta_data="train_metadata.csv")
