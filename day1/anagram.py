class Anagram:
    def __init__(self, dict_file):
        self.words = []
        self.word_signatures = {} 
        self.sort_dict(dict_file)

    def sort_dict(self, dict_file):
        """
        辞書ファイルを読み込んで、ソートされた文字列（signature）を取得
        """
        try:
            with open(dict_file, 'r') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.words.append(word)
                        signature = ''.join(sorted(word))
                        
                    if signature not in self.word_signatures:
                        self.word_signatures[signature] = []
                    self.word_signatures[signature].append(word)
                    
        except FileNotFoundError:
            print(f"Dictionary file {dict_file} not found.")
    
    def find_anagrams(self, input_word):
        """
        入力された単語のアナグラムを検索
        """
        input_signature = ''.join(sorted(input_word))
        anagrams = self.word_signatures.get(input_signature, [])
        result = [word for word in anagrams if word != input_word]
        return result
