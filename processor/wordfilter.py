import re

class WordFilter(object):

    sieve = set()

    def __init__(self, resource_path, filter_simple_words=True, filter_known_words=True):
        if filter_simple_words:
            with open("./data/primary_school_vocabulary.txt") as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

            with open("./data/middle_school_vocabulary.txt") as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

            with open("./data/other_simple_words.txt") as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

            with open("./data/stopwords.txt") as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

        if filter_known_words:
            with open("./data/known_words.txt") as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

    def passed(self, word):
        return len(word) > 0 and (word not in self.sieve) and (word.lower() not in self.sieve)
