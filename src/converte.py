from json import dump
from constantes import mapa
from copy import deepcopy

nodes = []
node_count = 1
node_positions = {}
mapa = deepcopy(mapa)

# Atribuindo números aos nós e registrando suas posições no mapa
for i, linha in enumerate(mapa):
    for j, celula in enumerate(linha):
        if celula == 'rh' or celula == 'rv':
            node_positions[(i, j)] = node_count
            nodes.append({
                "number": node_count,
                "neighbors": [],
                "houses": []
            })
            node_count += 1

# Função para verificar se uma posição está dentro do mapa e não é uma estrada
def posicao_valida(i, j):
    return 0 <= i < len(mapa) and 0 <= j < len(mapa[i])

# Determinando os vizinhos
for (i, j), node_number in node_positions.items():
    neighbors = [
        (i-1, j),  # Cima
        (i+1, j),  # Baixo
        (i, j-1),  # Esquerda
        (i, j+1)   # Direita
    ]
    for ni, nj in neighbors:
        if posicao_valida(ni, nj):
            if mapa[ni][nj] in ['rh', 'rv']:
                neighbor_node_number = node_positions.get((ni, nj))
                if neighbor_node_number:
                    nodes[node_number-1]["neighbors"].append({
                        "neighbor": neighbor_node_number,
                        "weight": 1
                    })


# Adicionando casas aos nós
for i, linha in enumerate(mapa):
    for j, celula in enumerate(linha):
        if celula.isdigit():
            for ni, nj in [
                (i-1, j), (i+1, j), (i, j-1), (i, j+1)
            ]:
                if (ni, nj) in node_positions:
                    node_number = node_positions[(ni, nj)]
                    nodes[node_number-1]["houses"].append(int(celula))


# Estrutura final do JSON
graph = {
    "nodes": nodes
}

# Salvando em um arquivo JSON
with open('./json/grafo.json', 'w') as arquivo:
    dump(graph, arquivo, indent=4)

print("Arquivo JSON criado com sucesso!")
