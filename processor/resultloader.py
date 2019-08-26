import os

def load_sentences(sentences_file: str):
    with open(sentences_file) as fp:
        sentences = list(fp.readlines())
    return sentences

def load_vocabulary(vocabulary_file: str):
    word_sources_list = []
    with open(vocabulary_file) as fp:
        for l in fp.readlines():
            fields = l.strip().split(',')
            word = fields[0]
            freq = int(fields[1])
            sources = [int(x) for x in fields[2].split("$$")]
            word_sources_list.append((word, freq, sources))

    return word_sources_list