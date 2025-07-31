import numpy as np

class WeightProjection:
    def __init__(self, current_weight, target_weight, bmr, activity_level=1.2):
        self.current_weight = current_weight
        self.target_weight = target_weight
        self.bmr = bmr
        self.tdee = bmr * activity_level  # Total Daily Energy Expenditure

    def project_weight_loss(self, daily_calorie_intake, exercise_calories_per_day, timeframe_days):
        days = np.arange(0, timeframe_days + 1)
        projected_weights = []
        current_w = self.current_weight

        for day in days:
            # El déficit calórico diario es la diferencia entre el gasto total de energía y la ingesta calórica
            daily_deficit = self.tdee - daily_calorie_intake + exercise_calories_per_day
            
            # La pérdida de peso diaria se basa en el déficit calórico (aproximadamente 7700 calorías por kg de grasa)
            daily_weight_loss = daily_deficit / 7700
            current_w -= daily_weight_loss
            
            # Asegurarse de que el peso no caiga por debajo del peso objetivo
            projected_weights.append(max(current_w, self.target_weight))
        
        return days, projected_weights