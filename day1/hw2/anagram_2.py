class BroadAnagram:
    def __init__(self, dict_file):
        self.words = []
        self.char_count = {} 
        self.search_dict(dict_file)

    def search_dict(self, dict_file):
        """
        辞書ファイルを読み込んで、それぞれのアルファベットをカウント
        """
        try:
            with open(dict_file, 'r') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.words.append(word)
                        dict_set = self.count_characters(word)
                        self.char_count[word] = dict_set
                    
        except FileNotFoundError:
            print(f"Dictionary file {dict_file} not found.")
    
    def find_anagrams(self, input_word):
        """
        入力された単語の広義アナグラムを検索
        """
        input_set = self.count_characters(input_word)
        anagrams = []
        for word in self.words:
            if word != input_word:
                word_chars = self.char_count[word]
                if self.can_form_word(input_set, word_chars):
                    anagrams.append(word)
        return anagrams
    
    def count_characters(self, word):
        """
        単語の各文字の出現回数をカウント
        """
        char_count = {}
        for c in word:
            if c in char_count:
                char_count[c] += 1
            else:
                char_count[c] = 1
        return char_count
    
    def can_form_word(self, available_chars, needed_chars):
        """
        出現回数で、部分アナグラムができるかを判定
        """
        for char, needed_count in needed_chars.items():
            if available_chars.get(char, 0) < needed_count:
                return False
        return True