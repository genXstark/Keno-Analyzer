"""
Enhanced Prediction Engine for Keno Analysis
Combines multiple mathematical algorithms and ML techniques.
"""
import numpy as np
import random
from collections import Counter
import re


class PredictionEngine:
    """Advanced prediction engine combining multiple strategies"""
    
    def __init__(self):
        self.strategies = {
            'frequency': self.frequency_analysis,
            'hot_cold': self.hot_cold_strategy,
            'pattern': self.pattern_detection,
            'statistical': self.statistical_approach,
            'markov': self.markov_chain_analysis,
        }
    
    def predict(self, historical_data, num_picks=4, strategy='ensemble'):
        """
        Make predictions using specified strategy
        
        Args:
            historical_data: List of lists containing historical draws
            num_picks: Number of numbers to predict
            strategy: Prediction strategy to use
            
        Returns:
            dict with predicted numbers and confidence scores
        """
        if strategy == 'ensemble':
            return self.ensemble_predict(historical_data, num_picks)
        elif strategy in self.strategies:
            numbers = self.strategies[strategy](historical_data, num_picks)
            return {
                'numbers': numbers,
                'confidence': self._calculate_confidence(historical_data, numbers),
                'strategy': strategy
            }
        else:
            return self.frequency_analysis(historical_data, num_picks)
    
    def ensemble_predict(self, historical_data, num_picks=4):
        """
        Combine multiple strategies for ensemble prediction
        """
        all_predictions = []
        weights = []
        
        # Get predictions from each strategy
        for strategy_name, strategy_func in self.strategies.items():
            try:
                predictions = strategy_func(historical_data, num_picks)
                all_predictions.append(predictions)
                weights.append(1.0)
            except Exception as e:
                print(f"Strategy {strategy_name} failed: {e}")
                continue
        
        # Weight and combine predictions
        number_scores = Counter()
        for predictions, weight in zip(all_predictions, weights):
            for num in predictions:
                number_scores[num] += weight
        
        # Get top predicted numbers
        final_predictions = [num for num, _ in number_scores.most_common(num_picks)]
        
        return {
            'numbers': sorted(final_predictions),
            'confidence': self._calculate_confidence(historical_data, final_predictions),
            'strategy': 'ensemble',
            'component_predictions': {
                name: pred for name, pred in zip(self.strategies.keys(), all_predictions)
            }
        }
    
    def frequency_analysis(self, historical_data, num_picks=4):
        """
        Predict based on number frequency in recent history
        """
        if not historical_data:
            return self._random_picks(num_picks)
        
        # Count frequency of all numbers
        frequency = Counter()
        for draw in historical_data[-100:]:  # Last 100 draws
            frequency.update(draw)
        
        # Get most frequent numbers
        most_common = [num for num, _ in frequency.most_common(num_picks)]
        
        return most_common if len(most_common) == num_picks else self._random_picks(num_picks)
    
    def hot_cold_strategy(self, historical_data, num_picks=4):
        """
        Mix of hot (frequent) and cold (infrequent) numbers
        """
        if not historical_data or len(historical_data) < 50:
            return self._random_picks(num_picks)
        
        # Analyze frequency
        frequency = Counter()
        for draw in historical_data[-50:]:
            frequency.update(draw)
        
        # All possible numbers
        all_numbers = set(range(1, 81))
        drawn_numbers = set(frequency.keys())
        
        # Hot numbers (most frequent)
        hot_count = num_picks // 2
        hot_numbers = [num for num, _ in frequency.most_common(hot_count)]
        
        # Cold numbers (least frequent or not drawn)
        cold_numbers = list(all_numbers - drawn_numbers)
        if not cold_numbers:
            cold_numbers = [num for num, _ in frequency.most_common()[-10:]]
        
        cold_count = num_picks - hot_count
        cold_picks = random.sample(cold_numbers, min(cold_count, len(cold_numbers)))
        
        predictions = hot_numbers[:hot_count] + cold_picks
        return sorted(predictions[:num_picks])
    
    def pattern_detection(self, historical_data, num_picks=4):
        """
        Detect patterns in number sequences
        """
        if len(historical_data) < 10:
            return self._random_picks(num_picks)
        
        # Look for numbers that often appear together
        pair_frequency = Counter()
        
        for draw in historical_data[-30:]:
            # Count all pairs
            for i in range(len(draw)):
                for j in range(i + 1, len(draw)):
                    pair = tuple(sorted([draw[i], draw[j]]))
                    pair_frequency[pair] += 1
        
        # Extract numbers from most common pairs
        predicted_numbers = set()
        for pair, _ in pair_frequency.most_common(num_picks * 2):
            predicted_numbers.update(pair)
            if len(predicted_numbers) >= num_picks:
                break
        
        result = sorted(list(predicted_numbers))[:num_picks]
        return result if len(result) == num_picks else self._random_picks(num_picks)
    
    def statistical_approach(self, historical_data, num_picks=4):
        """
        Statistical analysis using mean and variance
        """
        if not historical_data:
            return self._random_picks(num_picks)
        
        # Calculate statistics for each number
        number_appearances = {i: [] for i in range(1, 81)}
        
        for draw_idx, draw in enumerate(historical_data[-100:]):
            for num in draw:
                if 1 <= num <= 80:
                    number_appearances[num].append(draw_idx)
        
        # Calculate expected value based on gap since last appearance
        current_draw = len(historical_data)
        scores = {}
        
        for num in range(1, 81):
            appearances = number_appearances[num]
            if not appearances:
                # Number hasn't appeared - give it moderate score
                scores[num] = 50
            else:
                # Calculate gap since last appearance
                gap = current_draw - appearances[-1]
                # Calculate average gap
                if len(appearances) > 1:
                    gaps = [appearances[i] - appearances[i-1] for i in range(1, len(appearances))]
                    avg_gap = np.mean(gaps)
                    # Score based on if gap exceeds average
                    scores[num] = gap / (avg_gap + 1)
                else:
                    scores[num] = gap
        
        # Get numbers with highest scores
        sorted_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in sorted_numbers[:num_picks]]
    
    def markov_chain_analysis(self, historical_data, num_picks=4):
        """
        Simple Markov chain analysis for next-state prediction
        """
        if len(historical_data) < 5:
            return self._random_picks(num_picks)
        
        # Build transition matrix (simplified)
        transitions = Counter()
        
        for i in range(len(historical_data) - 1):
            current_draw = tuple(sorted(historical_data[i]))
            next_draw = historical_data[i + 1]
            
            for num in next_draw:
                transitions[(current_draw[:3], num)] += 1  # Use first 3 nums as state
        
        # Get last draw as current state
        current_state = tuple(sorted(historical_data[-1][:3]))
        
        # Find most likely next numbers
        likely_numbers = Counter()
        for (state, num), count in transitions.items():
            if state == current_state:
                likely_numbers[num] += count
        
        if likely_numbers:
            predictions = [num for num, _ in likely_numbers.most_common(num_picks)]
            if len(predictions) == num_picks:
                return sorted(predictions)
        
        # Fallback to frequency
        return self.frequency_analysis(historical_data, num_picks)
    
    def _calculate_confidence(self, historical_data, predictions):
        """
        Calculate confidence score for predictions (0-100)
        """
        if not historical_data or not predictions:
            return 20.0
        
        # Check how often these numbers appeared in recent history
        recent_frequency = Counter()
        for draw in historical_data[-20:]:
            recent_frequency.update(draw)
        
        # Calculate average frequency of predicted numbers
        total_freq = sum(recent_frequency[num] for num in predictions)
        avg_freq = total_freq / len(predictions)
        
        # Normalize to 0-100 scale (assume max frequency is 20)
        confidence = min(100, (avg_freq / 20) * 100)
        
        # Add randomness factor (Keno is random, so cap confidence)
        confidence = min(confidence, 65)  # Never exceed 65% confidence
        
        return round(confidence, 1)
    
    def _random_picks(self, num_picks):
        """Generate random picks as fallback"""
        return sorted(random.sample(range(1, 81), num_picks))
    
    def analyze_historical_accuracy(self, historical_data, lookback=50, num_picks=4):
        """
        Analyze historical accuracy of predictions
        """
        if len(historical_data) < lookback + 10:
            return None
        
        results = {
            'total_tests': 0,
            'matches': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
            'strategies': {}
        }
        
        # Test each strategy
        for strategy_name in self.strategies.keys():
            strategy_results = {'matches': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}}
            
            for i in range(lookback, len(historical_data) - 1):
                # Make prediction based on history up to this point
                training_data = historical_data[:i]
                actual_draw = historical_data[i]
                
                try:
                    predicted = self.strategies[strategy_name](training_data, num_picks)
                    matches = len(set(predicted) & set(actual_draw))
                    strategy_results['matches'][matches] += 1
                    results['total_tests'] += 1
                except:
                    continue
            
            results['strategies'][strategy_name] = strategy_results
        
        return results


def load_historical_data_from_file(filename):
    """
    Load historical data from a Keno data file
    """
    historical_data = []
    
    try:
        with open(filename, 'r') as f:
            regex = re.compile(r'(\d{2})')
            for line in f:
                numbers = regex.findall(line)
                if numbers:
                    draw = [int(num) for num in numbers]
                    historical_data.append(draw)
    except Exception as e:
        print(f"Error loading data: {e}")
    
    return historical_data
