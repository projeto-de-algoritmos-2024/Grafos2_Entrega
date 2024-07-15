from node import Node
import itertools
import pygame
import heapq
import json
import sys


def dijkstra(graph, source, destinations):
    # Initialize distances, previous nodes, and visited nodes
    distances = {node.number: float('inf') for node in graph}
    previous = {node.number: None for node in graph}
    distances[source] = 0
    visited = set()
    visited_count = 0

    while visited_count < len(graph):
        # Find the node with the minimum distance
        min_distance = float('inf')
        min_node = None
        for node in graph:
            if node.number not in visited and distances[node.number] < min_distance:
                min_distance = distances[node.number]
                min_node = node

        if min_node is None:
            break

        # Mark the node as visited
        visited.add(min_node.number)
        visited_count += 1

        # Update distances to neighboring nodes
        for neighbor, weight in min_node.neighbors:
            distance = distances[min_node.number] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = min_node.number

    # Build the result with distances and paths
    result = {}
    for node in destinations:
        path = []
        current = node
        while current is not None and current != source:
            path.append(current)
            current = previous[current]
        path.reverse()
        result[node] = (distances[node], path)

    return result


def abstract_graph(graph, destinations):
    results = {}
    for destination in destinations:
        result = dijkstra(graph, destination, destinations)
        # Remove the destination node from the result
        del result[destination]
        results[destination] = result

    # Create the second graph using the results
    abstract_graph = {}
    for source, result in results.items():
        for destination, (distance, path) in result.items():
            if source not in abstract_graph:
                abstract_graph[source] = {}
            abstract_graph[source][destination] = (distance, path)
    
    return abstract_graph


# def prim(graph):
#     mst = {}
#     visited = set()
#     start_node = list(graph.keys())[0]
#     priority_queue = [(0, start_node, None)]

#     while priority_queue:
#         weight, node, parent = heapq.heappop(priority_queue)
#         if node in visited:
#             continue
#         visited.add(node)
#         if parent is not None:
#             if parent not in mst:
#                 mst[parent] = {}
#             mst[parent][node] = (weight, graph[parent][node][1])  # Include the path in the result

#         for neighbor, (edge_weight, path) in graph[node].items():
#             if neighbor not in visited:
#                 heapq.heappush(priority_queue, (edge_weight, neighbor, node))

#     return mst

def shortest_path(graph, source):
    # Generate all possible permutations of the destinations excluding the source
    destinations = [node for node in graph.keys() if node != source]
    permutations = itertools.permutations(destinations)

    # Initialize the minimum distance and path
    min_distance = float('inf')
    min_path = None

    # Iterate through each permutation
    for permutation in permutations:
        distance = 0
        path = []
        visited = set()
        visited.add(source)
        current_node = source

        # Calculate the total distance and path for the current permutation
        for destination in permutation:
            if current_node in graph and destination in graph[current_node] and destination not in visited:
                distance += graph[current_node][destination][0]
                path.extend(graph[current_node][destination][1])
                visited.add(destination)
                current_node = destination
            else:
                distance = float('inf')
                break

        # Return to the source to complete the cycle
        if current_node in graph and source in graph[current_node]:
            distance += graph[current_node][source][0]
            path.extend(graph[current_node][source][1])
        else:
            distance = float('inf')

        # Check if the current permutation has a shorter distance
        if distance < min_distance:
            min_distance = distance
            min_path = path

    return min_distance, min_path

def main(destinations):
    nodes = []

    with open('./json/nodes.json') as json_file:
        data = json.load(json_file)
        for node in data['nodes']:
            # print(Node(node).neighbors)
            nodes.append(Node(node))

    farmacy = destinations[0]
    # print(destinations)
    # print(f"Shortest path from the farmacy to the houses: {destinations[1:]}")
    # print(shortest_path(abstract_graph(nodes, destinations), farmacy))
    return shortest_path(abstract_graph(nodes, destinations), farmacy)
