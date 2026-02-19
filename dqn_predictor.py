"""
Deep Q-Network (DQN) Predictor for Keno Analysis
This module implements a DQN-based approach for pattern recognition in Keno draws.
Note: This is for educational purposes - Keno outcomes are random and cannot be reliably predicted.
"""
import numpy as np
import random
from collections import deque
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available. DQN features will be limited.")


class DQNKenoPredictor:
    """DQN-based predictor for Keno number patterns"""
    
    def __init__(self, state_size=80, action_size=80, learning_rate=0.001):
        self.state_size = state_size  # 80 possible Keno numbers
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = learning_rate
        self.model = None
        
        if TENSORFLOW_AVAILABLE:
            self.model = self._build_model()
    
    def _build_model(self):
        """Build the neural network model"""
        if not TENSORFLOW_AVAILABLE:
            return None
            
        model = keras.Sequential([
            layers.Dense(128, input_dim=self.state_size, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Choose action based on epsilon-greedy policy"""
        if not TENSORFLOW_AVAILABLE or self.model is None:
            return self._fallback_predict(state)
            
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])
    
    def _fallback_predict(self, state):
        """Fallback prediction using frequency analysis"""
        # Return index of most frequent number
        return np.argmax(state[0])
    
    def replay(self, batch_size=32):
        """Train on batch of experiences"""
        if not TENSORFLOW_AVAILABLE or self.model is None:
            return
            
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def load(self, name):
        """Load model weights"""
        if TENSORFLOW_AVAILABLE and self.model is not None:
            try:
                self.model.load_weights(name)
            except:
                print(f"Could not load weights from {name}")
    
    def save(self, name):
        """Save model weights"""
        if TENSORFLOW_AVAILABLE and self.model is not None:
            self.model.save_weights(name)
    
    def predict_numbers(self, historical_data, num_picks=4):
        """
        Predict Keno numbers based on historical data
        
        Args:
            historical_data: List of previous Keno draws
            num_picks: Number of numbers to predict
            
        Returns:
            List of predicted numbers (1-80)
        """
        # Create state from historical data
        state = self._create_state(historical_data)
        
        if not TENSORFLOW_AVAILABLE or self.model is None:
            # Fallback to frequency-based prediction
            return self._frequency_based_prediction(state, num_picks)
        
        # Reshape for model input
        state = np.reshape(state, [1, self.state_size])
        
        # Get predictions
        predictions = []
        for _ in range(num_picks):
            action = self.act(state)
            predictions.append(action + 1)  # Convert to 1-80 range
        
        return sorted(predictions)
    
    def _create_state(self, historical_data):
        """Create state vector from historical draws"""
        state = np.zeros(80)
        
        # Count frequency of each number in recent history
        for draw in historical_data[-50:]:  # Use last 50 draws
            for num in draw:
                if 1 <= num <= 80:
                    state[num - 1] += 1
        
        # Normalize
        if np.sum(state) > 0:
            state = state / np.sum(state)
        
        return state
    
    def _frequency_based_prediction(self, state, num_picks):
        """Fallback prediction based on frequency analysis"""
        # Get indices sorted by frequency
        sorted_indices = np.argsort(state)[::-1]
        
        # Mix hot and cold numbers
        hot_numbers = sorted_indices[:10]  # Top 10 frequent
        cold_numbers = sorted_indices[-20:]  # Bottom 20 least frequent
        
        # Select mix of hot and cold
        predictions = []
        hot_count = num_picks // 2
        cold_count = num_picks - hot_count
        
        predictions.extend(np.random.choice(hot_numbers, hot_count, replace=False))
        predictions.extend(np.random.choice(cold_numbers, cold_count, replace=False))
        
        # Convert to 1-80 range and return sorted
        return sorted([int(x + 1) for x in predictions])
    
    def train_on_history(self, historical_data, episodes=100):
        """
        Train the DQN model on historical Keno data
        
        Args:
            historical_data: List of historical Keno draws
            episodes: Number of training episodes
        """
        if not TENSORFLOW_AVAILABLE or self.model is None:
            print("TensorFlow not available. Cannot train DQN model.")
            return
        
        print(f"Training DQN on {len(historical_data)} historical draws...")
        
        for episode in range(episodes):
            # Sample training data
            if len(historical_data) < 60:
                continue
            
            start_idx = random.randint(0, len(historical_data) - 60)
            training_window = historical_data[start_idx:start_idx + 60]
            
            # Create state from first 50 draws
            state = self._create_state(training_window[:50])
            state = np.reshape(state, [1, self.state_size])
            
            # Use next 10 draws as targets
            for target_draw in training_window[50:]:
                # Select action
                action = self.act(state)
                
                # Calculate reward based on if predicted number appeared
                reward = 1.0 if (action + 1) in target_draw else -0.1
                
                # Get next state
                next_state = self._create_state(training_window[:51])
                next_state = np.reshape(next_state, [1, self.state_size])
                
                # Remember experience
                self.remember(state, action, reward, next_state, False)
                
                # Update state
                state = next_state
            
            # Train on batch
            self.replay(batch_size=32)
            
            if episode % 10 == 0:
                print(f"Episode {episode}/{episodes}, Epsilon: {self.epsilon:.3f}")
        
        print("Training complete!")


def predict_with_dqn(historical_data, num_picks=4):
    """
    Convenience function to make predictions using DQN
    
    Args:
        historical_data: List of previous Keno draws
        num_picks: Number of numbers to predict
        
    Returns:
        List of predicted numbers
    """
    predictor = DQNKenoPredictor()
    return predictor.predict_numbers(historical_data, num_picks)
