# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.config import db
from app.models import UserPreferences
import uuid

main = Blueprint('main', __name__)
user_preferences = UserPreferences(db)

def generate_session_id():
    """Generate a unique session ID if not exists"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@main.before_request
def before_request():
    """Ensure user has a session ID before each request"""
    if 'session_id' not in session:
        generate_session_id()

@main.route('/')
def landing_page():
    session_id = generate_session_id()
    # Try to load existing preferences
    prefs = user_preferences.get_user_preferences(session_id)
    if prefs:
        # Restore preferences to session
        session['grades'] = prefs.get('grades', [])
        session['subjects'] = prefs.get('subjects', [])
        session['teacher_tech'] = prefs.get('teacher_tech', [])
        session['student_devices'] = prefs.get('student_devices', [])
        session['goals'] = prefs.get('goals', [])
    
    return render_template('landing.html')

@main.route('/grades', methods=['GET', 'POST'])
def grades():
    session_id = generate_session_id()
    
    if request.method == 'POST':
        selected_grades = request.form.getlist('grade')
        if not selected_grades:
            flash('Please select at least one grade')
            return redirect(url_for('main.grades'))
        
        session['grades'] = selected_grades
        
        # Save to MongoDB
        prefs = user_preferences.get_user_preferences(session_id)
        if prefs:
            user_preferences.update_user_preferences(session_id, {'grades': selected_grades})
        else:
            user_preferences.create_user_preferences(session_id, {'grades': selected_grades})
        
        return redirect(url_for('main.subjects'))
    
    # For GET requests, try to load existing preferences
    prefs = user_preferences.get_user_preferences(session_id)
    selected_grades = prefs.get('grades', []) if prefs else []
    
    return render_template('grades.html', selected_grades=selected_grades)

@main.route('/subjects', methods=['GET', 'POST'])
def subjects():
    session_id = generate_session_id()
    print(f"Current session ID: {session_id}") #Debug print

    if request.method == 'POST':
        selected_subjects = request.form.getlist('subject')
        print(f"Form data received {selected_subjects}") #Debug print
        if not selected_subjects:
            flash('Please select at least one subject')
            return redirect(url_for('main.subjects'))
        
        session['subjects'] = selected_subjects
        print(f"Session subjects: {session['subjects']}") #Debug print
        
        # Save to MongoDB
        prefs = user_preferences.get_user_preferences(session_id)
        print(f"Existing preferences: {prefs}") #Debug print
        try:
            if prefs:
                updated = user_preferences.update_user_preferences(session_id, {'subjects': selected_subjects})
                print(f"Update result {updated}") #Debug print
            else:
                created = user_preferences.create_user_preferences(session_id, {'subjects': selected_subjects})
                print(f"Create result {created}") #Debug print
        except Exception as e:
            print(f"MongoDB operation failed: {str(e)}") #Debug print
            flash('An error occurred while saving your preferences. Please try again.')
        
        return redirect(url_for('main.tools'))
    
    # Load existing preferences
    prefs = user_preferences.get_user_preferences(session_id)
    selected_subjects = prefs.get('subjects', []) if prefs else []
    print(f"Loaded subjects for display: {selected_subjects}") #Debug print
    return render_template('subjects.html', selected_subjects=selected_subjects)

@main.route('/tools', methods=['GET', 'POST'])
def tools():
    session_id = generate_session_id()
    
    if request.method == 'POST':
        teacher_tech = request.form.getlist('teacher_tech')
        student_devices = request.form.getlist('student_devices')
        
        if not teacher_tech and not student_devices:
            flash('Please select at least one tool')
            return redirect(url_for('main.tools'))
        
        session['teacher_tech'] = teacher_tech
        session['student_devices'] = student_devices
        
        # Save to MongoDB
        prefs = user_preferences.get_user_preferences(session_id)
        if prefs:
            user_preferences.update_user_preferences(
                session_id,
                {
                    'teacher_tech': teacher_tech,
                    'student_devices': student_devices
                }
            )
        else:
            user_preferences.create_user_preferences(
                session_id,
                {
                    'teacher_tech': teacher_tech,
                    'student_devices': student_devices
                }
            )
        
        return redirect(url_for('main.goals'))
    
    # Load existing preferences
    prefs = user_preferences.get_user_preferences(session_id)
    selected_tech = prefs.get('teacher_tech', []) if prefs else []
    selected_devices = prefs.get('student_devices', []) if prefs else []
    
    return render_template(
        'tools.html',
        selected_tech=selected_tech,
        selected_devices=selected_devices
    )

@main.route('/goals', methods=['GET', 'POST'])
def goals():
    session_id = generate_session_id()
    
    if request.method == 'POST':
        selected_goals = request.form.getlist('goals')
        if not selected_goals:
            flash('Please select at least one goal')
            return redirect(url_for('main.goals'))
        
        session['goals'] = selected_goals
        
        # Save to MongoDB
        prefs = user_preferences.get_user_preferences(session_id)
        if prefs:
            user_preferences.update_user_preferences(session_id, {'goals': selected_goals})
        else:
            user_preferences.create_user_preferences(session_id, {'goals': selected_goals})
        
        return redirect(url_for('main.final_onboarding'))
    
    # Load existing preferences
    prefs = user_preferences.get_user_preferences(session_id)
    selected_goals = prefs.get('goals', []) if prefs else []
    
    return render_template('goals.html', selected_goals=selected_goals)

@main.route('/final_onboarding', methods=['GET', 'POST'])
def final_onboarding():
    session_id = generate_session_id()
    
    # Load all preferences from MongoDB
    prefs = user_preferences.get_user_preferences(session_id)
    
    if not prefs:
        return redirect(url_for('main.landing_page'))
    
    context = {
        'grades': prefs.get('grades', []),
        'subjects': prefs.get('subjects', []),
        'teacher_tech': prefs.get('teacher_tech', []),
        'student_devices': prefs.get('student_devices', []),
        'goals': prefs.get('goals', [])
    }
    
    return render_template('final_onboarding.html', **context)