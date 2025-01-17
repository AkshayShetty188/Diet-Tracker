from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import plotly
import plotly.graph_objs as go
import json
from datetime import date

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class MealLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    meal = db.Column(db.String(200), nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Diet Plan Data
diet_plans = {
    "Breakfast": {
        "options": [
            {
                "name": "Vegetable Upma with Boiled Eggs",
                "nutrition": {"Protein": 24, "Carbs": 53},
                "recipe": "Roast 30g semolina in a dry pan. Sauté chopped vegetables (carrot, beans, peas) in 1 tsp oil. Add water, salt, and roasted semolina; cook until thickened."
            }
        ]
    },
    "Mid-Morning Snack": {
        "options": [
            {
                "name": "Moong Sprouts and Small Apple",
                "nutrition": {"Protein": 14.5, "Carbs": 43},
                "recipe": "Boil sprouts in water for 5 minutes. Add lemon juice, salt, and chopped onions."
            }
        ]
    },
    "Lunch": {
        "options": [
            {
                "name": "Brown Rice, Dal, Stir-Fried Vegetables, and Curd",
                "nutrition": {"Protein": 18, "Carbs": 74},
                "recipe": "For dal: Pressure cook 50g dal with water, turmeric, and salt. Add tempering with 1 tsp oil, mustard seeds, and curry leaves."
            }
        ]
    },
    "Pre-Workout Snack": {
        "options": [
            {
                "name": "Boiled Egg and Sweet Potato",
                "nutrition": {"Protein": 7, "Carbs": 26},
                "recipe": "Boil sweet potato and egg. Serve warm."
            }
        ]
    },
    "Post-Workout Snack": {
        "options": [
            {
                "name": "Curd with Chia Seeds",
                "nutrition": {"Protein": 10, "Carbs": 14},
                "recipe": "Mix curd with chia seeds and serve chilled."
            }
        ]
    },
    "Dinner": {
        "options": [
            {
                "name": "White Rice with Sambar and Salad",
                "nutrition": {"Protein": 12, "Carbs": 85},
                "recipe": "For Sambar: Pressure cook 50g toor dal with water and turmeric. Add tamarind extract, chopped vegetables, and sambar powder."
            }
        ]
    },
    "Bedtime Snack": {
        "options": [
            {
                "name": "Skimmed Milk",
                "nutrition": {"Protein": 8, "Carbs": 12},
                "recipe": "Serve warm or chilled."
            }
        ]
    },
}


# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose a different username."
        
        # Create a new user if username is unique
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    logs = MealLog.query.filter_by(user_id=user_id).all()

    # Calculate totals
    total_protein = sum(log.protein for log in logs)
    total_carbs = sum(log.carbs for log in logs)
    total_meals = len(logs)

    # Group logs by date for better visualization
    stats = {}
    for log in logs:
        if log.date not in stats:
            stats[log.date] = {'protein': 0, 'carbs': 0}
        stats[log.date]['protein'] += log.protein
        stats[log.date]['carbs'] += log.carbs

    return render_template('profile.html', total_protein=total_protein, total_carbs=total_carbs, total_meals=total_meals, stats=stats)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    # Fetch meal logs for the user
    logs = MealLog.query.filter_by(user_id=user_id).all()

    # Calculate totals
    total_meals = len(logs)
    total_protein = sum(log.protein for log in logs)
    total_carbs = sum(log.carbs for log in logs)

    # Diet plan data
    diet_plans = {
    "Breakfast": {
        "options": [
            {
                "name": "Vegetable Upma with Boiled Eggs",
                "nutrition": {"Protein": 24, "Carbs": 53},
                "recipe": "Roast 30g semolina in a dry pan. Sauté chopped vegetables (carrot, beans, peas) in 1 tsp oil. Add water, salt, and roasted semolina; cook until thickened."
            }
        ]
    },
    "Mid-Morning Snack": {
        "options": [
            {
                "name": "Moong Sprouts and Small Apple",
                "nutrition": {"Protein": 14.5, "Carbs": 43},
                "recipe": "Boil sprouts in water for 5 minutes. Add lemon juice, salt, and chopped onions."
            }
        ]
    },
    "Lunch": {
        "options": [
            {
                "name": "Brown Rice, Dal, Stir-Fried Vegetables, and Curd",
                "nutrition": {"Protein": 18, "Carbs": 74},
                "recipe": "For dal: Pressure cook 50g dal with water, turmeric, and salt. Add tempering with 1 tsp oil, mustard seeds, and curry leaves."
            }
        ]
    },
    "Pre-Workout Snack": {
        "options": [
            {
                "name": "Boiled Egg and Sweet Potato",
                "nutrition": {"Protein": 7, "Carbs": 26},
                "recipe": "Boil sweet potato and egg. Serve warm."
            }
        ]
    },
    "Post-Workout Snack": {
        "options": [
            {
                "name": "Curd with Chia Seeds",
                "nutrition": {"Protein": 10, "Carbs": 14},
                "recipe": "Mix curd with chia seeds and serve chilled."
            }
        ]
    },
    "Dinner": {
        "options": [
            {
                "name": "White Rice with Sambar and Salad",
                "nutrition": {"Protein": 12, "Carbs": 85},
                "recipe": "For Sambar: Pressure cook 50g toor dal with water and turmeric. Add tamarind extract, chopped vegetables, and sambar powder."
            }
        ]
    },
    "Bedtime Snack": {
        "options": [
            {
                "name": "Skimmed Milk",
                "nutrition": {"Protein": 8, "Carbs": 12},
                "recipe": "Serve warm or chilled."
            }
        ]
    },
}

    return render_template(
        'dashboard.html',
        diet_plans=diet_plans,
        total_meals=total_meals,
        total_protein=total_protein,
        total_carbs=total_carbs
    )


@app.route('/meal_details/<meal_name>', methods=['GET', 'POST'])
def meal_details(meal_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    for category, data in diet_plans.items():
        for option in data["options"]:
            if option["name"] == meal_name:
                if request.method == 'POST':
                    taken = request.form.get('taken') == 'yes'
                    if taken:
                        new_log = MealLog(
                            user_id=user_id,
                            date=str(date.today()),
                            meal=meal_name,
                            protein=option["nutrition"]["Protein"],
                            carbs=option["nutrition"]["Carbs"]
                        )
                        db.session.add(new_log)
                        db.session.commit()
                    return redirect(url_for('dashboard'))
                return render_template('meal_details.html', meal_name=meal_name, nutrition=option["nutrition"], recipe=option["recipe"])
    return "Meal not found!", 404

@app.route('/intake_summary')
def intake_summary():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    logs = MealLog.query.filter_by(user_id=user_id).all()

    total_protein = sum(log.protein for log in logs)
    total_carbs = sum(log.carbs for log in logs)

    dates = [log.date for log in logs]
    protein_values = [log.protein for log in logs]
    carb_values = [log.carbs for log in logs]

    protein_trace = go.Bar(x=dates, y=protein_values, name='Protein')
    carbs_trace = go.Bar(x=dates, y=carb_values, name='Carbs')
    layout = go.Layout(title='Nutritional Intake', barmode='group')
    figure = go.Figure(data=[protein_trace, carbs_trace], layout=layout)

    graphJSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('intake_summary.html', total_protein=total_protein, total_carbs=total_carbs, graphJSON=graphJSON)


@app.route('/add_extra_item', methods=['GET', 'POST'])
def add_extra_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        item_name = request.form['item_name']
        fat = float(request.form['fat'])
        protein = float(request.form['protein'])
        carbs = float(request.form['carbs'])
        user_id = session['user_id']
        
        # Log the extra item as a MealLog
        new_log = MealLog(
            user_id=user_id,
            date=str(date.today()),
            meal=item_name,
            protein=protein,
            carbs=carbs
        )
        db.session.add(new_log)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_extra_item.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
