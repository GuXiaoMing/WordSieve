import os
import json

from flask import Flask
from flask import render_template
from jinja2 import Environment, PackageLoader, select_autoescape
from waitress import serve
import pandas as pd

from processor.resultloader import load_sentences, load_vocabulary
from processor.dictionary import load_dictionary

app = Flask(__name__)

DATA_PATH = "./data"
SENTENCES_PATH = os.path.join(DATA_PATH, "outputs", "sentences.csv")
VOCABUARY_PATH = os.path.join(DATA_PATH, "outputs", "vocabulary.csv")
DICT_PATH = os.path.join(DATA_PATH, "resources", "dictionary")
sentences = load_sentences(SENTENCES_PATH)
vocabulary = load_vocabulary(VOCABUARY_PATH)
dictionary = load_dictionary(DICT_PATH)

env = Environment(
    loader=PackageLoader(__name__, "templates"),
    autoescape=select_autoescape(["html", "xml"])
)
meanings_template = env.get_template("meanings.html")

def get_meaning(word):
    entry = dictionary.get(word)
    if not entry:
        return None
    meanings = entry["meanings"]
    return meanings_template.render(meanings=meanings)

df = pd.DataFrame({"Word": list(map(lambda t: t[0], vocabulary)), "Count": list(map(lambda t: t[1], vocabulary)), "Sources": list(map(lambda t: t[2], vocabulary))})
df["Occurrences"] = df["Sources"].apply(lambda x: ", ".join([str(i) for i in x[:5]]))
df["Source"] = df["Sources"].apply(lambda x: sentences[x[0]])
df["YouDao"] = df["Word"].apply(lambda w: f'<a href="http://www.youdao.com/w/eng/{w}" target="_blank">{w}</a>')
df["Meaning"] = df["Word"].apply(get_meaning)

df = df.loc[:, ["Word", "Count", "Source", "Meaning", "YouDao", "Occurrences"]]


@app.route("/hello/<name>")
def hello_world(name=None):
    return render_template("hello.html", name=name)

@app.route('/')
def index():
    return render_template("vocabulary.html", df=df)

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port="5000", debug=False)
    serve(app, host="0.0.0.0", port="5000")