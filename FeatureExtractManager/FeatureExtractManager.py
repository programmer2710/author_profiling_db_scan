import string
import nltk as nltk
import re
from nltk.corpus import brown
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('genesis')
nltk.download('universal_tagset')
from nltk import ngrams
from nltk import word_tokenize, ngrams

def wordCounter(text):
    vector = text.split(" ")
    return len(vector)

def posTagCount(text):
    cleanedText = re.sub("\$.*?\$", '', text)
    table = str.maketrans(dict.fromkeys(string.punctuation))
    cleanedText = cleanedText.translate(table)
    tokens = nltk.tokenize.word_tokenize(cleanedText)
    pos = nltk.pos_tag(tokens)
    i = 0
    tags = []
    for tag in pos:
       tags.append(tag[1])
    return ' '.join(str(e) for e in tags)

def grams(text,gramCount):
    cleanedText = re.sub("\$.*?\$", '', text)
    table = str.maketrans(dict.fromkeys(string.punctuation))
    cleanedText = cleanedText.translate(table)
    grams = list(ngrams(cleanedText, gramCount))
    grams = [''.join(tups) for tups in grams]
    return grams

from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('omw')
import mlconjug3
import spacy
from spacy import displacy
from spacy.lang.pt import Portuguese # updated
from spacy import displacy
linkingVerbs = ["ser","estar","permanecer","ficar","parecer"]
adjetivosUniformes = ['e', 'l', 'm', 'r', 's','z']
def getGender(text,realGender,textId):
    cleanedText = re.sub("\$.*?\$", '', text)

    nlp = spacy.load("pt")
    #nlp = Portuguese()
    #nlp.add_pipe(nlp.create_pipe('sentencizer'))  # updated
    femCount = 0
    maleCount = 0
    doc = nlp(cleanedText)
    sub_toks = [tok for tok in doc if ("Person=1" in tok.tag_)]
    if len(sub_toks) > 0:
        print("=======================================")
        print("ID DO TEXTO:")
        print(textId)
        for token in sub_toks:
            if token.lemma_ in linkingVerbs:
                print("Palavra a ser analisada")
                print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
                gender = genero(token.head,adj=True,verb=True)
                if gender:
                    if gender == "Masc":
                        maleCount += 1
                    elif gender == "Fem":
                        femCount += 1
                for child in token.children:
                    gender = genero(child,adj=True,verb=True)
                    if gender:
                        if gender == "Masc":
                            maleCount += 1
                        elif gender == "Fem":
                            femCount += 1
        if maleCount == 0 and femCount == 0:
            return
        if maleCount > femCount:
            print("Genero real: ", realGender)
            print("Genero Predito: Masculino")
            print("=======================================")
            return "Masc"
        else:
            print("Genero real: ", realGender)
            print("Genero Predito: Feminino")
            print("=======================================")
            return "Fem"
        #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.head.text,[child for child in token.children])
        #displacy.serve(doc, style="dep")
        #for token in sub_toks:
        #    print(token.text, token.pos_, token.tag_)
    return

def genero(pos,adj,verb):
    print("Palavra ligada a ser analisada: ")
    print(pos.text, pos.lemma_, pos.pos_, pos.tag_, pos.dep_)
    if adj:
        search = re.search('ADJ__Gender=(.+?)\|Number=Sing', pos.tag_)
        if search:
            if pos.text[-1:] in adjetivosUniformes:
                return
            print(pos.text, pos.lemma_, pos.pos_, pos.tag_, pos.dep_)
            if search.group(1) == "Fem":
                print("Gênero Feminino")
                return "Fem"
            elif search.group(1) == "Masc":
                print("Gênero Masculino")
                return "Masc"
            else:
                print("Gênero nao especificado")
                return
    if verb:
        search = re.search('VERB__Gender=(.+?)\|Number=Sing\|VerbForm=Part\|Voice=Pass', pos.tag_)
        if search:
            print(pos.text, pos.lemma_, pos.pos_, pos.tag_, pos.dep_)
            if search.group(1) == "Fem":
                print("Gênero Feminino")
                return "Fem"
            elif search.group(1) == "Masc":
                print("Gênero Masculino")
                return "Masc"
            else:
                print("Gênero nao especificado")
                return

from nltk.corpus import stopwords
def getWords(text):
    cleanedText = re.sub("\$.*?\$", '', text)
    table = str.maketrans(dict.fromkeys(string.punctuation))
    cleanedText = cleanedText.translate(table)
    tokens = nltk.tokenize.word_tokenize(cleanedText)
    stop_words = set(stopwords.words('portuguese'))
    filtered_sentence = [w for w in tokens if not w in stop_words]
    return ' '.join(str(e) for e in filtered_sentence)

import re
def getPontcCount(text):
    count = len(re.findall("[,\.!?]",text))
    return count

def getBlankSpaces(text):
    blank = text.count(' ')
    print("Blank: %s" %blank)
    return blank


def getCapitalizedCount(text):
    cleanedText = re.sub("\$.*?\$", '', text)
    count = sum(map(str.isupper, cleanedText.split()))
    return count