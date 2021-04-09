import getopt
import random
import re
import sys

import gensim.downloader as api
import nltk
import numpy as np
import spacy
import wikipedia as wk
from nltk.corpus import wordnet as wn

word_vectors = []

help_message = 'main.py -t <topic> -q <question_generation_method> -d <distractor_generation_method>\n' \
               'For <question_generation_method> choose one of these:\n' \
               '     -TextRank\n' \
               '     -Random <--default\n' \
               'For<distractor_generation_method> choose one of these:\n' \
               '     -WordNet\n' \
               '     -WordEmbed\n' \
               '     -Random <--default\n'


def main(argv):
    title = 'Algorithm'
    question_method = generate_random_cloze_questions
    distractor_method = generate_random_distractors
    try:
        opts, args = getopt.getopt(argv, "t:", ["topic="])
    except getopt.GetoptError:
        print('main.py -t <topic> -q <question_generation_method> -d <distractor_generation_method>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ("-t", "--topic"):
            title = arg
        elif opt in ("-q", "--question"):
            question_method = arg
            if question_method == "Random":
                question_method = generate_random_cloze_questions
            elif question_method == "TextRank":
                question_method = generate_questions_using_text_rank
            else:
                print(help_message)
                sys.exit(2)
        elif opt in ("-d", "--distractor"):
            distractor_method = arg
            if distractor_method == "WordNet":
                distractor_method = get_distractors_wordnet
            elif distractor_method == "WordEmbed":
                distractor_method = generate_distractors_embedding
            elif distractor_method == "Random":
                distractor_method = generate_random_distractors
            else:
                print(help_message)
                sys.exit(2)

    try:
        text = TextFetcher(title).getText()
    except KeyError as error:
        print("an error occurred while parsing text")
        sys.exit(-1)

    # word_vectors = api.load("glove-wiki-gigaword-300")
    # text = clean_up_text(text)
    # print(text)
    # text = nlp(text)
    # generate_quiz(text, question_method, distractor_method)


class ClozeQuestion:
    def __init__(self, original_sentence, question, answer, distractors):
        self.original_sentence = original_sentence
        self.question = question
        self.answer = answer
        self.choices = []
        self.choices.append(answer)
        self.set_distractors(distractors)

    def get_quiz(self):
        pass

    def print_question(self):
        print("{}\n".format(self.question))
        for choice in self.choices:
            print("- {} \n".format(choice))
        print("\n")

    def set_distractors(self, distractors):
        self.distractors = distractors
        [self.choices.append(distractor) for distractor in distractors]
        random.shuffle(self.choices)


def checkTopic(title):
    """ A helper function for Text Fetcher class used to check if a given topic exists"""
    search = wk.search(title, results=3)
    if len(search) > 0:
        if search[0].lower() == title.lower():
            return 1
        else:
            raise KeyError("Unclear topic, choose one of these:", search)
    elif len(search) == 0:
        raise KeyError("No text was found!")


class TextFetcher:
    """ Text fetcher class is used communicate with Wikipedia API and fetching articles from it"""

    def __init__(self, title):
        wk.set_lang("en")
        search = wk.search(title, results=3)
        if len(search) > 0:
            if search[0].lower() == title.lower():
                try:
                    self.text = wk.page(title).summary
                except Exception:
                    raise KeyError("Sorry, an error occurred while fetching text")
            else:
                raise KeyError("Unclear topic, choose one of these:", search)
        elif len(search) == 0:
            raise KeyError("No text was found!")

    def getText(self):
        return self.text


def clean_up_text(text):
    """Cleans up text by removing whitespace and adding appropriate spacing to the end of sentences."""
    # TODO add special characters
    text = re.sub('\( \(([^\)]+)\)\)', ' ', text)
    text = re.sub('([a-z])([.!?])([A-Z])', r'\1\2 \3', text)
    text = re.sub('[\s]+', ' ', text)

    return text


# Random
def generate_random_cloze_questions(text, number_of_questions=10):
    # text = nlp(clean_up_text(text))
    questions = []
    for sent in get_random_sentences(text, number_of_questions):
        question, answer = get_random_blanks(sent)
        # distractors = generate_random_distractors(answer, text)
        questions.append(ClozeQuestion(sent, question, answer, []))
    return questions


def get_random_sentences(tokenized_text, number_of_questions=10):
    text_sentences = list(tokenized_text.sents)
    n_of_sentences = len(text_sentences)
    if n_of_sentences <= number_of_questions:
        sentences = text_sentences
    else:
        sentences = np.random.choice(text_sentences, number_of_questions, replace=False)
    return sentences


def get_random_blanks(sentence):
    len_of_sent = len(sentence)
    choice_index = np.random.choice(len_of_sent)
    while True:
        word = sentence[choice_index]
        if not word.is_stop and not word.is_punct and not word.is_space:
            sent_text = ""
            for i, token in enumerate(sentence):
                if i == choice_index:
                    sent_text += " _____ "
                else:
                    sent_text += token.text_with_ws
            return sent_text, word
        else:
            choice_index = np.random.choice(len_of_sent)


def generate_random_distractors(answer, text):
    distractors = []
    tag = answer.tag_
    text_sentences = list(text.sents)
    while True:
        random_sentence = np.random.choice(text_sentences)
        for word in random_sentence:
            if word.lower != answer.lower:
                if word.tag_ == tag:
                    distractors.append(word.text)
                    if len(distractors) == 3:
                        return distractors


def _normalize_matrix(matrix):
    #     normalize matrix
    for i in range(len(matrix)):
        if matrix[i].sum() == 0:
            matrix[i] = np.ones(len(matrix))
        matrix[i] /= matrix[i].sum()

    matrix
    return matrix


# TODO optimize the similarity by storing each words similarity
def _token_similarity(token1, token2):
    # if token1.lower == token2.lower:
    if token1.lemma_ == token2.lemma_:
        return 1.0
    if token2 and token2.vector_norm and token1 and token1.vector_norm:
        similarity = token1.similarity(token2)
        if similarity > 0.4:
            return similarity
    return 0


# TODO exclude stopwords
def _sentence_similarity(sent, sent2):
    similarity_count = 0
    for word in sent:
        for word2 in sent2:
            similarity_count += _token_similarity(word, word2)
    #         Changed from log10 to log2 !!
    return similarity_count / len(sent) + (len(sent2))
    #  return similarity_count / (np.log10(len(sent)) + np.log10(len(sent2)))


class TextRank:
    """Text rank is an class that implements text rank algorithm based on Michalcea and Paul Tarau paper.
    This is a modified version of the algorithm that is adapted for the purpose of a project.
    """

    def __init__(self, text, nlp, tag_filter=["NNP", "NN", "NNS"]):  # , "ADJ", "JJ", "VB", "VBN", "VBG",
        self.tag_filter = tag_filter
        self.d = 0.85
        self.convergence_threshold = 0.00001
        self.tokenized_text = text

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
                    # Based on the the fact that first sentences are more important, code below add weights based on the
                    # sentences appearance in the text
                    similarity = _sentence_similarity(sent, sent2) + (1 / (number_of_sentences * i + 1))
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
        total_number_of_sentences = len(original_sentences)
        if total_number_of_sentences < n:
            print("Only {} sentences are available. Returning ranked sentence list".format(total_number_of_sentences))
            n = total_number_of_sentences
        indexes = list(reversed(self.__integrate_weights(self.__create_sentence_similarity_matrix()).argsort()))[:n]

        return [original_sentences[i] for i in indexes]

    def get_top_keywords(self, n=3):

        key_rating, keywords = self.__create_keyword_similarity_matrix()
        key_ratings = self.__integrate_weights(key_rating)

        if n > len(keywords):
            n = len(keywords)
        indexes = list(reversed(key_ratings.argsort()))[:n]

        return [keywords[i] for i in indexes]


# TODO fix to actually get 10
def generate_questions_using_text_rank(text, number_of_questions):
    text_rank = TextRank(text=text, nlp=nlp)
    top_sentences = text_rank.get_top_sentences(number_of_questions * 2)

    top_keywords = text_rank.get_top_keywords(number_of_questions)
    cloze_questions = []

    for sentence in top_sentences:
        original_sentence = sentence.orth_
        question = " "
        answer = ""
        has_keyword = False
        has_blank = False

        for token in sentence:
            if token in top_keywords and not has_blank:

                has_blank = True
                has_keyword = True
                question += "______"
                answer = token
            else:
                question += token.text_with_ws

        if has_keyword:
            cloze_questions.append(ClozeQuestion(original_sentence=original_sentence, question=question, answer=answer,
                                                 distractors=[]))
    return cloze_questions


word_vectors = api.load("glove-wiki-gigaword-300")


# Word Embeddings
def generate_similar_distractors(word):
    candidates = word_vectors.most_similar_cosmul(word)
    # print("similar: ", candidates)
    return [x[0] for x in candidates]


def generate_potential_distractors(word, all_distractors):
    candidates = word_vectors.most_similar_cosmul(positive=[word, 'good'], negative=['happy'])
    results = []
    # print("potential: ",candidates)
    for candidate in candidates:
        if candidate[0] not in all_distractors:
            results.append(candidate[0])
    return results


def generate_off_topic_distractors(word, all_distractors):
    candidates = word_vectors.most_similar_cosmul(positive=[word, 'good'], negative=['bad'])
    results = []
    # print("not in topic: ",candidates)
    for candidate in candidates:
        if candidate[0] not in all_distractors:
            results.append(candidate[0])
    return results


def check_candidate(sentence, target, candidates):
    tokens = nlp(sentence)
    target_token = nlp(target)[0]
    target_pos = target_token.pos_
    for i, candidate in enumerate(candidates):
        if candidate in sentence:
            del candidates[i]
        else:
            token = nlp(candidate)[0]
            pos = token.pos_
            # print(token.lemma_," ", target_token.lemma_)
            if pos != target_pos or token.lemma_ == target_token.lemma_:
                del candidates[i]
            else:
                return candidate


def generate_distractors_embedding(answer, sentence):
    distractors = []
    word = answer.lower_
    distractors.append(check_candidate(sentence,
                                       word,
                                       generate_similar_distractors(word)))
    distractors.append(check_candidate(sentence,
                                       word,
                                       generate_potential_distractors(word,
                                                                      distractors)))
    distractors.append(check_candidate(sentence,
                                       word,
                                       generate_off_topic_distractors(word,
                                                                      distractors)))
    return distractors


# Distractors from Wordnet
# TODO get the sense from the text to avoid word sense disambiguation
def get_distractors_wordnet(syn, word):
    distractors = []
    word = word.lower()
    orig_word = word
    if len(word.split()) > 0:
        word = word.replace(" ", "_")
    hypernym = syn.hypernyms()
    if len(hypernym) == 0:
        return distractors
    for item in hypernym[0].hyponyms():
        name = item.lemmas()[0].name()
        # print ("name ",name, " word",orig_word)
        if name == orig_word:
            continue
        name = name.replace("_", " ")
        name = " ".join(w for w in name.split())
        if name is not None and name not in distractors:
            distractors.append(name)
    return distractors


def generate_distractors_wornet(answer, sentence):
    synset_to_use = wn.synsets(answer)
    potential = get_distractors_wordnet(synset_to_use[0], answer)
    if len(potential) < 4:
        return potential
    else:
        return potential[:3]


def generate_quiz(tokenized_text, question_generation_method, distractor_generation_method, number_of_questions=10):
    cloze_questions = question_generation_method(text=tokenized_text, number_of_questions=number_of_questions)
    print("_______ QUIZ _______")
    for i, question in enumerate(cloze_questions):
        if distractor_generation_method == generate_random_distractors:
            distractors = distractor_generation_method(question.answer, tokenized_text)
        else:
            distractors = distractor_generation_method(question.answer, question.original_sentence)

        question.set_distractors(distractors)
        question.print_question()


main(sys.argv[1:])
nltk.download('wordnet')
nlp = spacy.load('en_core_web_md')
