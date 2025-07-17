from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, timedelta
from analytics.weight_projection import WeightProjection
from data.exercises import calculate_calories_burned, get_exercises_list

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/exercises')
def get_exercises():
    return jsonify(get_exercises_list())

@app.route('/api/projection', methods=['POST'])
def calculate_projection():
    data = request.get_json()
    
    user_data = data.get('userData', {})
    daily_records = data.get('dailyRecords', [])
    exercises = data.get('exercises', [])
    days = data.get('days', 30)
    
    # Calcular BMR
    projection = WeightProjection(
        current_weight=user_data.get('weight', 70),
        target_weight=user_data.get('targetWeight', 65),
        bmr=calculate_bmr(user_data)
    )
    
    # Calcular déficit calórico promedio
    daily_deficit = calculate_daily_deficit(daily_records, exercises, user_data)
    
    # Generar proyección
    days_array, weights_array = projection.project_weight_loss(daily_deficit, days)
    
    return jsonify({
        'days': days_array.tolist(),
        'weights': weights_array,
        'projected_loss': user_data.get('weight', 70) - weights_array[-1],
        'daily_deficit': daily_deficit
    })

def calculate_bmr(user_data):
    weight = user_data.get('weight', 70)
    height = user_data.get('height', 165)
    age = user_data.get('age', 25)
    gender = user_data.get('gender', 'female')
    
    if gender == 'female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return 10 * weight + 6.25 * height - 5 * age + 5

def calculate_daily_deficit(daily_records, exercises, user_data):
    # Calcular déficit promedio de registros diarios
    if daily_records:
        avg_consumed = sum(r['consumed'] for r in daily_records) / len(daily_records)
        avg_target = sum(r['target'] for r in daily_records) / len(daily_records)
        food_deficit = avg_target - avg_consumed
    else:
        food_deficit = 0
    
    # Calcular calorías quemadas por ejercicio
    exercise_calories = 0
    weight = user_data.get('weight', 70)
    
    for exercise in exercises:
        calories_per_session = calculate_calories_burned(
            exercise['name'], 
            weight, 
            exercise['duration']
        )
        weekly_calories = calories_per_session * exercise['frequency']
        exercise_calories += weekly_calories / 7  # Promedio diario
    
    return food_deficit + exercise_calories

if __name__ == '__main__':
    app.run(debug=True)