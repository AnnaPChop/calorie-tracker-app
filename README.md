# CalorieTracker Pro 

*Porque MyFitnessPal me tenía HARTA y las calculadoras online son súper básicas*

## El drama que me llevó a crear esto 

Literal, estaba harta de usar aplicaciones que:
- Te bombardean con anuncios cada 2 segundos
- Tienen bases de datos súper limitadas para ejercicios (sobre todo para personas como yo que limpiar ya es un ejercicio agotador)
- Te cobran premium por funciones básicas
- No te dejan personalizar NADA

Y no me vengan con las típicas calculadoras de "1 libra = 3500 calorías" porque eso es súper simplista. Nuestro metabolismo es más complejo que eso 🙄

Así que dije "ya estuvo, lo hago yo misma" y aquí estamos.

## ¿Qué hace esta cosa? 

Básicamente es tu tracker personal de calorías pero con esteroides:

🍎 **Tracking real**: Registras lo que comes vs lo que deberías comer
💪 **Ejercicios que SÍ cuentan**: 23 actividades diferentes con cálculos reales basados en tu peso (Unos ejercicios bien fifis para aquellos que hacen más que yo)
📊 **Proyecciones que no mienten**: Te dice cuánto vas a bajar en 1, 3, 6 meses o 1 año
🧠 **Ciencia real**: Usa fórmulas científicas, no de esas cosas que a veces lees de internet
📱 **Bonita y funcional**: Porque si va a estar en mi portafolio, tiene que verse bien

## ¿Cómo funciona la magia? 🔮

### El algoritmo que me costó 3 trasnoches:

1. **BMR (Basal Metabolic Rate)**: Uso la fórmula Mifflin-St Jeor porque es la más precisa
2. **Cálculo de ejercicio**: Interpolación lineal entre datos de 57kg y 80kg (sí, hice la tarea)
3. **Proyección de peso**: Modelo exponencial con adaptación metabólica porque el cuerpo es inteligente
4. **Déficit calórico**: Combina comida + ejercicio de manera inteligente

### Ejemplo de cómo NO me puse a inventar con las matemáticas:

```python
# Fórmula para mujeres (que somos diferentes, shocking!)
BMR = 10 * peso + 6.25 * altura - 5 * edad - 161

# Para ejercicios (interpolación lineal porque soy fancy)
calorías = m * tu_peso + b
```

## Cómo usar esta belleza 

### Instalación (súper fácil, en serio):

```bash
git clone https://github.com/tuusuario/calorie-tracker-app.git
cd calorie-tracker-app
pip install -r requirements.txt
python app.py
```

### Uso diario:

1. **Llena tus datos**: Peso, altura, edad (no, no los voy a guardar en ningún lado)
2. **Registra tu comida**: Calorías que comiste vs las que deberías
3. **Agrega ejercicio**: Selecciona de la lista y cuántas veces por semana
4. **Ve la magia**: Proyecciones visuales que realmente tienen sentido

## Stack técnico (para los nerds como yo) 🤓

- **Python + Flask**: Porque Django es overkill para esto
- **JavaScript vanilla**: No necesito React para todo, gracias
- **Plotly.js**: Para graficas que sí se ven profesionales
- **CSS Grid**: Porque flexbox ya me tiene traumada
- **NumPy**: Para que las matemáticas no me odien

## Por qué esto es perfecto para mi portafolio 💼

Este proyecto demuestra que sé:
- Manipular datos reales (Excel incluido)
- Crear algoritmos que funcionan
- Hacer interfaces que no dan pena
- Resolver problemas reales con código
- Documentar como la gente (no como robot)

## Contribuciones 🤝

Si encuentras bugs o tienes ideas, manda PR. Solo no me cambies el diseño sin preguntar porque me tomó años llegar a algo que me gusta por favor 😅

También acepto:
- Más ejercicios para la base de datos
- Mejores algoritmos de proyección
- Traducciones (aunque está en español porque soy latina y bueno, luego me pongo a hacerla en inglés pra practicar)

## Disclaimer legal boring 📋

Esto es para uso personal/educativo. No soy nutrióloga ni doctora, solo una científica de datos que se cansó de apps que no le gustan. Consulta a profesionales para temas serios de salud.

---

*Hecho con mucho café ☕ y frustración 😤 en Morelia, Michoacán*

**¿Te gustó?** Dale estrella al repo y sígueme para más proyectos nacidos de la desesperación 🌟