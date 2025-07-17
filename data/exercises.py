# Fórmula para interpolar calorías según peso
def calculate_calories_burned(exercise_name, weight_kg, duration_minutes):
    # Calorías por hora para 57kg y 80kg
    exercises_data = {
        "Aeróbic": {"57kg": 283, "80kg": 396},
        "Ciclismo": {"57kg": 453, "80kg": 635},
        "Esquí de fondo": {"57kg": 453, "80kg": 635},
        # ... todos los ejercicios
    }
    
    if exercise_name not in exercises_data:
        return 0
    
    # Interpolación lineal basada en peso
    cal_57 = exercises_data[exercise_name]["57kg"]
    cal_80 = exercises_data[exercise_name]["80kg"]
    
    # Fórmula: y = mx + b
    m = (cal_80 - cal_57) / (80 - 57)
    b = cal_57 - m * 57
    
    calories_per_hour = m * weight_kg + b
    return (calories_per_hour * duration_minutes) / 60