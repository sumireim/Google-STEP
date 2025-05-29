class ScoreCount:
    def __init__(self, words=None):
        self.scores = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
        self.words = words
        
    def count(self, word):
        """
        単語のスコアを計算
        """
        counter = 0
        for character in word:
            if 'a' <= character <= 'z':
                index = ord(character) - ord('a')
                if 0 <= index < len(self.scores):
                    counter += self.scores[index]
        return counter
    def calculate_score(self, anagrams):
        """
        最大スコアのアナグラムを判定
        """
        max_score = 0
        best_anagram = None
        for anagram in anagrams:
            score = self.count(anagram)
            if score > max_score:
                max_score = score
                best_anagram = anagram
        
        return best_anagram, max_score
        