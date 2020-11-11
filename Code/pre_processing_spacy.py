import spacy

class CleanText():
    def __init__(self, text):
        nlp = spacy.load('en_core_web_sm')
        self.doc = nlp(text)
        self.clean_text = []
        self.__remove_punctuation()
        self.__remove_stop_words()
        self.__lemmatize()

    def __remove_punctuation(self):
        self.clean_text = [self.clean_text.append(token.text)for token in self.doc if token.pos_ != 'PUNCT']

    def __remove_stop_words(self):
        self.clean_text = [self.clean_text.append(token.text) for token in self.doc if not token.is_stop]

    def __lemmatize(self):
        self.lemmatized_text = ' '.join([t.lemma_ for t in self.doc])


text = 'Oxygen is the chemical element with the symbol O and atomic number 8. It is a member of the chalcogen group ' \
       'in the periodic table, a highly reactive nonmetal, and an oxidizing agent that readily forms oxides with most' \
       'elements as well as with other compounds.'

clean_text = CleanText(text=text).clean_text
print(clean_text)
