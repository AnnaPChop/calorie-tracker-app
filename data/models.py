"""
Modelos de datos para CalorieTracker Pro
Representan las entidades principales de la aplicación
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class User:
    """Modelo para datos del usuario"""
    weight: float  # kg
    height: float  # cm
    age: int
    gender: str  # 'male' o 'female'
    target_weight: float  # kg
    activity_level: str = 'sedentary'  # sedentary, light, moderate, active, very_active
    
    def calculate_bmr(self) -> float:
        """
        Calcula Basal Metabolic Rate usando fórmula Mifflin-St Jeor
        Más precisa que Harris-Benedict
        """
        if self.gender.lower() == 'female':
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
    
    def calculate_tdee(self) -> float:
        """
        Total Daily Energy Expenditure
        BMR * factor de actividad
        """
        activity_factors = {
            'sedentary': 1.2,      # Poco o nada de ejercicio
            'light': 1.375,        # Ejercicio ligero 1-3 días/semana
            'moderate': 1.55,      # Ejercicio moderado 3-5 días/semana
            'active': 1.725,       # Ejercicio duro 6-7 días/semana
            'very_active': 1.9     # Ejercicio muy duro, trabajo físico
        }
        
        bmr = self.calculate_bmr()
        factor = activity_factors.get(self.activity_level, 1.2)
        return bmr * factor
    
    def weight_to_lose(self) -> float:
        """Kilos que necesita perder"""
        return max(0, self.weight - self.target_weight)
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para JSON"""
        return {
            'weight': self.weight,
            'height': self.height,
            'age': self.age,
            'gender': self.gender,
            'target_weight': self.target_weight,
            'activity_level': self.activity_level,
            'bmr': self.calculate_bmr(),
            'tdee': self.calculate_tdee()
        }

@dataclass
class DailyRecord:
    """Registro diario de calorías"""
    date: date
    calories_consumed: int
    calories_target: int
    weight_recorded: Optional[float] = None  # Peso del día (opcional)
    notes: str = ""
    
    @property
    def calorie_deficit(self) -> int:
        """Déficit calórico del día (positivo = déficit, negativo = exceso)"""
        return self.calories_target - self.calories_consumed
    
    @property
    def is_on_track(self) -> bool:
        """Si cumplió o se acercó al objetivo (margen ±100 cal)"""
        return abs(self.calorie_deficit) <= 100
    
    def to_dict(self) -> Dict:
        return {
            'date': self.date.isoformat(),
            'calories_consumed': self.calories_consumed,
            'calories_target': self.calories_target,
            'calorie_deficit': self.calorie_deficit,
            'weight_recorded': self.weight_recorded,
            'notes': self.notes,
            'is_on_track': self.is_on_track
        }

@dataclass
class Exercise:
    """Modelo para ejercicios individuales"""
    name: str
    calories_per_hour_57kg: int
    calories_per_hour_80kg: int
    category: str = "general"  # cardio, strength, flexibility, sport
    
    def calculate_calories(self, weight_kg: float, duration_minutes: int) -> float:
        """
        Calcula calorías quemadas usando interpolación lineal
        """
        # Interpolación lineal entre 57kg y 80kg
        cal_57 = self.calories_per_hour_57kg
        cal_80 = self.calories_per_hour_80kg
        
        # y = mx + b
        m = (cal_80 - cal_57) / (80 - 57)
        b = cal_57 - m * 57
        
        calories_per_hour = m * weight_kg + b
        return (calories_per_hour * duration_minutes) / 60
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'calories_57kg': self.calories_per_hour_57kg,
            'calories_80kg': self.calories_per_hour_80kg,
            'category': self.category
        }

@dataclass
class ExerciseSession:
    """Sesión de ejercicio específica"""
    exercise_name: str
    duration_minutes: int
    date: date
    calories_burned: float = 0
    intensity: str = "moderate"  # light, moderate, intense
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'exercise_name': self.exercise_name,
            'duration_minutes': self.duration_minutes,
            'date': self.date.isoformat(),
            'calories_burned': self.calories_burned,
            'intensity': self.intensity,
            'notes': self.notes
        }

@dataclass
class WeeklyExercisePlan:
    """Plan semanal de ejercicio"""
    exercise_name: str
    sessions_per_week: int
    duration_per_session: int  # minutos
    
    def weekly_calories(self, weight_kg: float, exercise: Exercise) -> float:
        """Calorías totales por semana"""
        calories_per_session = exercise.calculate_calories(weight_kg, self.duration_per_session)
        return calories_per_session * self.sessions_per_week
    
    def daily_average_calories(self, weight_kg: float, exercise: Exercise) -> float:
        """Promedio diario de calorías"""
        return self.weekly_calories(weight_kg, exercise) / 7
    
    def to_dict(self) -> Dict:
        return {
            'exercise_name': self.exercise_name,
            'sessions_per_week': self.sessions_per_week,
            'duration_per_session': self.duration_per_session
        }

