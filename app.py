from flask import Flask, request, render_template,redirect,flash,jsonify
from random import randint, choice,sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys ,Question,Survey
#from surveys import personality_quiz  as survey
from flask import session
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "chickensareverycool42"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



@app.route('/')
def show_surveys():
    return render_template('survey_menu.html',surveys = surveys)


@app.route('/start_survey',methods=['POST'])
def start_survey_post():
    survey_key= request.form.get('survey_key')
    if survey_key in surveys:
         session['current_survey']= survey_key
         session['responses'] = []
         return redirect('/questions/0')
    else:
         return redirect('/')
     


@app.route('/questions/<survey_key>',methods=['GET'])
def start_survey(survey_key):
    if survey_key not in surveys:
        return redirect('/')
    session['current_survey']= survey_key
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/answer',methods=['POST'])
def handle_question():
    """handles actual question when answering"""
    #gets the choice from the form on questions.html
    choice = request.form.get('answer')
    session_responses = session.get('responses',[])
    session_responses.append(choice)
    session['responses'] = session_responses

    #get key
    current_survey_key = session.get('current_survey')
    if not current_survey_key or current_survey_key not in surveys:
        flash('issue in survey key')
        return redirect('/')
    current_survey = surveys[current_survey_key]
    num_of_questions = len(current_survey.questions)
    if len(session_responses) == num_of_questions:
        return redirect('/completed')
    else:
        next_question_index = len(session_responses)
        return redirect(f'/questions/{next_question_index}')


@app.route('/questions/<int:qid>')
def get_questions(qid):
    """get queation"""
    current_survey_key = session.get('current_survey')
    if not current_survey_key or current_survey_key not in surveys:
        flash("survey key not working")
        return redirect('/')
    current_survey = surveys[current_survey_key]
    num_of_questions = len(current_survey.questions)
    if qid >= num_of_questions:
        if qid == num_of_questions:
            flash('invalid question')
            return redirect('/completed')
        else:
            return redirect(f'/thank_you?qid={qid}')
    
    if(len(session['responses'])!=qid):
        flash(f'invalid question at questions/ {qid}')
        return redirect(f'/questions/{len(session["responses"])}')

    question = current_survey.questions[qid]
    return render_template("questions.html", question_num=qid,question=question)

@app.route('/completed')
def complete():
    survey_responses = session.get('responses',[])
    print(survey_responses)
    return render_template("completion.html",survey_responses=survey_responses)

@app.route('/thank_you')
def thanks_page():
    qid = request.args.get('qid')
    return render_template('thanks.html',qid=qid)
#@app.route('/questions/<int:index>')
#def take_survey(index):
#    survey = list(surveys.values())[index]
#    return render_template("survey.html",survey = survey)