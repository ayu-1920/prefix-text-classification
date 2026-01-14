from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from ml_pipeline import MLPipeline
import base64
from io import BytesIO
from logger import global_logger

app = Flask(__name__)
CORS(app)

ml_pipeline = MLPipeline()

global_logger.info("Flask backend started successfully")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Backend server is running',
        'version': '1.0.0'
    })

@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    """Return available datasets"""
    try:
        global_logger.info("Fetching available datasets")
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
    except Exception as e:
        global_logger.error("Failed to fetch datasets", e)
        return jsonify({'error': 'Failed to fetch datasets'}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Return available models"""
    try:
        global_logger.info("Fetching available models")
        models = [
            {
                'id': 'logistic',
                'name': 'Logistic Regression',
                'description': 'Fast linear classifier'
            },
            {
                'id': 'naive_bayes',
                'name': 'Naive Bayes',
                'description': 'Probabilistic classifier'
            },
            {
                'id': 'svm',
                'name': 'Support Vector Machine',
                'description': 'Powerful kernel-based classifier'
            }
        ]
        return jsonify(models)
    except Exception as e:
        global_logger.error("Failed to fetch models", e)
        return jsonify({'error': 'Failed to fetch models'}), 500

@app.route('/api/experiment', methods=['POST'])
def run_experiment():
    """Run ML experiment with given parameters"""
    try:
        data = request.json
        dataset_id = data.get('dataset', 'imdb')
        model_id = data.get('model', 'logistic')
        prefix_length = data.get('prefixLength', 50)

        global_logger.info(f"Starting experiment: dataset={dataset_id}, model={model_id}, prefix_length={prefix_length}")

        # Run experiment
        results = ml_pipeline.run_experiment(
            dataset_id=dataset_id,
            model_id=model_id,
            prefix_length=prefix_length
        )

        # Convert plot images to base64
        plots_data = {}
        if 'plots' in results:
            for key, fig_bytes in results['plots'].items():
                plots_data[key] = base64.b64encode(fig_bytes).decode('utf-8')
                results['plots'][key] = plots_data[key]

        # Save experiment to database
        experiment_data = {
            'dataset_id': dataset_id,
            'model_id': model_id,
            'prefix_length': prefix_length,
            'full_text_metrics': results['full_text'],
            'prefix_metrics': results['prefix'],
            'performance_retention': results['performance_retention'],
            'dataset_size': results['dataset_size'],
            'train_size': results['train_size'],
            'test_size': results['test_size'],
            'label_names': results['label_names'],
            'plots': plots_data
        }
        global_logger.log_experiment(experiment_data)

        global_logger.info(f"Experiment completed successfully: accuracy={results['prefix']['accuracy']:.3f}")

        return jsonify(results)

    except Exception as e:
        global_logger.error("Experiment failed", e, {
            'dataset_id': data.get('dataset') if 'data' in locals() else None,
            'model_id': data.get('model') if 'data' in locals() else None,
            'prefix_length': data.get('prefixLength') if 'data' in locals() else None
        })
        return jsonify({'error': str(e)}), 500

@app.route('/api/token-comparison', methods=['POST'])
def token_comparison():
    """Compare accuracy across different token counts"""
    try:
        data = request.json
        dataset_id = data.get('dataset', 'imdb')
        model_id = data.get('model', 'logistic')

        global_logger.info(f"Starting token comparison: dataset={dataset_id}, model={model_id}")

        results = ml_pipeline.compare_token_counts(
            dataset_id=dataset_id,
            model_id=model_id
        )

        # Convert plot to base64
        if 'plot' in results:
            results['plot'] = base64.b64encode(results['plot']).decode('utf-8')

        global_logger.info("Token comparison completed successfully")

        return jsonify(results)

    except Exception as e:
        global_logger.error("Token comparison failed", e, {
            'dataset_id': data.get('dataset') if 'data' in locals() else None,
            'model_id': data.get('model') if 'data' in locals() else None
        })
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
