import random
import string
import time
import sys
sys.setrecursionlimit(100000)

def gerar_arquivos():  # Gerador de Arquivos Aleatórios
    """Gera arquivos com dados aleatórios (ordenado e não ordenado)."""
    tamanhos = [100, 500, 1000, 5000, 10000]

    for tamanho in tamanhos:
        for ordenado in [True, False]:
            nome = f"arquivo_{tamanho}_{'ordenado' if ordenado else 'nao_ordenado'}.txt"
            dados = [(random.randint(1, 100000), random.randint(1, 100), 
                      ''.join(random.choices(string.ascii_letters, k=1000)))
                     for _ in range(tamanho)]

            if ordenado:
                dados.sort(key=lambda x: x[0])

            with open(nome, 'w') as f:
                for registro in dados:
                    f.write(f"{registro[0]} {registro[1]} {registro[2]}\n")

# Gera os arquivos necessários
gerar_arquivos()

def ler_arquivo(nome):  # Leitura dos Arquivos
    """Lê os dados do arquivo e retorna uma lista."""
    with open(nome, 'r') as f:
        return [tuple(line.split(maxsplit=2)) for line in f]

def buscar(arvore, valor, comp=0):  # Funções de Busca
    """Busca um valor na árvore binária e retorna o número de comparações."""
    comp += 1
    if arvore is None:
        return None, comp  # Não encontrado
    elif valor < arvore[0]:
        return buscar(arvore[1], valor, comp)
    elif valor > arvore[0]:
        return buscar(arvore[2], valor, comp)
    else:
        return arvore, comp  # Encontrado

def buscar_avl(arvore, valor, comp=0):
    """Busca um valor na árvore AVL e retorna o número de comparações."""
    comp += 1
    if arvore is None:
        return None, comp  # Não encontrado
    elif valor < arvore[0]:
        return buscar_avl(arvore[1], valor, comp)
    elif valor > arvore[0]:
        return buscar_avl(arvore[2], valor, comp)
    else:
        return arvore, comp  # Encontrado

def buscar_sequencial(lista, valor):  # Implementação da busca sequencial
    """Realiza uma busca sequencial em uma lista e retorna o número de comparações."""
    comp = 0
    for item in lista:
        comp += 1
        if item[0] == valor:
            return item, comp  # Encontrado
    return None, comp  # Não encontrado

def inserir(arvore, valor):  # Funções de Construção das Árvores
    """Insere um valor na árvore binária, evitando duplicatas."""
    if arvore is None:
        return [valor, None, None]
    elif valor < arvore[0]:
        arvore[1] = inserir(arvore[1], valor)
    elif valor > arvore[0]:  # Modificado para evitar duplicatas
        arvore[2] = inserir(arvore[2], valor)
    # Se valor == arvore[0], não faz nada para evitar duplicatas
    return arvore

def inserir_avl(arvore, valor):
    """Insere um valor na árvore AVL e realiza balanceamento."""
    if arvore is None:
        return [valor, None, None]
    elif valor < arvore[0]:
        arvore[1] = inserir_avl(arvore[1], valor)
    else:
        arvore[2] = inserir_avl(arvore[2], valor)

    # Balanceamento
    fb = altura(arvore[2]) - altura(arvore[1])

    if fb < -1 and valor < arvore[1][0]:
        return rotacao_direita(arvore)
    if fb > 1 and valor > arvore[2][0]:
        return rotacao_esquerda(arvore)
    if fb < -1 and valor > arvore[1][0]:
        arvore[1] = rotacao_esquerda(arvore[1])
        return rotacao_direita(arvore)
    if fb > 1 and valor < arvore[2][0]:
        arvore[2] = rotacao_direita(arvore[2])
        return rotacao_esquerda(arvore)

    return arvore

def altura(arvore):
    """Calcula a altura da árvore."""
    if arvore is None:
        return 0
    return max(altura(arvore[1]), altura(arvore[2])) + 1

