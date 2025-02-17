from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def landing_page():
    return render_template('landing.html', 
        title="Welcome to Instructo",
        description="Instructo is a purpose built tool for teachers to personalized instructional materials, without having to learn prompt engineering"
    )

@main.route('/grades')
def grades():
    return render_template('grades.html')
