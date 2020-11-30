# Imports
import spacy
from .text_fetcher import TextFetcher
from .text_rank import TextRank
from .cloze_question import ClozeQuestion


class ClozeQuizGenerator:
    def __init__(self, title, number_of_sentences=10, number_of_keywords=10):
        self.title = title
        self.nlp = spacy.load('en_core_web_md')
        self.text = TextFetcher(title=title).getText()
        text_rank = TextRank(text=self.text, nlp=self.nlp)
        self.top_sentences = text_rank.get_top_sentences(number_of_sentences)
        self.top_keywords = text_rank.get_top_keywords(number_of_keywords)

    def __form_cloze_questions(self):
        cloze_questions = []

        for sentence in self.top_sentences:

            original_sentence = sentence.orth_
            question = " "
            answer = ""
            has_keyword = False
            has_blank = False

            for token in sentence:

                if token in self.top_keywords and not has_blank:

                    has_blank = True
                    has_keyword = True
                    question += "______"
                    answer = token.text
                else:
                    question += token.text_with_ws

            if has_keyword:
                cloze_questions.append(
                    ClozeQuestion(original_sentence=original_sentence, question=question, answer=answer,
                                  distractors='None'))
        return cloze_questions

    def print_quiz(self):

        cloze_questions = self.__form_cloze_questions()

        for i, question in enumerate(cloze_questions):
            print("{} {}\n".format(i, cloze_questions[i].question))
            print("- {} \n\n".format(cloze_questions[i].answer))

    def get_quiz(self):
        cloze_questions = self.__form_cloze_questions()
        return cloze_questions

    def get_quiz_dic(self):
        result = {'title': self.title}
        cloze_questions = self.__form_cloze_questions()
        questions = {}
        for i, question in enumerate(cloze_questions):
            dist = {}
            for j, distractor in enumerate(question.distractors):
                dist[j] = distractor
            choices = {}
            for z,choice in enumerate(question.choices):
                choices[z] = choice
            questions[i] = {'question': question.question, "answer": question.answer, "distractors": dist,
                            'choices': choices}
        result['questions'] = questions
        return result

    def get_quiz_text(self):
        cloze_questions = self.__form_cloze_questions()
        quiz_text = ""
        for i, question in enumerate(cloze_questions):
            quiz_text += ("{} {}\n".format(i, cloze_questions[i].question))
            quiz_text += ("- {} \n\n".format(cloze_questions[i].answer))

        return quiz_text
# print(ClozeQuizGenerator(title="Oxygen").get_quiz_text())

