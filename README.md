# Keno Analyzer Pro - Enhanced AI-Powered Analysis System

## ⚠️ IMPORTANT DISCLAIMER

**This tool is for educational and entertainment purposes ONLY.**

- Keno is a game of chance with outcomes determined by certified random number generators
- No prediction system can reliably predict or "crack" random number generation
- The house edge in Keno makes it mathematically impossible to guarantee winning
- This system demonstrates statistical analysis and machine learning techniques for educational purposes
- **We do not claim 95% or any guaranteed winning rate**
- Use responsibly and never gamble more than you can afford to lose

## 🎯 Overview

Keno Analyzer Pro is an advanced statistical analysis and machine learning demonstration project that explores various approaches to analyzing Keno game patterns. It combines multiple mathematical algorithms, deep learning techniques, and a modern web interface.

## ✨ Features

### 🧠 Multiple Prediction Strategies

1. **Ensemble Method** - Combines all strategies using weighted voting
2. **Frequency Analysis** - Analyzes historical number frequencies
3. **Hot & Cold Strategy** - Mixes frequent and infrequent numbers
4. **Pattern Detection** - Identifies number co-occurrence patterns
5. **Statistical Approach** - Uses mean, variance, and gap analysis
6. **Markov Chain Analysis** - Models state transitions
7. **Deep Q-Network (DQN)** - Reinforcement learning approach

### 🖥️ Modern Web Interface

- Clean, responsive design
- Real-time predictions
- Interactive visualizations
- Historical statistics display
- Mobile-friendly

### 🔧 Technical Components

- **Backend**: Python Flask REST API
- **Frontend**: Pure HTML/CSS/JavaScript (no framework dependencies)
- **ML**: TensorFlow/Keras for DQN implementation
- **Analysis**: NumPy, Pandas, scikit-learn

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Virtual environment

### Setup

1. Clone the repository:
```bash
git clone https://github.com/genXstark/Keno-Analyzer.git
cd Keno-Analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python api.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 🚀 GitHub Pages Deployment

The project includes a static client-side version that can be deployed to GitHub Pages:

1. The `index.html` in the root directory is the GitHub Pages version
2. GitHub Actions workflow automatically deploys on push to main/master
3. Access the live demo at: `https://[username].github.io/Keno-Analyzer/`

## 📊 Usage

### Making Predictions

1. Select a prediction strategy from the dropdown
2. Choose the number of picks (1-10)
3. Click "Generate Predictions"
4. View the predicted numbers and confidence score

### Analyzing Historical Data

1. Click "Load Statistics" to see historical patterns
2. View hot and cold numbers
3. Examine frequency distributions

### Training the DQN Model

1. Click "Train DQN Model" (requires TensorFlow)
2. Wait for training to complete
3. Model is automatically saved for future predictions

## 🏗️ Architecture

### Backend (api.py)

- Flask REST API server
- Endpoints for predictions, statistics, and training
- Manages data loading and processing

### Prediction Engine (prediction_engine.py)

- Implements multiple statistical strategies
- Ensemble method for combining predictions
- Historical accuracy testing

### DQN Predictor (dqn_predictor.py)

- Deep Q-Network implementation
- Experience replay and epsilon-greedy exploration
- Model training on historical data

### Web Interface (static/index.html)

- Single-page application
- Responsive design
- Real-time API communication

## 📈 Algorithms Explained

### Frequency Analysis
Tracks how often each number appears in historical draws and favors frequently drawn numbers.

### Hot & Cold Strategy
Combines "hot" numbers (frequently drawn) with "cold" numbers (rarely drawn) for a balanced approach.

### Pattern Detection
Identifies pairs or groups of numbers that frequently appear together.

### Statistical Approach
Uses gap analysis to predict numbers "due" based on their historical draw intervals.

### Markov Chain
Models the probability of future states based on current state transitions.

### Deep Q-Network (DQN)
Reinforcement learning algorithm that learns patterns through trial and reward:
- State: Historical frequency distribution
- Action: Selecting a number
- Reward: Based on whether the number appears in subsequent draws
- Neural network with 3 hidden layers
- Experience replay for stable learning

## 🔬 Mathematical Reality

Understanding the mathematics:

- Each Keno draw is independent
- The probability of any number being drawn is equal (in a fair game)
- Past results do not influence future outcomes
- The house edge ranges from 20-40% depending on the game
- No strategy can overcome the mathematical house advantage

This tool demonstrates various analytical approaches but cannot overcome these fundamental mathematical constraints.

## 📁 Project Structure

```
Keno-Analyzer/
├── api.py                      # Flask REST API
├── prediction_engine.py        # Statistical prediction strategies
├── dqn_predictor.py           # Deep Q-Network implementation
├── analyzeKenoData.py         # Original analysis functions
├── getKenoData.py             # Data collection utilities
├── betCalculator.py           # Payout calculations
├── Tests.py                   # Testing strategies
├── main.py                    # Original CLI interface
├── requirements.txt           # Python dependencies
├── index.html                 # GitHub Pages static version
├── static/
│   └── index.html            # Full-featured UI (requires backend)
├── .github/
│   └── workflows/
│       └── pages.yml         # GitHub Actions deployment
├── kenoData/                 # Historical data storage
└── models/                   # Trained model storage
```

## 🧪 Testing

The system includes multiple test strategies in `Tests.py`:

```python
python main.py
```

Modify the `trigger` variable in `main.py` to run different tests.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes. Please check the repository for license information.

## ⚖️ Legal and Ethical Considerations

- This tool is NOT intended for actual gambling
- Do not use this to exploit gambling platforms
- Violating terms of service of gambling sites may have legal consequences
- Always gamble responsibly and within your means
- Seek help if gambling becomes a problem

## 🙏 Acknowledgments

- Original Keno Analyzer project by genXstark
- TensorFlow team for the ML framework
- Flask team for the web framework
- The open-source community

## 📞 Support

For issues, questions, or discussions:
- Open an issue on GitHub
- Check existing documentation
- Review the code comments

---

**Remember**: This is an educational tool. No system can reliably predict random outcomes. Use responsibly!
