from flask import Flask, render_template, request, jsonify
from analytics.weight_projection import WeightProjection
from data.exercises import get_exercises_list, calculate_calories_burned

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/exercises')
def get_exercises():
    return jsonify(get_exercises_list())

@app.route('/api/calculate_target_calories', methods=['POST'])
def calculate_target_calories_api():
    user_data = request.get_json()
    
    bmr = calculate_bmr(user_data)
    tdee = bmr * 1.2  # Gasto Energético Diario Total (asumiendo nivel de actividad sedentario)
    
    return jsonify({'maintenance_calories': tdee})

@app.route('/api/projection', methods=['POST'])
def calculate_projection_api():
    data = request.get_json()
    user_data = data.get('userData', {})
    daily_records = data.get('dailyRecords', [])
    exercises = data.get('exercises', [])
    days = int(data.get('days', 365)) # Proyectar a 1 año para el cálculo

    bmr = calculate_bmr(user_data)
    
    projection = WeightProjection(
        current_weight=float(user_data.get('weight', 70)),
        target_weight=float(user_data.get('target-weight', 65)),
        bmr=bmr
    )

    if daily_records:
        avg_consumed = sum(r['consumed'] for r in daily_records) / len(daily_records)
    else:
        tdee = bmr * 1.2
        avg_consumed = tdee - 500

    exercise_calories = calculate_daily_exercise_calories(exercises, user_data.get('weight', 70))
    
    days_array, weights_array = projection.project_weight_loss(avg_consumed, exercise_calories, days)
    
    # Calcular meses para alcanzar el objetivo
    months_to_target = None
    target_weight = float(user_data.get('target-weight', 65))
    for i, weight in enumerate(weights_array):
        if weight <= target_weight:
            days_to_target = days_array[i]
            months_to_target = round(days_to_target / 30, 1)
            break

    return jsonify({
        'days': days_array.tolist(),
        'weights': weights_array,
        'months_to_target': months_to_target
    })

def calculate_bmr(user_data):
    weight = float(user_data.get('weight', 70))
    height = float(user_data.get('height', 165))
    age = float(user_data.get('age', 25))
    gender = user_data.get('gender', 'female')
    
    if gender == 'female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return 10 * weight + 6.25 * height - 5 * age + 5

def calculate_daily_exercise_calories(exercises, weight):
    total_weekly_calories = 0
    for exercise in exercises:
        calories_per_session = calculate_calories_burned(
            exercise['name'],
            float(weight),
            int(exercise['duration'])
        )
        total_weekly_calories += calories_per_session * int(exercise['frequency'])
    
    return total_weekly_calories / 7 if total_weekly_calories > 0 else 0

if __name__ == '__main__':
    app.run(debug=True)