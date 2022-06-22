import csv

class NotLetter(Exception):
    def __init__(self, message = 'Invalid Characters'):
        self.message = message
        super().__init__(self.message)
class Duplicate(Exception):
    def __init__(self, message = 'Duplicate Entrance'):
        self.message = message
        super().__init__(self.message)

def check_email(email:str,arquivo:str) ->None:
    '''
        Função recebe duas strings do email e do arquivo a ser utilizado.
        Apenas verifica erros de entrada sem retorno.
    '''
    arquivo = open(arquivo, 'r')
    planilha = list(csv.reader(arquivo, delimiter=';', lineterminator='\n'))
    arquivo.close()

    for i in planilha:
        if email in i:
            raise Duplicate
    cont=0
    if not "@" in email: raise NotLetter()
    for caracter in email:
        if caracter=="@":
            cont+=1
            if cont>1: raise NotLetter()
        if (not caracter.isalpha() and not caracter.isnumeric()) and caracter!="@" and caracter!="_" and caracter!=".":
            raise NotLetter()
def char_nome(Nome:str)->None:
    '''
        Recebe uma string Nome e não recebe nada, apenas valida a entrada.
    '''
    for char in Nome:
        if not char.isalpha() and char!=" ":
            raise NotLetter()
def cadastrar_musicos(arquivo:str,header:dict)-> None:
    '''
        Recebe uma string com o arquivo com a base de músicos e um dicionário com o cabeçalho do arquivo.
        Retorna vazio apenas quando erro de entradas. Adiciona campos no arquivo recebido.
    '''
    entrada_csv={'Nome':'','Email':'','Gêneros':'','Instrumentos':''}
    
    Nome=input("Digite o nome do músico: ")
    
    try:
        char_nome(Nome)
    except NotLetter:
        print('Caracter inválido\n')
        return

    entrada_csv['Nome']=(Nome.title())

    Email=input("Digite o email do músico: ")

    try:
        check_email(Email,arquivo)
    except NotLetter:
        print('Caracter inválido\n')
        return
    except Duplicate:
        print("Email já está cadastrado\n")
        return

    entrada_csv['Email']=(Email)

    Genero=(input("Digite o(s) gênero(s) musical(is):\n (Caso tenha mais de um separar por virgula sem espaço)\n ex: Rock,Funk\n"))
    genero_list=Genero.split(",")
    for i in range(len(genero_list)):
        genero_list[i]=genero_list[i].title()
    entrada_csv['Gêneros']=(genero_list)

    Instrumento=(input("Digite o(s) instrumento(s) musical(is):\n (Caso tenha mais de um separar por virgula sem espaço)\n ex: Flauta,Guitarra\n"))
    instrumento_list=Instrumento.split(",")
    for i in range(len(instrumento_list)):
        instrumento_list[i]=instrumento_list[i].title()
    entrada_csv['Instrumentos']=(instrumento_list)
    
    with open(arquivo,'a') as file2:
        escrita=csv.DictWriter(file2,skipinitialspace=True,delimiter=';', lineterminator='\n',fieldnames=header)
        escrita.writerow(entrada_csv)
        print("\nCadastro efetuado com sucesso\n")
        


def buscar_musicos(arquivo:str)->None or list:
    '''
        Recebe uma string com o arquivo com a base de músicos. 
        Retorna vazio apenas quando erro de entradas, senão retorna lista de dicionários com busca realizada.
    '''

    print("Para fazer uma busca escreva o nome da categoria seguido pelo valor procurado espaçado por ':'caso tenha mais de um valor de busca, separe por espaço\n Ex: Nome:Rafael,Gêneros:Rock\n")
    print("Selecione pelo menos uma categoria de 'Nome,Email,Gêneros,Instrumentos\n")
    busca=str(input()).title()

    try:
        dict_busca=dict(x.split(":") for x in busca.split(","))
        if "Email" in dict_busca:
            dict_busca["Email"]=dict_busca["Email"].lower()
        
    except ValueError:
        print("\nValores de entrada incorretos, por favor tente novamente\n")
        return

    try:
        escolha_eou=int(input("Deseja os resultados batam com todas informações passadas(0) ou apenas uma(1)?\n "))
    except:
        print("\n Valores de entrada incorretos, por favor tente novamente\n")
        return

    lista_busca=[]

    with open(arquivo,'r') as file:
        leitura=csv.DictReader(file,skipinitialspace=True,delimiter=';', lineterminator='\n')
        for l in leitura:
            try:
                for key, value in dict_busca.items():
                        if key=="Gêneros" or key=="Instrumentos":                 
                            if value in l[key]:
                                lista_busca.append(l)
                                break
                        elif value in l[key]:
                            lista_busca.append(l)
                            break
            except:
                print("Categorias incorretas. Por favor, tente novamente.\n")
                break

    if escolha_eou==1:
        return lista_busca
    
    elif escolha_eou==0:
        proximo=False
        lista_busca2=[]
        for k in lista_busca:
            for key,value in dict_busca.items():
                if key=="Gêneros" or key=="Instrumentos":                 
                    if value not in k[key]:
                        proximo=True
                        break
                elif value not in k[key]:
                    proximo=True
                    break
            if proximo:
                proximo=False
            else:
                lista_busca2.append(k)
            
        return lista_busca2


def verifica_alteracao(dict_:dict) ->None:
    '''
        Recebe um dicionário e verifica se os campos estão corretos.
    '''
    for keys in dict_:
        if keys not in ["Gêneros","Instrumentos"]:
            raise 

