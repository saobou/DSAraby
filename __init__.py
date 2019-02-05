import json,os,codecs
class DSAraby:
    def __init__(self):
        self.load_mapping()
        self.letters_to_ret = set()
    
    
    def load_mapping(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.en_to_ar = json.loads(open(dir_path+'/assets/mapping.manual.json', encoding='utf-8').read())
        self.NWORDS = {}
        word_counts = codecs.open(dir_path+'/assets/corpus.txt', encoding='utf-8').read().split("\n")
        for word_count in word_counts:
            if word_count:
                [word, n] = word_count.split()
                if word is None or n is None:
                    pass
                else:
                    self.NWORDS[word] = int(n)

    
    def transliterate(self,sentence, verbose=False):
        words = sentence.split()
        ret = []
        for word in words:
            candidates = list(self.transliterate_word(word))
            best_candidates = self.sort_by_frequency(candidates)
            if len(best_candidates) > 0:
                ret.append(self.sort_by_frequency(candidates)[0])
            else:
                ret.append(word)
        return ' '.join(ret)
    
    def transliterate_word(self,word):
        ret = self.transliterate_letter(word,'',True)
        self.letters_to_ret = set()
        return ret
    
    def transliterate_letter(self,letters, word, begin='start'):
        if len(letters) == 0:
            self.letters_to_ret.add(word)
            return
        
        if begin == 'start':
            table = self.en_to_ar['start']
        elif begin == 'other':
            table = self.en_to_ar['other']
        else :
            table = self.en_to_ar['end']
        max_key_len = len(max(list(table), key=len))
        for i in range(1, max_key_len + 1):
            l = letters[:i]
            if l in table:
                for ar in table[l]:
                    self.transliterate_letter(letters[i:], word + ar,'start')
        
        return self.letters_to_ret
    
    def sort_by_frequency(self,candidates): 
        return sorted(candidates, key=lambda k: self.NWORDS.get(k,0), reverse=True)