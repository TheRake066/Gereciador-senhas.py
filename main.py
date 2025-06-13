import uuid
import hashlib
from colorama import Fore, Style
import time
from getpass import getpass
import shelve
import sys

def loading(titulo="carregando",segundos=3):
    for i in range(segundos*4):
        pontos = '.'*(i%4)
        sys.stdout.write(f'\r{titulo}{pontos}')
        sys.stdout.flush()
        time.sleep(0.25)

def criptografar(senha):
    return hashlib.sha256(senha.encode()).hexdigest()
    
def gerar_token():
    return str(uuid.uuid4())

def texto_devagar(texto, delay=0.03):
    for c in texto:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def cadastro():
    cadastrar = getpass('\nCadastre uma senha mestre: ').strip()
    
    with shelve.open("senhas_mestre") as db:

        if 'senhas_mestre' in db:
            print(f'Senha ja existe!')
            texto_devagar('Faça login para continuar!')
            print('entrando em login...')
            login()
            return 
        else: 
            token = gerar_token()
            db['senhas_mestre'] = {
                'senhasm': criptografar(cadastrar),
                'token': token
}
    print('Cadastro feito')
    print(f'Esse é seu token "{token}" caso esqueça a senha!')
    print('por favor! não perca...')

def login():
    login = getpass('\nDigite a senha mestre:')
    
    with shelve.open("senhas_mestre") as db:
        if 'senhas_mestre' not in db:
            print('nenhuma senha cadastrada ainda!')
            cadastro()
            return

        elif criptografar(login) == db['senhas_mestre']['senhasm']:
            print('Senha correta!')
            menu()
            return
        else:
            print('Senha incorreta! tente novamente.')
def menu():
    time.sleep(2)
    texto_devagar(f'{Fore.GREEN}{"MENU":-^20}{Style.RESET_ALL}')
    print('[1] adicionar senha')
    print('[2] ver todas as senhas')
    print('[3] sair')

    while True:
        try:
            ask = input('menu ~$ ')
            entrada = int(ask)

            if entrada == 1:
                while True:
                    try:
                        quanto = int(input('quantas senhas?\n'))
            
                        if quanto <= 0:
                            print('Precisa ser pelo menos 1')
                            continue
                        
                        for _ in range(quanto):
                            with shelve.open('senhas') as txt:
                                senha = input('Nova senha no formato "categoria: senha"\n~ ').strip().lower()

                                if ':' in senha:
                                    chave, valor = senha.split(':',1)
                                    senha = valor.strip()
                                    categoria = chave.strip()
                                    txt[categoria] = senha
                                    break
                                else:
                                    print('formato invalido! siga o indicado')
                        break
                    except ValueError:
                        print('precisa ser um numero inteiro!') 

            elif entrada == 2:
                with shelve.open('senhas') as txt:
                    print('\nsenhas:')
                    for c,s in txt.items():
                        texto_devagar(f'{c} - {s}')
            elif entrada == 3:
                break
            else:
                print('precisa ser um numero do MENU!')
        except ValueError:
            if ask.strip() == "":
                print(f'{Fore.RED}{"Nada foi digitado!"}{Style.RESET_ALL}')
            else:
                print(f'{Fore.RED}{"Precisa ser um numero inteiro"}{Style.RESET_ALL}')

while True:
    try:
        texto_devagar(f'SYSTEM'.center(20,'-'))
        print('[9] cadastrar senha-mestre')
        print('[6] logar senha-mestre')
        print('[0] fechar')

        sistema = input('~ ')
        validação = int(sistema)

        if validação == 9:
            loading()
            cadastro()
            break
        elif validação == 6:
            loading()
            login()
            break
        elif validação == 0:
            break
        else:
           print(f"{Fore.RED}{'precisa ser um numero do sistema!'}{Style.RESET_ALL}")
    except ValueError as e:
        print(f"Debug: erro ao converter '{sistema}' para int: {e}")
        raise
