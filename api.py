"""
Flask API for Keno Prediction System
Provides RESTful endpoints for the web interface
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import glob
import json
from datetime import datetime
import prediction_engine
import dqn_predictor
import analyzeKenoData

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Initialize prediction engine
predictor = prediction_engine.PredictionEngine()
dqn_model = None

try:
    dqn_model = dqn_predictor.DQNKenoPredictor()
except Exception as e:
    print(f"DQN initialization warning: {e}")


@app.route('/')
def index():
    """Serve the main UI"""
    return send_from_directory('static', 'index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Make predictions based on historical data
    
    Expected JSON:
    {
        "strategy": "ensemble|frequency|hot_cold|pattern|statistical|markov|dqn",
        "num_picks": 4,
        "data_source": "filename or 'latest'"
    }
    """
    try:
        data = request.get_json()
        strategy = data.get('strategy', 'ensemble')
        num_picks = data.get('num_picks', 4)
        data_source = data.get('data_source', 'latest')
        
        # Load historical data
        historical_data = load_data(data_source)
        
        if not historical_data:
            return jsonify({
                'error': 'No historical data available'
            }), 400
        
        # Make prediction
        if strategy == 'dqn' and dqn_model:
            predictions = dqn_model.predict_numbers(historical_data, num_picks)
            result = {
                'numbers': predictions,
                'confidence': 45.0,  # Conservative estimate for DQN
                'strategy': 'dqn'
            }
        else:
            result = predictor.predict(historical_data, num_picks, strategy)
        
        # Add metadata
        result['timestamp'] = datetime.now().isoformat()
        result['data_points'] = len(historical_data)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze historical data and return statistics
    """
    try:
        data = request.get_json()
        data_source = data.get('data_source', 'latest')
        
        historical_data = load_data(data_source)
        
        if not historical_data:
            return jsonify({'error': 'No data available'}), 400
        
        # Calculate statistics
        stats = calculate_statistics(historical_data)
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/historical-accuracy', methods=['GET'])
def historical_accuracy():
    """
    Test prediction accuracy on historical data
    """
    try:
        # Load latest data
        historical_data = load_data('latest')
        
        if len(historical_data) < 60:
            return jsonify({
                'error': 'Insufficient historical data for accuracy testing'
            }), 400
        
        # Run accuracy analysis
        accuracy_results = predictor.analyze_historical_accuracy(
            historical_data, 
            lookback=50, 
            num_picks=4
        )
        
        return jsonify(accuracy_results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data-files', methods=['GET'])
def list_data_files():
    """
    List available data files
    """
    try:
        data_dir = 'kenoData'
        files = []
        
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if filename.endswith('.txt'):
                    filepath = os.path.join(data_dir, filename)
                    size = os.path.getsize(filepath)
                    files.append({
                        'name': filename,
                        'size': size,
                        'path': filepath
                    })
        
        return jsonify({
            'files': sorted(files, key=lambda x: x['name'], reverse=True)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/train-dqn', methods=['POST'])
def train_dqn():
    """
    Train the DQN model on historical data
    """
    try:
        if not dqn_model:
            return jsonify({
                'error': 'DQN model not available. Install TensorFlow.'
            }), 400
        
        data = request.get_json()
        episodes = data.get('episodes', 100)
        
        # Load historical data
        historical_data = load_data('all')
        
        if len(historical_data) < 100:
            return jsonify({
                'error': 'Insufficient data for training'
            }), 400
        
        # Train model
        dqn_model.train_on_history(historical_data, episodes)
        
        # Save model
        dqn_model.save('models/dqn_keno_model.h5')
        
        return jsonify({
            'success': True,
            'message': f'Model trained on {len(historical_data)} draws',
            'episodes': episodes
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def load_data(source='latest'):
    """
    Load historical Keno data
    """
    data_dir = 'kenoData'
    historical_data = []
    
    try:
        if source == 'all':
            # Load all available data
            for root, dirs, files in os.walk(data_dir):
                for filename in sorted(files):
                    if filename.endswith('.txt'):
                        filepath = os.path.join(root, filename)
                        file_data = prediction_engine.load_historical_data_from_file(filepath)
                        historical_data.extend(file_data)
        
        elif source == 'latest':
            # Load most recent file
            files = []
            for root, dirs, filenames in os.walk(data_dir):
                for filename in filenames:
                    if filename.endswith('.txt'):
                        files.append(os.path.join(root, filename))
            
            if files:
                latest_file = max(files, key=os.path.getctime)
                historical_data = prediction_engine.load_historical_data_from_file(latest_file)
        
        else:
            # Load specific file
            if os.path.exists(source):
                historical_data = prediction_engine.load_historical_data_from_file(source)
    
    except Exception as e:
        print(f"Error loading data: {e}")
    
    return historical_data


def calculate_statistics(historical_data):
    """
    Calculate comprehensive statistics from historical data
    """
    from collections import Counter
    
    # Frequency analysis
    all_numbers = []
    for draw in historical_data:
        all_numbers.extend(draw)
    
    frequency = Counter(all_numbers)
    
    # Most and least common
    most_common = frequency.most_common(10)
    least_common = frequency.most_common()[-10:]
    
    # Recent trends (last 20 draws)
    recent_numbers = []
    for draw in historical_data[-20:]:
        recent_numbers.extend(draw)
    recent_frequency = Counter(recent_numbers)
    
    # Hot numbers (appearing frequently in recent draws)
    hot_numbers = recent_frequency.most_common(10)
    
    # Cold numbers (not appearing in recent draws)
    all_nums = set(range(1, 81))
    recent_nums = set(recent_numbers)
    cold_numbers = list(all_nums - recent_nums)
    
    return {
        'total_draws': len(historical_data),
        'total_numbers_drawn': len(all_numbers),
        'most_common': [{'number': num, 'count': count} for num, count in most_common],
        'least_common': [{'number': num, 'count': count} for num, count in least_common],
        'hot_numbers': [{'number': num, 'count': count} for num, count in hot_numbers],
        'cold_numbers': cold_numbers[:10],
        'unique_numbers': len(set(all_numbers))
    }


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("Starting Keno Prediction API...")
    print("Access the UI at: http://localhost:5000")
    print("⚠️  For production deployment, use a production WSGI server (e.g., gunicorn)")
    
    # Security: Only bind to localhost by default
    # Set FLASK_HOST environment variable to '0.0.0.0' to allow external access
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    if host == '0.0.0.0':
        print("⚠️  WARNING: Server is accessible from external networks!")
    
    app.run(debug=debug_mode, host=host, port=5000)
