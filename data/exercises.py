import pandas as pd
import os

def get_exercises_list():
    """Lee los ejercicios desde el archivo Excel"""
    try:
        # Ruta del archivo Excel
        excel_path = os.path.join('data', 'Ejercicio.xlsx')
        
        # Leer el Excel
        df = pd.read_excel(excel_path)
        
        # Limpiar y procesar datos
        exercises = []
        for _, row in df.iterrows():
            # Verificar que tenga datos válidos para ambos pesos
            if (pd.notna(row['Persona con 57 kg de peso']) and 
                pd.notna(row['Persona con 80 kg de peso'])):
                
                exercise = {
                    "name": row['Actividad'],
                    "57kg": int(row['Persona con 57 kg de peso']),
                    "80kg": int(row['Persona con 80 kg de peso']),
                    "duration": int(row['Tiempo (min)']) if pd.notna(row['Tiempo (min)']) else 60
                }
                exercises.append(exercise)
        
        print("[DEBUG] Ejercicios leídos del Excel:")
        for ex in exercises:
            print(f"- {ex['name']} (57kg: {ex['57kg']}, 80kg: {ex['80kg']}, duración: {ex['duration']} min)")
        return exercises
        
    except Exception as e:
        print(f"Error leyendo Excel: {e}")
        # Fallback con datos básicos si falla
        return [
            {"name": "Aeróbic", "57kg": 283, "80kg": 396, "duration": 60},
            {"name": "Ciclismo", "57kg": 453, "80kg": 635, "duration": 60},
            {"name": "Natación", "57kg": 453, "80kg": 635, "duration": 60},
            {"name": "Correr moderado", "57kg": 453, "80kg": 635, "duration": 60},
            {"name": "Caminar rápido", "57kg": 239, "80kg": 336, "duration": 60}
        ]

def calculate_calories_burned(exercise_name, weight_kg, duration_minutes):
    """
    Calcula calorías quemadas usando interpolación lineal
    basada en los datos del Excel para 57kg y 80kg
    """
    exercises = {ex["name"]: ex for ex in get_exercises_list()}
    
    if exercise_name not in exercises:
        return 0
    
    exercise = exercises[exercise_name]
    cal_57 = exercise["57kg"]
    cal_80 = exercise["80kg"]
    
    # Interpolación lineal: y = mx + b
    m = (cal_80 - cal_57) / (80 - 57)  # pendiente
    b = cal_57 - m * 57                # intersección
    
    calories_per_hour = m * weight_kg + b
    
    # Convertir a calorías por duración específica
    return (calories_per_hour * duration_minutes) / 60

def get_exercise_names():
    """Retorna solo los nombres de ejercicios para formularios"""
    return [exercise["name"] for exercise in get_exercises_list()]

# Función para debugging
def print_all_exercises():
    """Imprime todos los ejercicios disponibles"""
    exercises = get_exercises_list()
    print(f"Ejercicios disponibles ({len(exercises)}):")
    for i, ex in enumerate(exercises, 1):
        print(f"{i:2d}. {ex['name']} - 57kg: {ex['57kg']} cal/h - 80kg: {ex['80kg']} cal/h")

if __name__ == "__main__":
    # Test del módulo
    print_all_exercises()
    print(f"\nTest: Ciclismo para 65kg por 30min = {calculate_calories_burned('Ciclismo', 65, 30):.0f} calorías")