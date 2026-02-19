# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install numpy flask flask-cors
```

Optional (for full DQN functionality):
```bash
pip install tensorflow
```

### Step 2: Run the Application

```bash
python api.py
```

### Step 3: Open in Browser

Navigate to: **http://localhost:5000**

---

## 🎮 Using the Interface

### Make a Prediction

1. Select a strategy from the dropdown (try "Ensemble" first)
2. Choose number of picks (4 is recommended)
3. Click **"Generate Predictions"**
4. View your predicted numbers!

### View Statistics

1. Click **"Load Statistics"**
2. See hot and cold numbers
3. Understand historical patterns

---

## 📱 GitHub Pages Version

Don't want to run Python? Use the static version:

**Just open `index.html` in your browser!**

Or visit the GitHub Pages deployment (after merging to main):
`https://[your-username].github.io/Keno-Analyzer/`

---

## 🧪 Run Tests

```bash
python test_system.py
```

This verifies everything is working correctly.

---

## 🎓 Understanding Results

### Confidence Scores
- **20-30%**: Random baseline
- **30-45%**: Pattern detected
- **45-65%**: Strong patterns

**Note**: Scores are intentionally capped because Keno is random!

### Prediction Strategies

- **Ensemble**: Combines all methods (recommended)
- **Frequency**: Most common numbers
- **Hot & Cold**: Mix of frequent and rare numbers
- **Pattern**: Numbers that appear together
- **Statistical**: Gap analysis
- **Markov**: State transitions
- **DQN**: Machine learning (requires TensorFlow)

---

## ⚠️ Important Reminder

This tool is **educational only**:
- ✅ Learn about statistics and ML
- ✅ Understand probability
- ✅ See algorithms in action
- ❌ Do NOT expect to win at gambling
- ❌ Do NOT rely on predictions
- ❌ Keno is random and cannot be "cracked"

---

## 🆘 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "TensorFlow not available"
This is normal! The system works without it.
To enable DQN: `pip install tensorflow`

### "No historical data"
The system needs data files in `kenoData/` directory.
The repository includes sample data.

### Port 5000 in use
Change the port in `api.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 📖 More Information

- **Full Documentation**: See `README.md`
- **Usage Guide**: See `USAGE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`

---

## 🎯 Next Steps

1. ✅ Run the application
2. ✅ Try different strategies
3. ✅ View the statistics
4. ✅ Run the test suite
5. ✅ Read the documentation
6. ✅ Understand the limitations
7. ✅ Use responsibly!

---

**Remember**: This is a learning tool. Gamble responsibly and never bet more than you can afford to lose!
