import re
import os
import logging

logger = logging.getLogger(__name__)

class WordFilter(object):

    sieve = set()

    def __init__(self, resource_path, filter_simple_words=True, filter_known_words=True):
        logger.info("Initializing WordFilter")
        if filter_simple_words:
            with open(os.path.join(resource_path, "primary_school_vocabulary.txt")) as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

            with open(os.path.join(resource_path, "middle_school_vocabulary.txt")) as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

            with open(os.path.join(resource_path, "other_simple_words.txt")) as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

            with open(os.path.join(resource_path, "stopwords.txt")) as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

        if filter_known_words:
            with open(os.path.join(resource_path, "known_words.txt")) as f:
                for line in f.readlines():
                    self.sieve.add(line.strip())

    def passed(self, word):
        return len(word) > 0 and (word not in self.sieve) and (word.lower() not in self.sieve)
