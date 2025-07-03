#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(cities, tour):
    """経路全体の距離"""
    total = 0
    for i in range(len(tour)):
        total += distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
    return total

def two_opt(cities, tour):
    """2-opt改善法"""
    best_tour = tour[:] # 現在の最良経路
    best_distance = total_distance(cities, best_tour) # 最良距離を記録
    
    improved = True
    while improved: # 改善がある限り繰り返し
        improved = False
        
        # 全ての辺のペアを試行
        for i in range(len(tour) - 1):
            for j in range(i + 1, len(tour)):
                if j == i + 1:
                    continue  # 隣接する辺はスキップ
                
                # 経路の一部を反転
                new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
                new_distance = total_distance(cities, new_tour)
                
                if new_distance < best_distance:
                    best_tour = new_tour
                    best_distance = new_distance
                    improved = True
                    tour = best_tour
                    break
            if improved:
                break
    return best_tour

def greedy(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    
    return tour

def solve(cities):
    
    # Greedy法で初期経路を生成
    tour = greedy(cities)
    
    # 2-opt
    if N <= 512:
        tour = two_opt(cities, tour)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
