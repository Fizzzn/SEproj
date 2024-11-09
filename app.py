from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Workout, Users
from collections import defaultdict
from datetime import datetime
app = Flask(__name__)

# SQLALchemy database
app.config['SECRET_KEY'] = '0ded7bc9b1679e570d69b5320f550910'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_database.db'
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
        else:
            new_user = Users(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!')
            
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Please enter both username and password.')
        else:
            user = Users.query.filter_by(username=username).first()
            if user and user.password == password:
                # Successful login logic here
                flash('Login successful!')
                return redirect(url_for('workout_form'))
            else:
                flash('Invalid username or password.')
    
    return render_template('login.html')

# provides the user with a form to create a log for a specific exercise 
@app.route('/workout_form')
def workout_form():
    return render_template("workout_form.html")

# Create a submit new workout
@app.route('/saved_workout', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        muscle_group = request.form['muscle_group']
        exercise = request.form['exercise']
        sets = int(request.form['sets'])
        reps = int(request.form['reps'])
        workout_date_str = request.form['workout_date']
        workout_date = datetime.strptime(workout_date_str, '%Y-%m-%d').date()
        
        created_workout = Workout(
            muscle_group=muscle_group, 
            exercise=exercise, 
            sets=sets, 
            reps=reps, 
            date=workout_date)
        
        db.session.add(created_workout)
        db.session.commit()
    return redirect(url_for('workout_logs'))
    

# Look at past workouts
@app.route('/logged_workouts', methods=['GET', 'POST'])
def workout_logs():
    workouts = Workout.query.all()  
    workouts_by_date = defaultdict(list)
    
    for workout in workouts:
        workouts_by_date[workout.date].append(workout)
        
    return render_template("logged_workouts.html", workouts=workouts, workouts_per_date=workouts_by_date)

@app.route('/About_Us')
def aboutUs():
    return render_template("aboutUs.html")\
    
    
# Deleting and editing logs
@app.route('/delete/<int:workout_id>', methods=['GET','POST'])
def delete_exercise(workout_id):
    workout = Workout.query.get(workout_id)
    if workout:
        db.session.delete(workout)
        db.session.commit()
        flash("Exercise deleted")
    return redirect(url_for('workout_logs'))



if __name__ == "__main__":
    app.run(debug=True)