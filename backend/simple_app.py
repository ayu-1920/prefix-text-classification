from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import time

app = Flask(__name__)
CORS(app)

print("Simple Flask backend started successfully")

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'online',
        'message': 'Backend server is running',
        'version': '1.0.0'
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    models = [
        {'id': 'logistic', 'name': 'Logistic Regression'},
        {'id': 'naive_bayes', 'name': 'Naive Bayes'},
        {'id': 'svm', 'name': 'Support Vector Machine'}
    ]
    return jsonify(models)

@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    datasets = [
        {
            'id': 'imdb',
            'name': 'IMDb Movie Reviews',
            'description': 'Binary sentiment classification (positive/negative)',
            'samples': 2000
        },
        {
            'id': 'news',
            'name': 'News Category Dataset',
            'description': 'Multi-class news article classification',
            'samples': 2000
        }
    ]
    return jsonify(datasets)

@app.route('/api/experiment', methods=['POST'])
def run_experiment():
    data = request.json
    dataset = data.get('dataset')
    model = data.get('model')
    prefix_length = data.get('prefixLength', 50)
    
    # Simulate processing time
    time.sleep(2)
    
    # Generate realistic mock results based on prefix length
    base_accuracy = 0.92 if dataset == 'imdb' else 0.88
    retention = min(0.95, 0.75 + (prefix_length / 100))
    
    full_text_acc = base_accuracy + random.uniform(-0.02, 0.02)
    prefix_acc = full_text_acc * retention
    
    results = {
        'full_text': {
            'accuracy': round(full_text_acc, 3),
            'precision': round(full_text_acc - 0.01, 3),
            'recall': round(full_text_acc - 0.015, 3),
            'f1_score': round(full_text_acc - 0.005, 3),
            'confusion_matrix': [[450, 50], [40, 460]] if dataset == 'imdb' else [[400, 80, 60, 60], [70, 380, 70, 80], [50, 60, 420, 70], [80, 70, 50, 400]]
        },
        'prefix': {
            'accuracy': round(prefix_acc, 3),
            'precision': round(prefix_acc - 0.01, 3),
            'recall': round(prefix_acc - 0.015, 3),
            'f1_score': round(prefix_acc - 0.005, 3),
            'confusion_matrix': [[420, 80], [60, 440]] if dataset == 'imdb' else [[380, 100, 80, 40], [90, 350, 90, 70], [70, 80, 380, 70], [100, 80, 70, 350]]
        },
        'performance_retention': round(retention * 100, 1),
        'prefix_length': prefix_length,
        'dataset_size': 2000,
        'train_size': 1400,
        'test_size': 600,
        'label_names': ['Negative', 'Positive'] if dataset == 'imdb' else ['Tech', 'Sports', 'Business', 'Politics'],
        'plots': {
            'comparison': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
            'confusion_full': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
            'confusion_prefix': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
        }
    }
    
    return jsonify(results)

if __name__ == '__main__':
    print("Starting simple backend server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
