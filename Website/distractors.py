import gensim.downloader as gensim
import nltk
from nltk.corpus import wordnet as wn


# nltk.download('wordnet')
# word_vectors = gensim.load("glove-wiki-gigaword-300")
#
#
# class DistractorsEmbeddings():
#     def __init__(self, nlp):
#         self.nlp = nlp
#
#     def generate_similar_distractors(self, word):
#         candidates = word_vectors.most_similar_cosmul(word)
#         # print("similar: ", candidates)
#         return [x[0] for x in candidates]
#
#     def generate_potential_distractors(self, word, all_distractors):
#         candidates = word_vectors.most_similar_cosmul(positive=[word, 'good'], negative=['happy'])
#         results = []
#         # print("potential: ",candidates)
#         for candidate in candidates:
#             if candidate[0] not in all_distractors:
#                 results.append(candidate[0])
#         return results
#
#     def generate_off_topic_distractors(self, word, all_distractors):
#         candidates = word_vectors.most_similar_cosmul(positive=[word, 'good'], negative=['bad'])
#         results = []
#         # print("not in topic: ",candidates)
#         for candidate in candidates:
#             if candidate[0] not in all_distractors:
#                 results.append(candidate[0])
#         return results
#
#     def check_candidate(self, sentence, target, candidates):
#         tokens = self.nlp(sentence)
#         target_token = self.nlp(target)[0]
#         target_pos = target_token.pos_
#         for i, candidate in enumerate(candidates):
#             if candidate in sentence:
#                 del candidates[i]
#             else:
#                 token = self.nlp(candidate)[0]
#                 pos = token.pos_
#                 # print(token.lemma_," ", target_token.lemma_)
#                 if pos != target_pos or token.lemma_ == target_token.lemma_:
#                     del candidates[i]
#                 else:
#                     return candidate
#
#     def generate_distractors(self, word, sentence):
#         distractors = []
#         distractors.append(self.check_candidate(sentence,
#                                                 word,
#                                                 self.generate_similar_distractors(word)))
#         distractors.append(self.check_candidate(sentence,
#                                                 word,
#                                                 self.generate_potential_distractors(word,
#                                                                                     distractors)))
#         distractors.append(self.check_candidate(sentence,
#                                                 word,
#                                                 self.generate_off_topic_distractors(word,
#                                                                                     distractors)))
#         return distractors


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


def generate_word_distractors(original_word):
    distractor_list = []
    synset_to_use = wn.synsets(original_word)
    if len(synset_to_use) > 0:
        distractors = get_distractors_wordnet(synset_to_use[0], original_word)
        if len(distractors) > 3:
            for i in range(3):
                distractor_list.append(distractors[i])
        else:
            distractor_list = distractors
    return distractor_list
