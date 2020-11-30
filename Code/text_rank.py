
import re
import numpy as np




def clean_up_text(text):
    """Cleans up text by removing whitespace and adding appropriate spacing to the end of sentences."""
    # TODO add special characters
    text = re.sub('([a-z])([.!?])([A-Z])', r'\1\2 \3', text)
    text = re.sub('[\s]+', ' ', text)
    return text


# TODO first sentence is usually the most important

def _normalize_matrix(matrix):
    #     normalize matrix
    for i in range(len(matrix)):
        if matrix[i].sum() == 0:
            matrix[i] = np.ones(len(matrix))
        matrix[i] /= matrix[i].sum()
    print(matrix)
    return matrix

# TODO optimize the similarity by storing each words similarity
def _token_similarity(token1, token2):
    if token1.lower == token2.lower:
        return 1.0
    if token2 and token2.vector_norm and token1 and token1.vector_norm:
        similarity = token1.similarity(token2)
        if similarity > 0.6:
            return similarity
    return 0


def _sentence_similarity(sent, sent2):
    similarity_count = 0
    for word in sent:
        for word2 in sent2:
            similarity_count += _token_similarity(word, word2)
    #         Changed from log10 to log2 !!
    return similarity_count / (np.log2(len(sent)) + np.log2(len(sent2)))

# TODO add division by length to each sentence to equalize the ranking (added log2 instead of log10)

class TextRank:
    """Text rank is an class that implements text rank algorithm based on Michalcea and Paul Tarau paper.
    This is a modified version of the algorithm that is adapted for the purpose of a project.
    """

    def __init__(self, text, nlp, tag_filter=["NNP", "VBG", "NN", "NNS"]):  # , "ADJ", "JJ", "VB", "VBN"
        self.tag_filter = tag_filter
        self.d = 0.85
        self.convergence_threshold = 0.00001
        self.tokenized_text = nlp(clean_up_text(text))

    def __get_sentence_list(self):
        """Removes all stop words, filters out by specified tags and lemmatizes text"""
        sentences = self.tokenized_text.sents
        sentences_list = []

        for sent in sentences:
            words = []
            for word in sent:
                if not word.is_stop and not word.is_punct and not word.is_space and word.tag_ in self.tag_filter:
                    if word.ent_type_ == '':
                        words.append(word)  # words.append(word.lemma_.lower())
                    else:
                        words.append(word)  # words.append(word.lemma_)
            sentences_list.append(words)
        return sentences_list

    def __get_keyword_list(self):
        keyword_list = []
        word_list = []
        for token in self.tokenized_text:
            if not token.is_stop and not token.is_punct and not token.is_space and token.tag_ in self.tag_filter and len(
                    token.text) > 2:
                if token.lemma_.lower() not in word_list:
                    keyword_list.append(token)
                    word_list.append(token.lemma_.lower())
        return keyword_list

    def __create_sentence_similarity_matrix(self):
        # initialize empty matrix
        sentences = self.__get_sentence_list()
        weights = np.zeros([len(sentences), len(sentences)])
        number_of_sentences = len(sentences)
        for i in range(number_of_sentences):
            for j in range(i + 1, number_of_sentences):
                sent = sentences[i]
                sent2 = sentences[j]
                if sent != sent2:
                    similarity = _sentence_similarity(sent, sent2) + (1/20 * i)
                    weights[i][j] = similarity
                    weights[j][i] = similarity

        return _normalize_matrix(weights)

    def __create_keyword_similarity_matrix(self):
        keywords = self.__get_keyword_list()
        weights = np.zeros([len(keywords), len(keywords)])

        for i in range(len(keywords)):
            for j in range(i + 1, len(keywords)):
                word_similarity = _token_similarity(keywords[i], keywords[j])
                weights[i][j] = word_similarity
                weights[j][i] = word_similarity
        return _normalize_matrix(weights), keywords

    def __integrate_weights(self, similarity_matrix):

        number = 1 / len(similarity_matrix)
        page_rank = np.array([number] * (len(similarity_matrix)))
        previous_page_rank = 0
        while True:
            page_rank = (1 - self.d) + self.d * np.dot(page_rank, similarity_matrix)
            if abs(previous_page_rank - sum(page_rank)) < self.convergence_threshold:
                return page_rank
            else:
                previous_page_rank = sum(page_rank)

    def get_top_sentences(self, n=3):
        original_sentences = list(self.tokenized_text.sents)
        indexes = list(reversed(self.__integrate_weights(self.__create_sentence_similarity_matrix()).argsort()))[:n]

        return [original_sentences[i] for i in indexes]

    def get_top_keywords(self, n=3):

        key_rating, keywords = self.__create_keyword_similarity_matrix()
        key_ratings = self.__integrate_weights(key_rating)

        if n > len(keywords):
            n = len(keywords)
        indexes = list(reversed(key_ratings.argsort()))[:n]

        return [keywords[i] for i in indexes]


