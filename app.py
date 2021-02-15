from flask import Flask, request, render_template, redirect, flash, jsonify
# debug toolbar
from flask_debugtoolbar import DebugToolbarExtension

from surveys import Question, Survey, satisfaction_survey
app = Flask(__name__)

# debug toolbar
app.config['SECRET_KEY'] = "password"
debug = DebugToolbarExtension(app)


# survey title
title = satisfaction_survey.title
question_nbr_current = [0]
responses = []


@app.route("/")
def survey_welcome():
    """ Renders a welcome page with the title of the survey, the instructions, 
        and a button to start the survey. 

        The button links to a page with /questions/0.
    """

    instructions = satisfaction_survey.instructions

    return render_template("welcome.html", survey_title=title,
                           survey_instructions=instructions)


@app.route("/questions/<question_nbr>")
def survey_questions(question_nbr):
    """ Handles a survey questions. The question number is passed 
        in as a variable name in the route.

        The page presents the current survey question and possible 
        answer choices as radio buttons. 

        Answering the question (no button) generates a post 
        request to /answer with the answer selected. 

        Answer page will eventually redirect back to questions
        where the next question is aksed.

    """

    # do you want to use the number from the route or an internal counter?

    title = satisfaction_survey.title
    question_text = satisfaction_survey.questions[question_nbr_current[0]].question

    # the answers for the survey question require processing. We need a value to present
    #  as text on the form and an internal form value for each answer.
    answers = []
    idx = 0
    for answer in satisfaction_survey.questions[question_nbr_current[0]].choices:
        answers.append((
            answer, f"{idx}_{answer.replace(' ', '-')}"))
        idx = idx + 1

    print(f"question_nbr_current={question_nbr_current[0]}", flush=True)
    print(f"survey_title={title}", flush=True)
    print(f"question_text={question_text}", flush=True)
    print(
        f"satisfaction_survey.questions={satisfaction_survey.questions[question_nbr_current[0]]}", flush=True)
    print(f"answers={answers}", flush=True)

    return render_template("questions.html", survey_title=title,
                           question_nbr=question_nbr_current[0],
                           question_nbr_max=(
                               len(satisfaction_survey.questions)),
                           question_text=question_text,
                           question_answers=answers)


@app.route("/answer", methods=["POST"])
def survey_answer():
    """ Handles the answer to a survey question. 

    """

    print("\n\n\nresponses:", flush=True)
    print(responses, flush=True)
    print("\ntitle", flush=True)
    print(title, flush=True)
    print("\nquestion_nbr_current", flush=True)
    print(question_nbr_current[0], flush=True)

    #print(f"question_nbr_current={question_nbr_current}", flush=True)

    # key = "q-" + question_nbr_current + "-choices"
    # answer = request.form[key]
    answer = request.form[f'q-{question_nbr_current[0]}-choices']
    # answer = request.form["q-0-choices"]

    responses.append(answer)
    print(f"responses={responses}", flush=True)

    question_nbr_current[0] = question_nbr_current[0] + 1

    print("\nquestion_nbr_current", flush=True)
    print(question_nbr_current[0], flush=True)

    # print(
    #     f"question {question_nbr_current} answer: {answer}, responses = {responses}", flush=True)

    # CURRENTQUESTION = CURRENTQUESTION + 1
    # question_nbr_current = question_nbr_current + 1

    return redirect(f"/questions/question_nbr_current[0]")
    # return render_template("answer.html", survey_title=title,
    #                        question_nbr=question_nbr_current,
    #                        question_answer=answer)
