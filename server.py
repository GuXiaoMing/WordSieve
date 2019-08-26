import os
import json

from flask import Flask
from flask import render_template
import pandas as pd

from processor.resultloader import load_sentences, load_vocabulary
from processor.dictionary import load_dictionary


DATA_PATH = "./data"
SENTENCES_PATH = os.path.join(DATA_PATH, "outputs", "sentences.csv")
VOCABUARY_PATH = os.path.join(DATA_PATH, "outputs", "vocabulary.csv")
DICT_PATH = os.path.join(DATA_PATH, "resources", "dictionary")
sentences = load_sentences(SENTENCES_PATH)
vocabulary = load_vocabulary(VOCABUARY_PATH)
dictionary = load_dictionary(DICT_PATH)

def get_meaning(word):
    entry = dictionary.get(word)
    if not entry:
        return None
    meanings = entry["meanings"]
    for meaning in meanings:
        meaning.pop("id")
    return json.dumps(meanings, indent=4)

df = pd.DataFrame({"Word": list(map(lambda t: t[0], vocabulary)), "Frequency": list(map(lambda t: t[1], vocabulary)), "Sources": list(map(lambda t: t[2], vocabulary))})
df["All Sources"] = df["Sources"].apply(lambda x: ", ".join([str(i) for i in x[:5]]))
df["Source"] = df["Sources"].apply(lambda x: sentences[x[0]])
df["Online Search"] = df["Word"].apply(lambda w: f'<a href="http://www.iciba.com/{w}">{w}</a>')
df["Meaning"] = df["Word"].apply(get_meaning)

df = df.loc[:, ["Word", "Frequency", "Source", "Meaning", "Online Search", "All Sources"]]

app = Flask(__name__)

@app.route("/hello/<name>")
def hello_world(name=None):
    return render_template("hello.html", name=name)

@app.route('/')
def index():
    # df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    return render_template("vocabulary.html", df=df)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)