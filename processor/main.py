import re
from nltk.tokenize import sent_tokenize
from wordfilter import WordFilter
from wordtransformer import WordTransformer


if __name__ == "__main__":
    with open("./1984.txt") as fp:
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
    word_transformer = WordTransformer()
    word_filter = WordFilter()
    with open("./sentences.csv", "w") as fp:
        for i, sentence in enumerate(sentences):
            print(f"processing sentence {i}/{len(sentences)}")
            fp.write(sentence + '\n')
            words = prog.findall(sentence)
            words = map(word_transformer.transform, words)
            words = filter(word_filter.passed, words)

            for word in words:
                vocabulary[word] = vocabulary.get(word, 0) + 1
                if word not in word_appearence_dict:
                    word_appearence_dict[word] = []
                word_appearence_dict[word].append(i)

    # merge capital initialed word with lower case one if both appeared
    def lower_inital_letter(word):
        return str(word[0].lower() + word[1:])

    for k, v in vocabulary.items():
        if lower_inital_letter(k) in vocabulary:
            merge_k = lower_inital_letter(k)
        merged_vocabulary[merge_k] = merged_vocabulary.get(merge_k, 0) + v
        merged_word_appearence_dict[merge_k] = merged_word_appearence_dict.get(merge_k, []) + word_appearence_dict[k]

    word_freq_list = list(merged_vocabulary.items())
    word_freq_list.sort(key=lambda x: x[1], reverse=True)
    with open("./vocabulary.csv", 'w') as fp:
        for word, freq in word_freq_list:
            fp.write(f"{word},{freq}, {'$$'.join([str(i) for i in merged_word_appearence_dict[word]])}\n")
