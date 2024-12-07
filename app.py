from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Workout, Users
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# SQLAlchemy database configuration
app.config['SECRET_KEY'] = '0ded7bc9b1679e570d69b5320f550910'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To silence warnings
db.init_app(app)

# Define the Run model for the running tracker
class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each run
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.String(50), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Signup route
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

# Login route (This is where the welcome message is added)
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
                flash('Login successful!')
                return redirect(url_for('workout_form'))
            else:
                flash('Invalid username or password.')
    
    # Flash a welcome message when the user first visits the login page
    flash(' Please log in to continue.')

    return render_template('login.html')

# Workout form page
@app.route('/workout_form')
def workout_form():
    return render_template("workout_form.html")

# Submit new workout
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

# View logged workouts
@app.route('/logged_workouts', methods=['GET', 'POST'])
def workout_logs():
    workouts = Workout.query.all()  
    workouts_by_date = defaultdict(list)
    
    for workout in workouts:
        workouts_by_date[workout.date].append(workout)
        
    return render_template("logged_workouts.html", workouts=workouts, workouts_per_date=workouts_by_date)

# Running tracker
@app.route('/running', methods=['GET', 'POST'])
def running():
    if request.method == 'POST':
        # Get data from the form
        date = request.form['date']
        time = request.form['time']
        distance = request.form['distance']
         # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.')
            return redirect(url_for('running'))

        # Validate time format (HH:MM:SS)
        try:
            datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            flash('Invalid time format. Use HH:MM:SS.')
            return redirect(url_for('running'))

        # Validate distance is numeric and positive
        try:
            distance = float(distance)
            if distance <= 0:
                raise ValueError("Distance must be greater than zero.")
        except ValueError:
            flash('Invalid distance. Enter a positive number.')
            return redirect(url_for('running'))

        # Save the submitted run to the database
        new_run = Run(date=date, time=time, distance=distance)
        db.session.add(new_run)
        db.session.commit()
        flash('Run saved successfully!')
        return redirect(url_for('running'))

    # Query all runs from the database
    runs = Run.query.all()
    return render_template('running.html', runs=runs)

@app.route('/delete_run/<int:run_id>', methods=['POST'])
def delete_run(run_id):
    run = Run.query.get(run_id)
    if run:
        db.session.delete(run)
        db.session.commit()
        flash('Run deleted successfully!')
    else:
        flash('Run not found.')
    return redirect(url_for('running'))


# About Us page
@app.route('/About_Us')
def aboutUs():
    return render_template("aboutUs.html")

# Delete a workout log
@app.route('/delete/<int:workout_id>', methods=['GET', 'POST'])
def delete_exercise(workout_id):
    workout = Workout.query.get(workout_id)
    if workout:
        db.session.delete(workout)
        db.session.commit()
        flash("Exercise deleted")
    return redirect(url_for('workout_logs'))

if __name__ == "__main__":
    app.run(debug=True)
