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
        const formData = new FormData();
        formData.append('days', days);
        formData.append('userData', JSON.stringify(this.userData));
        formData.append('dailyRecords', JSON.stringify(this.dailyRecords));
        formData.append('exercises', JSON.stringify(this.exercises));
        
        try {
            const response = await fetch('/api/projection', {
                method: 'POST',
                body: formData
            });
            
            const projection = await response.json();
            this.renderChart(projection);
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
                color: '#667eea',
                width: 3
            },
            marker: {
                color: '#f093fb',
                size: 8
            },
            name: 'Proyección de Peso'
        };
        
        const layout = {
            title: 'Proyección de Pérdida de Peso',
            xaxis: { title: 'Días' },
            yaxis: { title: 'Peso (kg)' },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { family: 'Inter, sans-serif' }
        };
        
        Plotly.newPlot('weight-chart', [trace], layout, {responsive: true});
    }
}

// Inicializar app
const app = new CalorieTracker();

// Funciones globales
function addDailyRecord() {
    const consumed = document.getElementById('calories-consumed').value;
    const target = document.getElementById('calories-target').value;
    
    if (consumed && target) {
        app.dailyRecords.push({
            date: new Date().toISOString().split('T')[0],
            consumed: parseInt(consumed),
            target: parseInt(target)
        });
        
        // Limpiar campos
        document.getElementById('calories-consumed').value = '';
        document.getElementById('calories-target').value = '';
        
        showToast('Registro agregado exitosamente!');
    }
}

function addExercise() {
    const exercise = document.getElementById('exercise-select').value;
    const duration = document.getElementById('exercise-duration').value;
    const frequency = document.getElementById('exercise-frequency').value;
    
    if (exercise && duration && frequency) {
        app.exercises.push({
            name: exercise,
            duration: parseInt(duration),
            frequency: parseInt(frequency)
        });
        
        // Limpiar campos
        document.getElementById('exercise-select').value = '';
        document.getElementById('exercise-duration').value = '';
        document.getElementById('exercise-frequency').value = '';
        
        showToast('Ejercicio agregado exitosamente!');
    }
}

function showToast(message) {
    // Implementar notificación toast
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
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