import numpy as np
from datetime import datetime, timedelta

class WeightProjection:
    def __init__(self, current_weight, target_weight, bmr):
        self.current_weight = current_weight
        self.target_weight = target_weight
        self.bmr = bmr  # Basal Metabolic Rate
        
    def calculate_bmr(self, weight, height, age, gender):
        # Fórmula Mifflin-St Jeor
        if gender == 'female':
            return 10 * weight + 6.25 * height - 5 * age - 161
        else:
            return 10 * weight + 6.25 * height - 5 * age + 5
    
    def project_weight_loss(self, daily_calorie_deficit, timeframe_days):
        # 1 kg grasa = ~7700 calorías
        days = np.arange(0, timeframe_days + 1)
        
        # Modelo exponencial (más realista que lineal)
        projected_weights = []
        current_w = self.current_weight
        
        for day in days:
            # Adaptación metabólica gradual
            metabolic_adaptation = 1 - (day / timeframe_days) * 0.1
            effective_deficit = daily_calorie_deficit * metabolic_adaptation
            
            # Pérdida de peso diaria
            daily_weight_loss = effective_deficit / 7700
            current_w -= daily_weight_loss
            
            projected_weights.append(max(current_w, self.target_weight))
        
        return days, projected_weights