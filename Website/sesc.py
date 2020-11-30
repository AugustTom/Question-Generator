from flask import Flask, render_template, url_for, request, flash, session
import spacy
import sys
import secrets
from flask import jsonify

sys.path.append('/Users/augusteto/Documents/University/Year 3/Dissertation/Question-Generator')
from Code.cloze_method_one import ClozeQuizGenerator

nlp = spacy.load('en_core_web_md')

app = Flask(__name__)
# tell Flask to use the above defined config

secret = secrets.token_urlsafe(32)
app.secret_key = secret


@app.route('/')
def index():
    return render_template("index.html", length=0)


@app.route('/generate', methods=["POST"])
def process():
    if request.method == 'POST':
        title = request.form['topic']
        if session.get('title') is not None:
            if session['title'] == title:
                quiz = (session['quiz'])
            else:
                session.pop('title')
                session.pop('quiz')
                quiz = get_quiz(title=title)
        else:
            quiz = get_quiz(title=title)
        return render_template("quiz.html", quiz=quiz, title=title, len=len(quiz))


@app.route('/check', methods=['POST'])
def check_answers():
    correct = 0
    quiz = session['quiz']
    for i in range(len(quiz)):
        answered = request.form[i]
        if quiz[i].answer == answered:
            correct = correct + 1
    return '<h1>Correct Answers: <u>' + str(correct) + '</u></h1>'


def get_quiz(title):
    session['title'] = title
    quiz_list = ClozeQuizGenerator(title=title).get_quiz()
    for question in quiz_list:
        session[question.question] = question.__dict__
    return quiz_list

    # if request.method == 'POST':
    #     req = request.form.getlist('option')
    #     score = 0
    #     print(req)
    #     total_questions = len(quiz)
    #     for i, question in enumerate(quiz):
    #         print("{} == {}".format(question.answer, req[i]))
    #         if question.answer == req[i]:
    #             score += 1
    #     if score > total_questions / 2:
    #         flash('Well done, you scored: {}'.format(score))
    #     else:
    #         flash("Keep on learning and you will get there. Your score is: {}".format(score))
    #
    #     return render_template("quiz.html")


# def check_score(req,quiz):
#     score = 0
#     total_questions = len(quiz)
#     for i, question in enumerate(quiz):
#         print("{} == {}".format(question.answer, req[i]))
#         if question.answer == req[i]:
#             score += 1
#     if score > total_questions / 2:
#         flash('Well done, you scored: {}'.format(score))
#     else:
#         flash("Keep on learning and you will get there. Your score is: {}".format(score))


if __name__ == '__main__':
    app.run(debug=True)
