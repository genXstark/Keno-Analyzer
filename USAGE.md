# Usage Guide for Keno Analyzer Pro

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: TensorFlow is optional. The system will work with fallback methods if TensorFlow is not installed.

### 2. Run the System

#### Option A: Full System with API Backend

```bash
python api.py
```

Then open your browser to: `http://localhost:5000`

#### Option B: Static Client-Side Version

Simply open `index.html` in your browser. This version runs entirely in the browser without requiring Python.

### 3. GitHub Pages Deployment

The static version is automatically deployed to GitHub Pages when you push to the main/master branch.

Access it at: `https://[your-username].github.io/Keno-Analyzer/`

## Features Overview

### 📊 Prediction Strategies

1. **Ensemble (Recommended)**
   - Combines all strategies using weighted voting
   - Most robust approach
   - Typical confidence: 35-45%

2. **Frequency Analysis**
   - Analyzes which numbers appear most often
   - Based on statistical frequency
   - Good for understanding patterns

3. **Hot & Cold Mix**
   - Combines frequently drawn (hot) and rarely drawn (cold) numbers
   - Balanced approach
   - Popular in lottery systems

4. **Pattern Detection**
   - Identifies numbers that often appear together
   - Uses co-occurrence analysis
   - Interesting for pattern enthusiasts

5. **Statistical Approach**
   - Uses gap analysis and expected value
   - Mathematical approach
   - Good for understanding probability

6. **Markov Chain**
   - Models state transitions
   - Advanced probability theory
   - For those interested in stochastic processes

7. **Deep Q-Network (DQN)**
   - Reinforcement learning approach
   - Requires TensorFlow
   - Demonstrates AI in action

### 🎯 Using the Web Interface

1. **Select Strategy**: Choose from dropdown menu
2. **Set Number of Picks**: Enter 1-10 (typical is 4)
3. **Click Generate**: System analyzes data and shows predictions
4. **View Results**:
   - Predicted numbers displayed as balls
   - Confidence score shown as percentage
   - Strategy information included

### 📈 Viewing Statistics

- Click "Load Statistics" to see:
  - Total number of draws analyzed
  - Most common numbers historically
  - Hot numbers (frequent in recent draws)
  - Cold numbers (not appearing recently)

### 🧪 Testing Accuracy

- Click "Test Historical Accuracy" to:
  - Run backtest on historical data
  - See how strategies performed in the past
  - Understand statistical validity

### 🤖 Training DQN Model

If TensorFlow is installed:
1. Click "Train DQN Model"
2. Wait for training to complete (may take several minutes)
3. Model is saved for future predictions

## API Endpoints

### POST /api/predict
Make predictions based on historical data.

**Request:**
```json
{
    "strategy": "ensemble",
    "num_picks": 4,
    "data_source": "latest"
}
```

**Response:**
```json
{
    "numbers": [12, 34, 56, 78],
    "confidence": 42.5,
    "strategy": "ensemble",
    "timestamp": "2024-01-15T10:30:00",
    "data_points": 300
}
```

### POST /api/analyze
Get statistical analysis of historical data.

**Request:**
```json
{
    "data_source": "latest"
}
```

**Response:**
```json
{
    "total_draws": 300,
    "most_common": [...],
    "hot_numbers": [...],
    "cold_numbers": [...]
}
```

### GET /api/historical-accuracy
Test prediction accuracy on historical data.

**Response:**
```json
{
    "total_tests": 50,
    "matches": {...},
    "strategies": {...}
}
```

### POST /api/train-dqn
Train the DQN model (requires TensorFlow).

**Request:**
```json
{
    "episodes": 100
}
```

## Running Tests

```bash
python test_system.py
```

This runs comprehensive tests on:
- Prediction Engine
- DQN Predictor
- API Module
- Original Codebase Compatibility

## Understanding the Results

### Confidence Scores

- **20-30%**: Low confidence (random baseline)
- **30-45%**: Moderate confidence (pattern detected)
- **45-65%**: Higher confidence (strong patterns)
- **Never >65%**: Keno is inherently random

### What the Numbers Mean

The predictions are based on:
- Historical frequency patterns
- Statistical analysis
- Pattern recognition
- Machine learning (if TensorFlow available)

**Important**: These are educational demonstrations. No system can predict random outcomes reliably.

## Troubleshooting

### "TensorFlow not available"
- This is normal if TensorFlow is not installed
- System will use fallback methods
- To enable DQN: `pip install tensorflow`

### "No historical data available"
- Check that kenoData directory has .txt files
- Run data collection scripts from original project
- System needs at least one data file

### Server won't start
- Check port 5000 is not in use
- Install Flask: `pip install flask flask-cors`
- Check Python version (requires 3.8+)

## Best Practices

1. **Use Ensemble Strategy**: It combines multiple approaches
2. **Analyze Statistics First**: Understand the data before predicting
3. **Test on Historical Data**: See how strategies perform
4. **Never Rely on Predictions**: This is educational only
5. **Gamble Responsibly**: If using for entertainment, set limits

## Understanding the Mathematics

### Why Can't We Predict Keno?

1. **True Random Number Generation**: Licensed platforms use certified RNGs
2. **Independent Events**: Each draw is independent
3. **Equal Probability**: Every number has equal chance (1/80)
4. **House Edge**: Built-in mathematical advantage (20-40%)

### What This System Does

- Demonstrates statistical analysis techniques
- Shows pattern recognition algorithms
- Illustrates machine learning concepts
- Provides educational value
- **Does NOT**: Guarantee wins or "crack" the game

## Educational Value

This system is excellent for learning:
- Statistical analysis
- Pattern recognition
- Machine learning (DQN)
- Web development (Flask + JavaScript)
- API design
- Probability theory

## Safety and Ethics

- ✅ Use for learning and education
- ✅ Understand probability and statistics
- ✅ Gamble responsibly if playing
- ❌ Don't believe you can "beat" random systems
- ❌ Don't use to exploit gambling platforms
- ❌ Don't gamble more than you can afford to lose

## Further Reading

- [Deep Q-Networks Paper](https://www.nature.com/articles/nature14236)
- [Markov Chains in Gambling](https://en.wikipedia.org/wiki/Markov_chain)
- [Statistical Analysis of Lottery](https://en.wikipedia.org/wiki/Lottery_mathematics)
- [Responsible Gambling](https://www.ncpgambling.org/)

## Support

For issues or questions:
1. Check this usage guide
2. Review README.md
3. Check test results with `python test_system.py`
4. Open an issue on GitHub

---

**Remember**: This is an educational tool. Keno outcomes are random and cannot be reliably predicted. Always gamble responsibly!
