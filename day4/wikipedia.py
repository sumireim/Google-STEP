import sys
from collections import deque
import math

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def change_title_to_id(self, title):
        """
        タイトルからIDを取得
        """
        for id, t in self.titles.items():
            if t == title:
                return id
        return None
    
    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = self.change_title_to_id(start)
        goal_id = self.change_title_to_id(goal)
        if start_id is None or goal_id is None:
            print("Start or goal page not found.")
            return None
        queue = deque([start_id]) # キューの初期化
        visited = set([start_id]) # 到達済みのIDを記録
        parent_map = {start_id: None}
        
        while queue:
            current_id = queue.popleft()
            for neighbor_id in self.links[current_id]:
                # print(f"Visiting: {self.titles[current_id]} -> {self.titles[neighbor_id]}")
                if neighbor_id not in visited: # 未訪問のノードの場合
                    visited.add(neighbor_id)
                    parent_map[neighbor_id] = current_id
                    queue.append(neighbor_id)
                    
                    if neighbor_id == goal_id: # ゴールに到達した場合
                        path = []
                        node = neighbor_id
                        while node is not None: # 逆順に親ノードをたどる
                            path.append(node)
                            node = parent_map[node]
                        path.reverse()
                        
                        title_path = [self.titles[id] for id in path] # タイトルのリストを作成
                        print("The shortest path is:")
                        print(" - ".join(title_path)) # タイトルをハイフンで結合して表示
                        print()
                        return path
        return None


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self): # Random Surfer モデル
        tolerance = 1e-6
        ranks = {id: 1.0 for id in self.titles} 
        max_iterations = 100 # 最大反復回数

        for iteration in range(max_iterations): 
            new_ranks = {id: 0.0 for id in self.titles}  
            for id in self.titles:
                out_links = self.links.get(id, [])
                if out_links:
                    share_weight = 0.85 * ranks[id] / len(out_links) # 隣接ノードに分配 85%の重み
                    for target_id in out_links:
                        new_ranks[target_id] += share_weight
                    share_all_weight = 0.15 * ranks[id] / len(self.titles) # 全体に分配 15%の重み
                    for target_id in self.titles:
                        new_ranks[target_id] += share_all_weight
                else:
                    share_all_weight = ranks[id] / len(self.titles) # ページにリンクがない場合は全体に分配
                    for target_id in self.titles:
                        new_ranks[target_id] += share_all_weight
            sum_ranks = sum(new_ranks.values())
            sum_of_squares = sum((new_ranks[id] - ranks[id])**2 for id in self.titles)
            diff = math.sqrt(sum_of_squares)
            if diff < tolerance:
                break
            
            print(sum_ranks)
            ranks = new_ranks
        print("\nThe most popular pages are:")
        top_10 = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (id, rank) in enumerate(top_10, start=1):
            print(f"{i}. {self.titles[id]} (PageRank: {rank:.6f})")
        print()
        


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_shortest_path("パリ", "情報工学")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
