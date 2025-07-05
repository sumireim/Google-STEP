#!/usr/bin/env python3

import sys
import math
import random

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
            for j in range(i + 2, len(tour)):
                print(f"Trying edges ({i}, {j})")
                
                # 経路の一部を反転
                new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
                new_distance = total_distance(cities, new_tour)
                
                if new_distance < best_distance:# 新しい経路がより短い場合
                    best_tour = new_tour
                    best_distance = new_distance
                    improved = True
                    tour = best_tour
                    break
            if improved:
                break
    return best_tour

class GeneticAlgorithm:
    """遺伝的アルゴリズム"""
    
    def __init__(self, cities, population_size=100, generations=300, mutation_rate=0.2, tournament_size=3):
        self.cities = cities
        self.n = len(cities)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        
        # 距離行列を事前計算
        self.dist_matrix = self._compute_distance_matrix()
    
    def _compute_distance_matrix(self):
        """距離行列を事前計算"""
        N = self.n
        dist = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(i, N):
                dist[i][j] = dist[j][i] = distance(self.cities[i], self.cities[j])
        return dist
    
    def greedy_from_start(self, start_city):
        """指定した開始都市からのグリーディ法"""
        current_city = start_city
        unvisited_cities = set(range(self.n))
        unvisited_cities.remove(start_city)
        tour = [current_city]
        
        while unvisited_cities:
            next_city = min(unvisited_cities,
                           key=lambda city: self.dist_matrix[current_city][city])
            unvisited_cities.remove(next_city)
            tour.append(next_city)
            current_city = next_city
        
        return tour
    
    def nearest_neighbor_with_random_start(self):
        """ランダムな開始点での最近傍法"""
        start_city = random.randint(0, self.n - 1)
        return self.greedy_from_start(start_city)
    
    def two_opt_limited(self, tour, max_iterations=10):
        """制限付き2-opt改善法"""
        best_tour = tour[:]
        best_distance = total_distance(self.cities, best_tour)
        
        iteration = 0
        improved = True
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            for i in range(len(tour) - 1):
                for j in range(i + 2, len(tour)):
                    if j == len(tour) - 1 and i == 0:
                        continue
                    
                    new_tour = tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]
                    new_distance = total_distance(self.cities, new_tour)
                    
                    if new_distance < best_distance:
                        best_tour = new_tour
                        best_distance = new_distance
                        improved = True
                        tour = best_tour
                        break
                if improved:
                    break
        
        return best_tour
    
    def create_random_tour(self):
        """ランダムな経路を生成"""
        tour = list(range(self.n))
        random.shuffle(tour)
        return tour
    
    def tournament_selection(self, population):
        """トーナメント選択"""
        tournament = random.sample(population, self.tournament_size)
        best = min(tournament, key=lambda tour: total_distance(self.cities, tour))
        return best
    
    def order_crossover(self, parent1, parent2):
        """順序交叉"""
        n = len(parent1)
        
        # 交叉点を選択
        start = random.randint(0, n - 2)
        end = random.randint(start + 1, n - 1)
        
        # 子供を初期化
        child1 = [-1] * n
        child2 = [-1] * n
        
        # 選択された区間をコピー
        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]
        
        # 残りの都市を埋める
        def fill_remaining(child, parent_other):
            remaining = []
            for city in parent_other:
                if city not in child:
                    remaining.append(city)
            
            pos = 0
            for city in remaining:
                while child[pos] != -1:
                    pos += 1
                child[pos] = city
        
        fill_remaining(child1, parent2)
        fill_remaining(child2, parent1)
        
        return child1, child2
    
    def mutate(self, tour):
        """突然変異（2-opt風の変異）"""
        tour = tour[:]  # コピーを作成
        if random.random() < self.mutation_rate:
            n = len(tour)
            i = random.randint(0, n - 2)
            j = random.randint(i + 1, n - 1)
            tour[i:j+1] = tour[i:j+1][::-1]
        return tour
    
    def create_better_initial_population(self):
        """より良い初期集団を生成"""
        population = []
        
        # グリーディ法ベースの個体（25%）
        greedy_tour = self.greedy_from_start(0)  # 都市0から開始
        population.append(greedy_tour)
        
        # グリーディの変種（異なる開始点）
        for _ in range(self.population_size // 4 - 1):
            start_city = random.randint(0, self.n - 1)
            tour = self.greedy_from_start(start_city)
            population.append(tour)
        
        # 最近傍法の変種（25%）
        for _ in range(self.population_size // 4):
            tour = self.nearest_neighbor_with_random_start()
            population.append(tour)
        
        # 2-optで改善したランダム解（25%）
        for _ in range(self.population_size // 4):
            tour = self.create_random_tour()
            tour = self.two_opt_limited(tour, max_iterations=10)
            population.append(tour)
        
        # 完全ランダム（25%）
        for _ in range(self.population_size - len(population)):
            population.append(self.create_random_tour())
        
        return population
    
    def solve(self):
        """遺伝的アルゴリズムでTSPを解く"""
        # 初期集団を生成
        population = self.create_better_initial_population()
        
        best_tour = None
        best_distance = float('inf')
        
        for generation in range(self.generations):
            # 新しい世代を作成
            new_population = []
            
            current_best = min(population, key=lambda tour: total_distance(self.cities, tour))
            current_distance = total_distance(self.cities, current_best)
            
            if current_distance < best_distance:
                best_tour = current_best[:]
                best_distance = current_distance
                if generation % 100 == 0:
                    print(f"Generation {generation}: Best distance = {best_distance:.2f}")
            
            new_population.append(best_tour[:])
            
            # 残りの個体を生成
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(population)
                parent2 = self.tournament_selection(population)
                
                child1, child2 = self.order_crossover(parent1, parent2)
                
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            population = new_population
        
        return best_tour

def greedy(cities, start_city=0):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = start_city
    unvisited_cities = set(range(N))
    unvisited_cities.remove(start_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    
    return tour

def solve(cities):
    N = len(cities)
    
    if N <= 16:
        # 極小問題は全数探索
        best_tour = None
        best_distance = float('inf')
        
        for _ in range(min(100, N * 2)):
            tour = list(range(N))
            random.shuffle(tour)
            tour = two_opt(cities, tour)
            distance = total_distance(cities, tour)
            
            if distance < best_distance:
                best_distance = distance
                best_tour = tour
        
        return best_tour
    
    elif N <= 512:
        best_tour = None
        best_distance = float('inf')
        num_starts = min(20, N)
        
        for start_city in range(num_starts):
            # グリーディ法
            tour = greedy(cities, start_city)
            # 2-opt改善
            tour = two_opt(cities, tour)
            # 距離を計算
            distance = total_distance(cities, tour)
            
            if distance < best_distance:
                best_distance = distance
                best_tour = tour[:]
        return best_tour
        
    # 大きな問題に対しては遺伝的アルゴリズムを使用
    else:
        # 遺伝的アルゴリズムのパラメータを調整
        population_size = min(100, N * 2)
        generations = min(1000, N * 5)
        
        ga = GeneticAlgorithm(cities, population_size, generations)
        tour = ga.solve()
        return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
