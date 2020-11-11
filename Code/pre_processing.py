import nltk
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import pos_tag


def preprocess(text):

    text = text.lower()

    text_p = "".join([char for char in text if char not in string.punctuation])

    words = word_tokenize(text_p)

    stop_words = stopwords.words('english')
    filtered_words = [word for word in words if word not in stop_words]

    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in filtered_words]

    pos = pos_tag(filtered_words)

    return words, filtered_words, stemmed, pos

text = 'xygen is the chemical element with the symbol O and atomic number 8. It is a member of the chalcogen group ' \
       'in the periodic table, a highly reactive nonmetal, and an oxidizing agent that readily forms oxides with most' \
       'elements as well as with other compounds.'

preprocess(text)