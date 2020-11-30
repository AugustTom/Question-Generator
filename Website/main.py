from flask import Flask, render_template, url_for, request, flash, session
import spacy
import sys
import secrets

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
        # if 'quiz' not in session:
        quiz = get_quiz(title)
        session['quiz'] = quiz
        # else:
        #     quiz = session['quiz']
    return render_template("quiz.html", quiz=quiz['questions'], title=quiz['title'], len=len(quiz['questions']))


def result_message(correct, total_questions):
    result = correct / total_questions
    if result == 1:
        return "Amazing. You know it all!"
    if result > 0.5:
        return "Good job. Almost perfect!"
    else:
        return "Good try. Keep on learning!"


@app.route('/check', methods=['POST'])
def check_answers():
    correct = 0
    quiz = session['quiz']
    total_questions = len(quiz['questions'])
    print(session)
    for i in range(total_questions):
        answered = request.form[str(i)]
        answer = quiz['questions'][str(i)]['answer']
        print("answer:{}".format(answer))
        print("answered:{}".format(answered))
        if answer == answered:
            correct = correct + 1
    return render_template("results.html", result=correct, message=result_message(correct, total_questions))


def get_quiz(title):
    quiz = ClozeQuizGenerator(title=title).get_quiz_dic()
    print(quiz)
    return quiz

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
