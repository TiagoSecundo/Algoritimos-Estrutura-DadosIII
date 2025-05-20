import heapq  # Importa a biblioteca para manipulação de filas de prioridade (heap)
from collections import Counter  # Importa a biblioteca para contar elementos em coleções
import os  # Importa a biblioteca para manipulação de arquivos e diretórios

# Classe para representar um nó na árvore de Huffman
class No:
    def __init__(self, char=None, freq=0):
        # Inicializa o nó com um caractere (char) e sua frequência (freq)
        self.char = char  # Caractere que o nó representa (None para nós internos)
        self.freq = freq  # Frequência associada ao nó
        self.esquerda = None  # Referência para o filho esquerdo
        self.direita = None  # Referência para o filho direito

    def __lt__(self, outro):
        # Define como comparar dois nós pelo atributo frequência (necessário para usar no heap)
        return self.freq < outro.freq

# Função para criar a árvore de Huffman
def criar_arvore_huffman(frequencias):
    # Cria uma lista de nós com base nas frequências dos caracteres
    heap = [No(char, freq) for char, freq in frequencias.items()]
    heapq.heapify(heap)  # Converte a lista em um heap (min-heap)

    # Combina os dois nós de menor frequência até sobrar apenas um nó (a raiz)
    while len(heap) > 1:
        no1 = heapq.heappop(heap)  # Remove o nó com a menor frequência
        no2 = heapq.heappop(heap)  # Remove o segundo menor nó
        combinado = No(freq=no1.freq + no2.freq)  # Cria um novo nó com a soma das frequências
        combinado.esquerda = no1  # Define o primeiro nó como filho esquerdo
        combinado.direita = no2  # Define o segundo nó como filho direito
        heapq.heappush(heap, combinado)  # Adiciona o novo nó de volta ao heap

    return heap[0]  # Retorna o único nó restante, que é a raiz da árvore

# Função para gerar os códigos de Huffman
def gerar_codigos(no, prefixo="", codigos=None):
    if codigos is None:  # Inicializa o dicionário de códigos, se necessário
        codigos = {}
    if no.char:  # Verifica se o nó é uma folha (possui um caractere associado)
        codigos[no.char] = prefixo  # Associa o caractere ao prefixo atual (o código)
    else:
        # Recursivamente percorre a árvore adicionando "0" para a esquerda e "1" para a direita
        if no.esquerda:
            gerar_codigos(no.esquerda, prefixo + "0", codigos)
        if no.direita:
            gerar_codigos(no.direita, prefixo + "1", codigos)
    return codigos  # Retorna o dicionário com os códigos gerados

# Função para compactar um arquivo
def compactar(arquivo_entrada, arquivo_saida):
    # Verifica se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print("Erro: Arquivo de entrada não encontrado!")
        return False

    with open(arquivo_entrada, "r") as f:  # Abre o arquivo no modo leitura
        texto = f.read()  # Lê todo o conteúdo do arquivo

    # Verifica se o arquivo de entrada está vazio
    if not texto:
        print("Erro: O arquivo de entrada está vazio!")
        return False

    # Conta as frequências dos caracteres no texto
    frequencias = Counter(texto)
    # Cria a árvore de Huffman com base nas frequências
    raiz = criar_arvore_huffman(frequencias)
    # Gera os códigos de Huffman para cada caractere
    codigos = gerar_codigos(raiz)

    # Codifica o texto usando os códigos de Huffman
    texto_codificado = "".join(codigos[char] for char in texto)
    sobra = 8 - len(texto_codificado) % 8  # Calcula os bits necessários para alinhar a 8 bits
    texto_codificado += "0" * sobra  # Adiciona os bits extras ao final

    # Salva o texto compactado no arquivo de saída
    with open(arquivo_saida, "wb") as f:  # Abre o arquivo no modo binário
        f.write(bytes([sobra]))  # Grava o número de bits extras no início do arquivo
        for i in range(0, len(texto_codificado), 8):  # Processa o texto em blocos de 8 bits
            f.write(bytes([int(texto_codificado[i:i+8], 2)]))  # Converte cada bloco em um byte e grava

    # Salva um log com informações da compactação
    with open("progresso_compactacao.txt", "w") as f:
        f.write("Compactação concluída.\n")
        f.write(f"Tamanho original: {len(texto)} caracteres\n")
        f.write(f"Tamanho compactado: {len(texto_codificado) // 8} bytes\n")
        f.write("Códigos de Huffman:\n")
        for char, codigo in codigos.items():
            f.write(f"'{char}': {codigo}\n")

    print("Arquivo compactado com sucesso!")
    print("Progresso salvo em 'progresso_compactacao.txt'.")
    return True  # Indica que a operação foi concluída com sucesso

# Função para descompactar um arquivo
def descompactar(arquivo_compactado, arquivo_saida):
    # Verifica se o arquivo compactado existe
    if not os.path.exists(arquivo_compactado):
        print("Erro: Arquivo compactado não encontrado!")
        return False

    with open(arquivo_compactado, "rb") as f:  # Abre o arquivo no modo binário
        sobra = ord(f.read(1))  # Lê o número de bits extras do primeiro byte
        dados = f.read()  # Lê os dados compactados restantes
        texto_binario = "".join(f"{byte:08b}" for byte in dados)  # Converte os bytes em string binária
        texto_binario = texto_binario[:-sobra]  # Remove os bits extras

    # Reconstrói a árvore de Huffman a partir do texto original
    with open("entrada.txt", "r") as f:  # Lê o texto original
        texto_original = f.read()
    frequencias = Counter(texto_original)  # Conta as frequências dos caracteres
    raiz = criar_arvore_huffman(frequencias)  # Cria a árvore de Huffman

    # Decodifica o texto binário usando a árvore de Huffman
    no_atual = raiz
    texto_decodificado = []
    for bit in texto_binario:  # Percorre cada bit no texto binário
        no_atual = no_atual.esquerda if bit == "0" else no_atual.direita  # Navega na árvore
        if no_atual.char:  # Verifica se alcançou uma folha
            texto_decodificado.append(no_atual.char)  # Adiciona o caractere correspondente
            no_atual = raiz  # Reinicia na raiz para o próximo caractere

    # Salva o texto decodificado no arquivo de saída
    with open(arquivo_saida, "w") as f:
        f.write("".join(texto_decodificado))  # Concatena os caracteres e grava no arquivo

    print(f"Arquivo descompactado com sucesso! Salvo como '{arquivo_saida}'.")
    return True  # Indica que a operação foi concluída com sucesso


# Menu principal
def menu():
    compactado = False

    while True:
        print("\nMenu:")
        print("1. Compactar")
        print("2. Descompactar")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            if compactado:
                print("Erro: O texto já está compactado. Descompacte antes de compactar novamente.")
            else:
                sucesso = compactar("entrada.txt", "saida.huf")
                if sucesso:
                    compactado = True
        elif opcao == "2":
            if not compactado:
                print("Erro: Nenhum arquivo compactado disponível. Compacte antes de descompactar.")
            else:
                sucesso = descompactar("saida.huf", "entradadescomprimida.txt")
                if sucesso:
                    compactado = False
        elif opcao == "3":
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()