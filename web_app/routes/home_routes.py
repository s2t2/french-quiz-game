# web_app/routes/home_routes.py

from flask import Blueprint, render_template, flash, request, redirect
from app.play_quiz import get_category_data, get_level_data, load_database
from random import shuffle

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    print("VISITED THE HOME PAGE")
    #return "Welcome Home (TODO)"
    return render_template("home.html")

@home_routes.route("/about")
def about():
    print("VISITED THE ABOUT PAGE")
    #return "About Me (TODO)"
    return render_template("about.html")

@home_routes.route("/instructions")
def rules():
    print("VISITED THE INSTRUCTIONS PAGE")
    #return "How to play the game (TODO)"
    return render_template("instructions.html")

@home_routes.route("/user/new")
def register():
    print("VISITED THE REGISTRATION PAGE")
    #return "New user page (TODO)"
    return render_template("signup.html")

@home_routes.route("/user/create", methods=["POST"])
def regisetered():
    print("VISITED USER CREATED PAGE")
    user = dict(request.form)
    #print("FORM DATA:", dict(request.form))
    print("FORM DATA:", user)
    # todo: store in a database or google sheet!
    flash(f"User '{user['user_name']}' created successfully!", "success")
    #return "New user created page (TODO)"
    return redirect("/")

@home_routes.route("/new/setup")
def new_quiz_setup():
    print("VISITED NEW QUIZ SETTINGS PAGE")
    #return "New quiz settings page (TODO)"
    return render_template("quiz_setup.html")

@home_routes.route("/new/start", methods=["POST"])
def new_quiz_start():
    print("VISITED NEW QUIZ START PAGE")
    #print("FORM DATA:", dict(request.form))
    setup_info = dict(request.form)

    level_data = get_level_data(setup_info['lvl'])
    category_data = get_category_data(setup_info['categ'], level_data)

    shuffle(category_data)

    questions = []

    count = 1
    for question in category_data:
        if count <= int(setup_info['len']):
            payload = {
                "number": count,
                "english_word": question["english_word"],
                "french_word": question["french_word"]
            }

            questions.append(payload)
        else:
            break
        count = count + 1

    # questions must contain english word and ID
    return render_template("quiz_uncompleted.html", questions=questions, quiz_params=setup_info)
    #return render_template("quiz_setup.html")

@home_routes.route("/new/feedback", methods=["POST"])
def new_quiz_end():
    print("VISITED NEW QUIZ START PAGE")
    #print("FORM DATA:", dict(request.form))
    quiz_info = dict(request.form)

    quiz_length = int(quiz_info['quiz_length'])
    feedbacks = []

    setup_info = {
        'lvl': quiz_info['quiz_level'],
        'categ': quiz_info['quiz_cat'],
        'len': quiz_info['quiz_length']
    }

    for i in range(1, quiz_length + 1):
        question = str(i)
        count = 0
        payload = {
            "number": i,
            "correct": quiz_info[question].lower() == quiz_info[question + "_answer"].lower(),
            "english_word": quiz_info[question],
            "french_word": quiz_info[question + "_answer"]
        }

        feedbacks.append(payload)

        
    score_count = 0
    for feedback in feedbacks:
        if feedback["correct"] == True:
            score_count = score_count + 1
        else:
            score_count
    
    #print(score_count)
    percent_score = round((float(score_count)/float(setup_info['len']))*100,2)
    #print(percent_score)

    comment = ""

    if percent_score == 100:
        comment = "That's a perfect score! Great job!"
    elif percent_score < 100 and percent_score >= 85:
        comment = "Great going! You're almost there!"
    elif percent_score < 85 and percent_score >= 60:
        comment = "Don't worry, you just need some more practice"
    elif percent_score < 60:
        comment = "What happened there? You need to work harder!"
    else:
        comment = "IF THIS SHOWS UP, SOMETHING'S WRONG"

    #email_report_to = str(request.form)
    #print(email_report_to)

    #flash(f"Quiz report emailed to '{email_report_to}' successfully!", "success")

    return render_template("quiz_feedback.html", feedbacks=feedbacks, quiz_params=setup_info, 
    score_count=score_count, percent_score=percent_score, comment=comment)
    #return render_template("quiz_setup.html")

