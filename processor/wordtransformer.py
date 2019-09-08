import os
import logging

from .dictionary import load_dictionary

logger = logging.getLogger(__name__)

class WordTransformer(object):
    verb_to_present_dict = dict()
    noun_to_singular_dict = dict()

    def __init__(self, resource_path, to_present=True, to_singular=True):
        logger.info("Initializing WordTransformer")
        verbs_file_path = os.path.join(resource_path, "verbs.csv")
        with open(verbs_file_path) as fp:
            for line in fp.readlines():
                fields = line.strip().split(',')
                if len(fields) == 0:
                    continue
                present_tense = fields[0]
                if len(present_tense) == 0:
                    continue
                for field in fields:
                    if (len(field) > 0):
                        self.verb_to_present_dict[field] = present_tense

        nouns_file_path = os.path.join(resource_path, "nouns.csv")
        with open(nouns_file_path) as fp:
            for line in fp.readlines():
                fields = line.strip().split(',')
                if len(fields) != 2:
                    continue
                self.noun_to_singular_dict[fields[1]] = fields[0]
        
        dictionary_path = os.path.join(resource_path, "dictionary")
        self.dictionary = load_dictionary(dictionary_path)

    def transform(self, word):
        if word.endswith("'"):
            word = word[:-1]
        if word.endswith("'s"):
            word = word[:-2]
        
        if word in self.dictionary:
            return word
        if word in self.verb_to_present_dict:
            return self.verb_to_present_dict[word]
        if word.lower() in self.verb_to_present_dict:
            return self.verb_to_present_dict[word.lower()]
        if word in self.noun_to_singular_dict:
            return self.noun_to_singular_dict[word]
        if word.lower() in self.noun_to_singular_dict:
            return self.noun_to_singular_dict[word.lower()]

        return word
