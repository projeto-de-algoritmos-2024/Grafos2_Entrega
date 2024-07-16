from node import Node
import itertools
import json
import sys
import pygame
from constantes import *

nodes = []
houses = [0 for _ in range(49)]
deu = False

with open('./json/nodes.json') as json_file:
    data = json.load(json_file)
    for node in data['nodes']:
        n = Node(node)
        nodes.append(n)
        for house in n.houses:
            houses[house] = n.number

def dijkstra(graph, source, destinations):
    distances = {node.number: float('inf') for node in graph}
    previous = {node.number: None for node in graph}
    distances[source] = 0
    visited = set()
    visited_count = 0

    while visited_count < len(graph):
        min_distance = float('inf')
        min_node = None
        for node in graph:
            if node.number not in visited and distances[node.number] < min_distance:
                min_distance = distances[node.number]
                min_node = node

        if min_node is None:
            break

        visited.add(min_node.number)
        visited_count += 1

        for neighbor, weight in min_node.neighbors:
            distance = distances[min_node.number] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = min_node.number

    result = {}
    for node in destinations:
        path = []
        current = node
        while current is not None and current != source:
            path.append(current)
            current = previous[current]
        path.reverse()
        result[node] = (distances[node],
         path)

    return result


def abstract_graph(graph, destinations):
    results = {}
    for destination in destinations:
        result = dijkstra(graph, destination, destinations)
        del result[destination]
        results[destination] = result

    abstract_graph = {}
    for source, result in results.items():
        for destination, (distance, path) in result.items():
            if source not in abstract_graph:
                abstract_graph[source] = {}
            abstract_graph[source][destination] = (distance, path)
    
    return abstract_graph

def shortest_path(graph, source):
    destinations = [node for node in graph.keys() if node != source]
    permutations = itertools.permutations(destinations)

    min_distance = float('inf')
    min_path = None

    for permutation in permutations:
        distance = 0
        path = []
        visited = set()
        visited.add(source)
        current_node = source

        for destination in permutation:
            if current_node in graph and destination in graph[current_node] and destination not in visited:
                distance += graph[current_node][destination][0]
                path.extend(graph[current_node][destination][1])
                visited.add(destination)
                current_node = destination
            else:
                distance = float('inf')
                break

        if current_node in graph and source in graph[current_node]:
            distance += graph[current_node][source][0]
            path.extend(graph[current_node][source][1])
        else:
            distance = float('inf')

        if distance < min_distance:
            min_distance = distance
            min_path = path

    return min_path

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


def draw_path(screen, path, nodes, destinations):
    if deu:
        return
    path.insert(0, FARMACY)
    for i in range(len(path) - 1):
        if path[i] == FARMACY:
            pygame.draw.polygon(screen, (255,0,0), [(nodes[path[i]-1].position[0], nodes[path[i]-1].position[1] - 15), (nodes[path[i]-1].position[0] - 15, nodes[path[i]-1].position[1] + 15), (nodes[path[i]-1].position[0] + 15, nodes[path[i]-1].position[1] + 15)])
        elif path[i] in destinations:
            pygame.draw.circle(screen, (255,0,0), nodes[path[i]-1].position, 15)
        if path[i + 1] is None:
            continue
        pygame.draw.line(screen, (255,0,0), nodes[path[i]-1].position, nodes[path[i+1]-1].position, 5)
        pygame.display.flip()
        pygame.time.wait(1000)
        

def menu(selecionados):
    house_destinations = selecionados
    
    if len(house_destinations) == 0:
        return None

    destinations = [FARMACY]
    for house in house_destinations:
        destinations.append(houses[house])

    return destinations
    
selecionados = []


def desenha_legenda(WIDTH, font, screen):
    alinhamento_lateral = WIDTH + 30
    mensagem = f'Casas selecionadas:'
    formatado2 = font.render(mensagem, False, PRETO)
    screen.blit(formatado2, (alinhamento_lateral, 5))
    mensagem = f'{selecionados}'
    formatado2 = font.render(mensagem, False, PRETO)
    screen.blit(formatado2, (alinhamento_lateral, 30))



def main():
    global selecionados
    global deu
    pygame.init()
    map_image = pygame.image.load('../img/mapa.png')
    WIDTH, HEIGHT = map_image.get_size()

    screen = pygame.display.set_mode((WIDTH + 300, HEIGHT))
    pygame.display.set_caption("Route Generator")

    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    screen.fill((255,255,255))
    screen.blit(map_image, (0, 0))
    text1 = font.render("ESC para sair", True, BRANCO)
    text2 = font.render("ENTER para iniciar", True, BRANCO)
    text3 = font.render("BACKSPACE para resetar", True, BRANCO)
    text_width = max(text1.get_width(), text3.get_width())
    text_height = text1.get_height() + text2.get_height() + text3.get_height() + 10

    rect = pygame.Rect(20, 15, text_width + 20, text_height)
    
    pygame.draw.rect(screen, (0, 0, 0), rect)
    screen.blit(text1, (30, 20))
    screen.blit(text2, (30, 40))
    screen.blit(text3, (30, 40))
    
    pygame.display.flip()

    running = True
    usuario = False
    tamanho_casa = 60

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for casa in mapa:
                if (x >= mapa[casa][0] and x < mapa[casa][0] + tamanho_casa) and (y >= mapa[casa][1] and y < mapa[casa][1] + tamanho_casa):
                    if casa not in selecionados:
                        selecionados.append(casa)
                        break
                    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            usuario = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            screen.blit(map_image, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), rect)
            screen.blit(text1, (30, 20))
            screen.blit(text2, (30, 40))
            pygame.display.flip()
            usuario = True
            deu = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            usuario = False
            deu = False
            selecionados = []
            
        if not deu:
            screen.fill((255,255,255))
            desenha_legenda(WIDTH, font, screen)
            screen.blit(map_image, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), rect)
            screen.blit(text1, (30, 20))
            screen.blit(text2, (30, 40))
            screen.blit(text3, (30, 60))
        if usuario:
            destinations = menu(selecionados)

            if destinations is None:
                usuario = False
                continue

            path = shortest_path(abstract_graph(nodes, destinations), FARMACY)
            draw_path(screen, path, nodes, destinations)
            deu = True

        pygame.display.flip()

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()
