import json
import os

def load_dictionary(dir_path):
    dictionary = {}
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        with open(file_path) as fp:
            sub_dict = json.load(fp)
            dictionary.update(sub_dict)
    return dictionary


if __name__ == "__main__":
    dictionary = load_dictionary("./data/dictionary")
    print(dictionary.get("fuck"))
    print(dictionary.get("foo"))
    print(dictionary.get("church"))