@dataclass
class WeightProjection:
    """Proyección de pérdida de peso"""
    start_weight: float
    target_weight: float
    start_date: date
    target_date: date
    daily_calorie_deficit: float
    projected_weights: List[float]
    projected_dates: List[date]
    
    @property
    def total_weight_loss(self) -> float:
        """Pérdida total proyectada"""
        return self.start_weight - self.projected_weights[-1]
    
    @property
    def days_to_goal(self) -> int:
        """Días estimados para llegar al objetivo"""
        for i, weight in enumerate(self.projected_weights):
            if weight <= self.target_weight:
                return i
        return len(self.projected_weights)
    
    @property
    def weekly_loss_rate(self) -> float:
        """Tasa de pérdida semanal promedio"""
        if len(self.projected_weights) < 7:
            return 0
        return (self.start_weight - self.projected_weights[6]) 
    
    def to_dict(self) -> Dict:
        return {
            'start_weight': self.start_weight,
            'target_weight': self.target_weight,
            'start_date': self.start_date.isoformat(),
            'target_date': self.target_date.isoformat(),
            'daily_deficit': self.daily_calorie_deficit,
            'total_loss': self.total_weight_loss,
            'days_to_goal': self.days_to_goal,
            'weekly_rate': self.weekly_loss_rate,
            'projected_weights': self.projected_weights,
            'projected_dates': [d.isoformat() for d in self.projected_dates]
        }

class UserProgress:
    """Clase para trackear progreso del usuario"""
    
    def __init__(self, user: User):
        self.user = user
        self.daily_records: List[DailyRecord] = []
        self.exercise_sessions: List[ExerciseSession] = []
        self.weekly_plans: List[WeeklyExercisePlan] = []
    
    def add_daily_record(self, record: DailyRecord):
        """Agregar registro diario"""
        self.daily_records.append(record)
        # Mantener ordenado por fecha
        self.daily_records.sort(key=lambda x: x.date)
    
    def add_exercise_session(self, session: ExerciseSession):
        """Agregar sesión de ejercicio"""
        self.exercise_sessions.append(session)
        self.exercise_sessions.sort(key=lambda x: x.date)
    
    def get_average_daily_deficit(self, days: int = 7) -> float:
        """Déficit calórico promedio de los últimos N días"""
        recent_records = self.daily_records[-days:]
        if not recent_records:
            return 0
        
        total_deficit = sum(record.calorie_deficit for record in recent_records)
        return total_deficit / len(recent_records)
    
    def get_exercise_calories_per_day(self, days: int = 7) -> float:
        """Calorías de ejercicio promedio por día"""
        recent_sessions = [s for s in self.exercise_sessions 
                          if (datetime.now().date() - s.date).days <= days]
        
        if not recent_sessions:
            return 0
        
        total_calories = sum(session.calories_burned for session in recent_sessions)
        return total_calories / days
    
    def get_streak_days(self) -> int:
        """Días consecutivos cumpliendo objetivo"""
        streak = 0
        for record in reversed(self.daily_records):
            if record.is_on_track:
                streak += 1
            else:
                break
        return streak
    
    def to_dict(self) -> Dict:
        return {
            'user': self.user.to_dict(),
            'daily_records': [r.to_dict() for r in self.daily_records],
            'exercise_sessions': [s.to_dict() for s in self.exercise_sessions],
            'weekly_plans': [p.to_dict() for p in self.weekly_plans],
            'stats': {
                'total_records': len(self.daily_records),
                'total_sessions': len(self.exercise_sessions),
                'current_streak': self.get_streak_days(),
                'avg_deficit_7d': self.get_average_daily_deficit(7),
                'avg_exercise_7d': self.get_exercise_calories_per_day(7)
            }
        }

# Funciones de utilidad
def create_user_from_dict(data: Dict) -> User:
    """Crear usuario desde diccionario"""
    return User(
        weight=data['weight'],
        height=data['height'],
        age=data['age'],
        gender=data['gender'],
        target_weight=data['target_weight'],
        activity_level=data.get('activity_level', 'sedentary')
    )

def create_daily_record_from_dict(data: Dict) -> DailyRecord:
    """Crear registro diario desde diccionario"""
    return DailyRecord(
        date=datetime.fromisoformat(data['date']).date(),
        calories_consumed=data['calories_consumed'],
        calories_target=data['calories_target'],
        weight_recorded=data.get('weight_recorded'),
        notes=data.get('notes', '')
    )

# Constantes útiles
ACTIVITY_LEVELS = {
    'sedentary': 'Sedentario (poco o nada de ejercicio)',
    'light': 'Ligero (ejercicio ligero 1-3 días/semana)',
    'moderate': 'Moderado (ejercicio moderado 3-5 días/semana)',
    'active': 'Activo (ejercicio duro 6-7 días/semana)',
    'very_active': 'Muy activo (ejercicio muy duro, trabajo físico)'
}

EXERCISE_CATEGORIES = {
    'cardio': 'Cardiovascular',
    'strength': 'Fuerza',
    'flexibility': 'Flexibilidad',
    'sport': 'Deporte',
    'general': 'General'
}

INTENSITY_LEVELS = {
    'light': 'Ligero',
    'moderate': 'Moderado', 
    'intense': 'Intenso'
}