def rotacao_direita(y):
    """Executa uma rotação à direita."""
    x = y[1]
    y[1] = x[2]
    x[2] = y
    return x

def rotacao_esquerda(x):
    """Executa uma rotação à esquerda."""
    y = x[2]
    x[2] = y[1]
    y[1] = x
    return y

def medir_tempo_e_comparacoes(funcao_busca, estrutura, chaves):  # Medição de Desempenho
    """Mede o tempo e o número de comparações para uma lista de chaves."""
    comparacoes_totais = 0
    inicio = time.perf_counter()

    for chave in chaves:
        _, comparacoes = funcao_busca(estrutura, chave)
        comparacoes_totais += comparacoes

    tempo_total = time.perf_counter() - inicio
    return comparacoes_totais / len(chaves), tempo_total / len(chaves)

# Função para executar medições para um tamanho específico
def executar_medições(tamanho):
    dados = ler_arquivo(f'arquivo_{tamanho}_ordenado.txt')  # Execução dos Testes

    # Gerar chaves presentes, evitando duplicatas
    chaves_presentes = set()
    while len(chaves_presentes) < 15:
        chave = int(random.choice(dados)[0])
        chaves_presentes.add(chave)

    chaves_presentes = list(chaves_presentes)
    
    # Gerar chaves ausentes
    chaves_ausentes = [random.randint(100001, 200000) for _ in range(15)]

    # Construção da árvore binária
    arvore_bst = None
    for chave, _, _ in dados:
        arvore_bst = inserir(arvore_bst, int(chave))

    # Construção da árvore AVL
    arvore_avl = None
    for chave, _, _ in dados:
        arvore_avl = inserir_avl(arvore_avl, int(chave))

    # Medição de desempenho para BST
    comp_bst_presente, tempo_bst_presente = medir_tempo_e_comparacoes(buscar, arvore_bst, chaves_presentes)
    comp_bst_ausente, tempo_bst_ausente = medir_tempo_e_comparacoes(buscar, arvore_bst, chaves_ausentes)

    # Medição de desempenho para AVL
    comp_avl_presente, tempo_avl_presente = medir_tempo_e_comparacoes(buscar_avl, arvore_avl, chaves_presentes)
    comp_avl_ausente, tempo_avl_ausente = medir_tempo_e_comparacoes(buscar_avl, arvore_avl, chaves_ausentes)

    # Medição de desempenho para Busca Sequencial
    comp_seq_presente, tempo_seq_presente = medir_tempo_e_comparacoes(buscar_sequencial, dados, chaves_presentes)
    comp_seq_ausente, tempo_seq_ausente = medir_tempo_e_comparacoes(buscar_sequencial, dados, chaves_ausentes)

    # Exibição dos resultados
    print(f"\n\nResultados da busca nas árvores:")
    print("_______________________________________\n")
    print("Árvore Binária de Busca :")
    print(f" - Chaves presentes: Média de {comp_bst_presente:.2f} comparações por busca, {tempo_bst_presente:.10f} segundos por busca.")
    print(f" - Chaves ausentes: Média de {comp_bst_ausente:.2f} comparações por busca, {tempo_bst_ausente:.10f} segundos por busca.\n")

    print("Árvore AVL:")
    print(f" - Chaves presentes: Média de {comp_avl_presente:.2f} comparações por busca, {tempo_avl_presente:.10f} segundos por busca.")
    print(f" - Chaves ausentes: Média de {comp_avl_ausente:.2f} comparações por busca, {tempo_avl_ausente:.10f} segundos por busca.\n")

    print("Busca Sequencial:")
    print(f" - Chaves presentes: Média de {comp_seq_presente:.2f} comparações por busca, {tempo_seq_presente:.10f} segundos por busca.")
    print(f" - Chaves ausentes: Média de {comp_seq_ausente:.2f} comparações por busca, {tempo_seq_ausente:.10f} segundos por busca.")

# Testa para os tamanhos desejados
tamanhos = [100, 500, 1000, 5000, 10000]
for tamanho in tamanhos:
    executar_medições(tamanho)