def modificar_musicos(arquivo:str,header:dict)->None:
    '''
        Recebe uma string com o arquivo com a base de músicos e um dicionário com o cabeçalho do arquivo.
        Altera a base de músicos a reescrevendo.
    '''
    nova_busca=input("Digite o e-mail do Músico para alterar os dados cadastrais:\n ")

    with open(arquivo,'r') as file:
        leitura=csv.DictReader(file,skipinitialspace=True,delimiter=';', lineterminator='\n')
        lista_modifica=[]
        header=leitura.fieldnames

        for k in leitura:
            lista_modifica.append(k)

        flag_email=False

        for l in lista_modifica:

            if l["Email"]==nova_busca:
                
                flag_email=True
                print("Valores cadastrados:\n",l)
                alteracoes=input("Digite os novos valores seguindo o formato Gêneros:Rock,Folk;Instrumentos:Guitarra,Baixo\n").title()
                
                try:
                    dict_altera=dict((x.split(":")) for x in alteracoes.split(";"))
                    verifica_alteracao(dict_altera)
                except:
                    print("\nValores de entrada incorretos, por favor tente novamente\n")
                    return

                for keys,values in dict_altera.items():
                    dict_altera[keys]=values.split(",")
                    lista_modifica[lista_modifica.index(l)][keys]=dict_altera[keys]

        if not flag_email:
            print("Músico não encontrado, tente novamente")
        else:
            with open(arquivo,'w') as file2:
                escrita=csv.DictWriter(file2,skipinitialspace=True,delimiter=';', lineterminator='\n',fieldnames=header)
                escrita.writeheader()
                escrita.writerows(lista_modifica)
                print("Alteração feita com sucesso")

def combs(lista_combs:list,n:int) ->list:
    '''
        Recebe uma lista_combs 1D que contenha todos os possíveis músicos e o instrumento que toca,
        recebe também uma variável n indicando a quantidade de integrantes da banda
        retorna um vetor contendo as possíveis combinações
    '''
    if n == 0:
        return [[]]
    saida=[]
    for j in range(len(lista_combs)):
        for i in combs(lista_combs[j+1:],n-1):
            saida.append([lista_combs[j],*i])
    return saida

def combinacao(lista_combs:list,n:int) ->list:
    '''
        Recebe uma lista_combs 1D que contenha todos os possíveis músicos e o instrumento que toca,
        recebe também uma variável n indicando a quantidade de integrantes da banda
        retorna um vetor contendo as possíveis combinações
    '''
    receba=combs(lista_combs,n)
    lista_final=[]
    for k in receba:
        lista_repetidos=[]
        lista_repetidos2=[]
        repetido=False
        for j in k:
            if j[1] in lista_repetidos or j[0] in lista_repetidos2: 
                #verifica se tem o nome repetido j[0] na nova combinação ou se tem o instrumento repetido j[1]
                repetido=True
                break
            lista_repetidos.append(j[1])
            lista_repetidos2.append(j[0])
        if repetido==False:
            #se não tem repetido adiciona na lista final
            lista_final.append(k)
    return lista_final

def montar_bandas(arquivo:str) ->None:
    '''
        Recebe uma string com o arquivo com a base de músicos.
        printa as possíveis combinações de acordo com a entrada do usuário.
    '''

    entrada_genero=input('Digite o Gênero desejado: ').title()
    entrada_qtde=int(input('Digite a quantidae de integrantes: '))
    entrada_instrumento=[]
    
    for _ in range(entrada_qtde):
        entrada_instrumento.append(input(f"Digite o instrumento do {_+1}º músico: ").title())
    
    with open(arquivo,'r') as file:
        leitura=csv.DictReader(file,skipinitialspace=True,delimiter=';', lineterminator='\n')
        possibilidades=[]
        for l in leitura:
            if entrada_genero in l["Gêneros"]:
                for i in range(len(entrada_instrumento)):
                    if entrada_instrumento[i] in l["Instrumentos"]:
                        possibilidades.append([l["Email"],entrada_instrumento[i]])

    possi_result=combinacao(possibilidades,entrada_qtde)
    for x in possi_result:
        print(' + '.join(str(e) for e in x))

def verifica_arquivo(arquivo:str) ->dict:
    '''
        Verifica se o arquivo existe.
    '''
    try:
        with open(arquivo,'r') as file2:
            leitura=csv.DictReader(file2,skipinitialspace=True,delimiter=';', lineterminator='\n')
            header=leitura.fieldnames
        return header
    
    except:
        print("arquivo não encontrado.")
        return

def Menu():

    Entrada=7
    print("\nDigite o nome arquivo a ser analisado com a respectiva extensão .csv: ")
    arquivo=input()
    header=verifica_arquivo(arquivo)

    while Entrada in range(1,8) and header!=None:
        
        try:
            Entrada=int(input("\n O que deseja fazer?\n 1-Cadastrar músicos\n 2-Buscar músicos\n 3-Modificar músicos\n 4-Montar bandas\n 5-Alterar arquivo \n 6-Sair\n"))
        except:
            print("Valor inválido, por favor tente novamente\n")
            Entrada=7

        if Entrada==1:
            cadastrar_musicos(arquivo,header)
        elif Entrada==2:
            try:
                print(*buscar_musicos(arquivo),sep='\n')
            except:
                pass 
        elif Entrada==3:
            modificar_musicos(arquivo,header)
        elif Entrada==4:
            montar_bandas(arquivo)
        elif Entrada==6:
            break
        elif Entrada==5:
            print("Digite o nome do novo arquivo a ser analisado com a respectiva extensão .csv: ")
            arquivo=input()
            header=verifica_arquivo(arquivo)
        elif Entrada not in range(1,8):
            print("Valor inválido, por favor tente novamente\n")
            Entrada=7
    print("Saída com sucesso")
Menu()