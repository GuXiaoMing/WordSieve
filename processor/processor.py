import os
import re
import logging

from nltk.tokenize import sent_tokenize

from .wordfilter import WordFilter
from .wordtransformer import WordTransformer

logger = logging.getLogger(__name__)

class Processor(object):

    def __init__(self, resource_path, config={}):
        logger.info("Initializing Processor")
        self.word_transformer = WordTransformer(
            resource_path=resource_path,
            to_present=True,
            to_singular=True
        )
        self.word_filter = WordFilter(
            resource_path=resource_path,
            filter_simple_words=True,
            filter_known_words=True
        )
        
    
    def process(self, input_path, output_path):
        # TODO: Support folder input
        with open(input_path) as fp:
            text = fp.read()

        text = text.replace("-\n", "")
        text = text.replace("- \n", "")

        sentences = sent_tokenize(text)
        sentences = list(map(lambda x: x.replace('\n', ''), sentences))

        vocabulary = dict()
        word_appearence_dict = dict()
        merged_vocabulary = dict()
        merged_word_appearence_dict = dict()

        prog = re.compile(r"[a-zA-Z][a-zA-Z|']*")
        sentences_file = os.path.join(output_path, "sentences.csv")
        with open(sentences_file, "w") as fp:
            for i, sentence in enumerate(sentences):
                print(f"processing sentence {i}/{len(sentences)}", end='\r')
                fp.write(sentence + '\n')
                words = prog.findall(sentence)
                words = map(self.word_transformer.transform, words)
                words = filter(self.word_filter.passed, words)

                for word in words:
                    vocabulary[word] = vocabulary.get(word, 0) + 1
                    if word not in word_appearence_dict:
                        word_appearence_dict[word] = []
                    word_appearence_dict[word].append(i)

        # merge capital initialed word with lower case one if both appeared
        def lower_inital_letter(word):
            return str(word[0].lower() + word[1:])

        for k, v in vocabulary.items():
            merge_k = k
            if lower_inital_letter(k) in vocabulary:
                merge_k = lower_inital_letter(k)
            merged_vocabulary[merge_k] = merged_vocabulary.get(merge_k, 0) + v
            merged_word_appearence_dict[merge_k] = merged_word_appearence_dict.get(merge_k, []) + word_appearence_dict[k]

        word_freq_list = list(merged_vocabulary.items())
        word_freq_list.sort(key=lambda x: x[1], reverse=True)
        vocabulary_file = os.path.join(output_path, "vocabulary.csv")
        with open(vocabulary_file, "w") as fp:
            for word, freq in word_freq_list:
                fp.write(f"{word},{freq}, {'$$'.join([str(i) for i in merged_word_appearence_dict[word]])}\n")