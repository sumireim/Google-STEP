from anagram_1 import Anagram
import sys

def main():
    
    dict_file = "../words.txt"
    input_file = sys.argv[1]
    
    finder = Anagram(dict_file)
    
    try:
        with open(input_file, 'r') as f:
            for line in f:
                input_word = line.strip()
                if input_word:
                    anagrams = finder.find_anagrams(input_word)
                    for anagram in anagrams:
                        print(anagram, end=' ')
                print()          
            
    except FileNotFoundError:
        print(f"Dictionary file {dict_file} not found.")
    
if __name__ == "__main__":
    main()


