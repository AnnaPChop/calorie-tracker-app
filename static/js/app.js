class CalorieTracker {
    constructor() {
        this.userData = {};
        this.dailyRecords = [];
        this.exercises = [];
        this.init();
    }
    
    init() {
        this.loadExercises();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        document.getElementById('user-form').addEventListener('input', this.handleUserFormInput.bind(this));
        document.getElementById('calculate-calories-btn').addEventListener('click', this.calculateAndShowMaintenanceCalories.bind(this));
        document.getElementById('add-record-btn').addEventListener('click', this.addDailyRecord.bind(this));
        document.getElementById('add-exercise-btn').addEventListener('click', this.addExercise.bind(this));
        document.getElementById('close-modal-btn').addEventListener('click', this.closeModal.bind(this));
        
        const projectionButtons = document.querySelectorAll('.timeframe-buttons button');
        projectionButtons.forEach(button => {
            button.addEventListener('click', () => {
                const days = parseInt(button.dataset.days);
                this.updateProjection(days);
            });
        });
    }
    
    handleUserFormInput(event) {
        this.userData[event.target.id] = event.target.value;
    }
    
    async calculateAndShowMaintenanceCalories() {
        if (this.userData.weight && this.userData.height && this.userData.age && this.userData.gender) {
            try {
                const response = await fetch('/api/calculate_target_calories', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.userData)
                });
                const data = await response.json();
                const maintenanceCalories = Math.round(data.maintenance_calories);
                // Show in modal with custom message
                document.getElementById('modal-text').innerHTML = `Tus calorías objetivo son: <strong>${maintenanceCalories}</strong>`;
                document.getElementById('calories-modal').style.display = 'flex';
            } catch (error) {
                console.error('Error calculating maintenance calories:', error);
            }
        }
    }

    closeModal() {
        document.getElementById('calories-modal').style.display = 'none';
    }
    
    addDailyRecord() {
        const consumed = document.getElementById('calories-consumed').value;
        if (consumed) {
            this.dailyRecords.push({
                date: new Date().toISOString().split('T')[0],
                consumed: parseInt(consumed)
            });
            document.getElementById('calories-consumed').value = '';
            this.showToast('Registro agregado exitosamente!');
        }
    }
    
    addExercise() {
        const exercise = document.getElementById('exercise-select').value;
        const duration = document.getElementById('exercise-duration').value;
        const frequency = document.getElementById('exercise-frequency').value;
        
        if (exercise && duration && frequency) {
            this.exercises.push({
                name: exercise,
                duration: parseInt(duration),
                frequency: parseInt(frequency)
            });
            
            document.getElementById('exercise-select').value = '';
            document.getElementById('exercise-duration').value = '';
            document.getElementById('exercise-frequency').value = '';
            
            this.showToast('Ejercicio agregado exitosamente!');
        }
    }
    
    async loadExercises() {
        try {
            const response = await fetch('/api/exercises');
            const exercises = await response.json();
            this.populateExerciseSelect(exercises);
        } catch (error) {
            console.error('Error loading exercises:', error);
        }
    }
    
    populateExerciseSelect(exercises) {
        const select = document.getElementById('exercise-select');
        exercises.forEach(exercise => {
            const option = document.createElement('option');
            option.value = exercise.name;
            option.textContent = exercise.name;
            select.appendChild(option);
        });
    }
    
    async updateProjection(days) {
        try {
            const response = await fetch('/api/projection', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userData: this.userData,
                    dailyRecords: this.dailyRecords,
                    exercises: this.exercises,
                    days: days
                })
            });
            
            const projection = await response.json();
            this.renderChart(projection);
            this.displayTimeToTarget(projection);

        } catch (error) {
            console.error('Error updating projection:', error);
        }
    }
    
    renderChart(data) {
        const trace = {
            x: data.days,
            y: data.weights,
            type: 'scatter',
            mode: 'lines+markers',
            line: {
                color: 'var(--primary-color)',
                width: 3
            },
            marker: {
                color: 'var(--accent-color)',
                size: 8
            },
            name: 'Proyección de Peso'
        };
        
        const layout = {
            title: 'Proyección de Pérdida de Peso',
            xaxis: { title: 'Días', color: 'white', gridcolor: 'rgba(255,255,255,0.1)' },
            yaxis: { title: 'Peso (kg)', color: 'white', gridcolor: 'rgba(255,255,255,0.1)' },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { family: 'Inter, sans-serif', color: 'white' }
        };
        
        Plotly.newPlot('weight-chart', [trace], layout, {responsive: true});
    }

    displayTimeToTarget(data) {
        const resultElement = document.getElementById('time-to-target-result');
        if (data.months_to_target) {
            resultElement.innerHTML = `Siguiendo este ritmo, alcanzarías tu peso objetivo en aproximadamente <strong>${data.months_to_target}</strong> meses.`;
        } else {
            resultElement.innerHTML = 'Con los datos actuales, no parece que vayas a alcanzar tu peso objetivo. ¡Sigue esforzándote!';
        }
    }
    
    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-gradient);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// Inicializar app
const app = new CalorieTracker();