# TODO replace pronouns sentences with nouns // Coreference resolution https://towardsdatascience.com/coreference-resolution-in-python-aca946541dec
# TODO add sentence weights based on the sentence order


# text = open("Data Generation/Oxygen.txt").read()
# tx = TextRank(text)
# # test = self.nlp(text)
# # for token in test:
# #         if token.pos_ == "PRON":
# #             print(token)
# #
# for key in tx.get_top_sentences(10):
#     print(key)
#

import spacy

nlp = spacy.load('en_core_web_md')


text = "Oxygen is the chemical element with the symbol O and atomic number 8. It is a member of the chalcogen group in" \
       " the periodic table, a highly reactive nonmetal, and an oxidizing agent that readily forms oxides with most" \
       " elements as well as with other compounds. After hydrogen and helium, oxygen is the third-most abundant element " \
       "in the universe by mass. At standard temperature and pressure, two atoms of the element bind to form dioxygen, " \
       "a colorless and odorless diatomic gas with the formula O2. Diatomic oxygen gas constitutes 20.95% of the Earth's " \
       "atmosphere. Oxygen makes up almost half of the Earth's crust in the form of oxides.Dioxygen provides the energy " \
       "released in combustion and aerobic cellular respiration, and many major classes of organic molecules in " \
       "living organisms contain oxygen atoms, such as proteins, nucleic acids, carbohydrates, and fats, " \
       "as do the major constituent inorganic compounds of animal shells, teeth, and bone. Most of the mass of living " \
       "organisms is oxygen as a component of water, the major constituent of lifeforms. Oxygen is continuously " \
       "replenished in Earth's atmosphere by photosynthesis, which uses the energy of sunlight to produce oxygen from " \
       "water and carbon dioxide. Oxygen is too chemically reactive to remain a free element in air without being " \
       "continuously replenished by the photosynthetic action of living organisms. Another form (allotrope) of " \
       "oxygen, ozone (O3), strongly absorbs ultraviolet UVB radiation and the high-altitude ozone layer helps " \
       "protect the biosphere from ultraviolet radiation. However, ozone present at the surface is a byproduct of " \
       "smog and thus a pollutant.Oxygen was isolated by Michael Sendivogius before 1604, but it is commonly believed " \
       "that the element was discovered independently by Carl Wilhelm Scheele, in Uppsala, in 1773 or earlier, " \
       "and Joseph Priestley in Wiltshire, in 1774. Priority is often given for Priestley because his work was " \
       "published first. Priestley, however, called oxygen dephlogisticated air, and did not recognize it as a " \
       "chemical element. The name oxygen was coined in 1777 by Antoine Lavoisier, who first recognized oxygen as a " \
       "chemical element and correctly characterized the role it plays in combustion.Common uses of oxygen include " \
       "production of steel, plastics and textiles, brazing, welding and cutting of steels and other metals, " \
       "rocket propellant, oxygen therapy, and life support systems in aircraft, submarines, spaceflight and diving. "


top_sentences = TextRank(text, nlp).get_top_sentences()

for sentence in top_sentences:
    print(sentence)
