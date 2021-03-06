from flask import Flask, request, render_template, redirect, flash, jsonify
# # debug toolbar
# from flask_debugtoolbar import DebugToolbarExtension

from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)

# # debug toolbar
# app.config['SECRET_KEY'] = "password"
# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


# survey title
title = satisfaction_survey.title
# A list is used for the question counter instead of a primitive integer because the counter
#  requires an updates in the answer route to advance to the next question. A global primitive
#  can get referenced but it cannot change.
# The work-around is to convert question_nbr_current from a primitive to a list because list
#  elements ARE alterable -- heck, we can add answers to responses!
question_nbr_current = [0]

# responses list to hold the answers to the survey questions.
responses = []


def survey_reset_controls():
    """ function resets survey control variables """
    question_nbr_current[0] = 0

    # responses list to hold the answers to the survey questions.
    responses.clear()


@app.route("/")
def survey_welcome():
    """ Renders a welcome page with the title of the survey, the instructions, 
        and a button to start the survey. 

        The button links to a page with /questions/0.
    """

    instructions = satisfaction_survey.instructions

    return render_template("welcome.html", survey_title=title,
                           survey_instructions=instructions)


# @app.route("/questions/<question_nbr>")
# def survey_questions(question_nbr):
@app.route("/questions")
def survey_questions():
    """ Handles a survey questions. The question number is passed 
        in as a variable name in the route.

        The page presents the current survey question and possible 
        answer choices as radio buttons. 

        Answering the question (no button) generates a post 
        request to /answer with the answer selected. 

        Answer page will eventually redirect back to questions
        where the next question is aksed.

    """

    # The survey question number was passed in as a parameter but right from
    #  inception of the code, a global counter was used instead of passing in
    #  a question number.
    # Unfortunately, too much time was lost trying to figure out why the counter
    #  could not get updated and references to typically failed in the answer
    #  route. Not happy . . the time is gone.

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

    # render the questions page. Note that within questions.html, the question number
    #  presented to the respondent is question_nbr_current[0] + 1. The respondent sees
    #  1 as the first question, not 0.
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

    # question_nbr_current[0] holds the number of the current question.
    # radio box choices are named q-#-choices where # is the question
    #  number.
    answer = request.form[f'q-{question_nbr_current[0]}-choices']

    responses.append(answer)

    # advance to the next question number.
    question_nbr_current[0] = question_nbr_current[0] + 1

    # Is there another question?
    if (question_nbr_current[0] < len(satisfaction_survey.questions)):
        return redirect("/questions")
        # return render_template("answer.html", survey_title=title,
        #                     question_nbr=question_nbr_current[0],
        #                     question_answer="temp answer")
    else:
        return redirect("/thankyou")


@app.route("/thankyou")
def survey_thankyou():
    """ Handles the thank you page for the survey. """

    # is this legitimate? Was the survey completed?
    if ((question_nbr_current[0] == len(satisfaction_survey.questions)) and (len(responses) == len(satisfaction_survey.questions))):
        questions_answers = "Your responses:<br>"
        idx = 0
        for question in satisfaction_survey.questions:
            questions_answers = f"{questions_answers}{idx + 1}. {question.question}  <strong>{responses[idx]}</strong><br><br>"
            idx = idx + 1

        return render_template("thank_you.html", survey_title=title,
                               q_and_a=questions_answers)
    else:
        # restart the survey
        # A lot can happen here. The respondent can also get reset to the next natural question. But for now,
        #  reset the survey.
        survey_reset_controls()
        flash("Some survey shenanigans were detected. Your survey was reset.", "warning")
        return redirect("/")


@app.route("/reset")
def survey_reset():
    """ function to reset the survey so there is no need to stop the server for testing """

    survey_reset_controls()
    # question_nbr_current[0] = 0

    # # responses list to hold the answers to the survey questions.
    # responses.clear()

    return redirect("/")
