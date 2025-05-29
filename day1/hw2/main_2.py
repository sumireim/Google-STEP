from anagram_2 import BroadAnagram
from score_count import ScoreCount
import sys

def main():
    
    dict_file = "../words.txt" 
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    
    finder = BroadAnagram(dict_file)
    counter = ScoreCount(finder.words)
    
    try:
        with open(input_file, 'r') as f:
            if output_file:
                with open(output_file, 'a') as out_f:
                    total = 0
                    for line in f:
                        input_word = line.strip()
                        if input_word:
                            anagrams = finder.find_anagrams(input_word)
                            if not anagrams:
                                print(f"No anagrams found for '{input_word}'", end=' ')
                            best_anagram, max_score = counter.calculate_score(anagrams)
                            total += max_score
                        else:
                            print("Empty input word", end=' ')
                
                        out_f.write(f"{input_word}: {best_anagram}\n")
            print(f"Total score: {total}")      
            
    except FileNotFoundError:
        print(f"Dictionary file {dict_file} not found.")
    
if __name__ == "__main__":
    main()


