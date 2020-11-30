class ClozeQuestion:
    def __init__(self, original_sentence, question, answer, distractors):
        self.original_sentence = original_sentence
        self.question = question
        self.answer = answer
        self.distractors = distractors
        self.choices =[]
        self.choices.append(answer)
        self.choices.append(distractors)

    def get_quiz(self):
        pass



