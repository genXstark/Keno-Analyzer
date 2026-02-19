#!/usr/bin/env python3
"""
Test script for Keno Analyzer Pro
Tests all major components of the system
"""

import sys
import os

def test_prediction_engine():
    """Test the prediction engine"""
    print("=" * 60)
    print("Testing Prediction Engine")
    print("=" * 60)
    
    try:
        import prediction_engine
        
        # Load test data
        test_file = 'kenoData/kenoNum01-2015/kenoNum01-08-2015.txt'
        if not os.path.exists(test_file):
            print("❌ Test data file not found")
            return False
        
        historical_data = prediction_engine.load_historical_data_from_file(test_file)
        print(f"✓ Loaded {len(historical_data)} draws from test file")
        
        # Test prediction engine
        engine = prediction_engine.PredictionEngine()
        result = engine.predict(historical_data, num_picks=4, strategy='ensemble')
        print(f"✓ Ensemble Prediction: {result['numbers']}")
        print(f"  Confidence: {result['confidence']}%")
        
        # Test individual strategies
        for strategy in ['frequency', 'hot_cold', 'pattern', 'statistical']:
            res = engine.predict(historical_data, num_picks=4, strategy=strategy)
            print(f"✓ {strategy.capitalize()}: {res['numbers']}")
        
        print("✅ Prediction Engine: PASSED\n")
        return True
    
    except Exception as e:
        print(f"❌ Prediction Engine: FAILED - {e}\n")
        return False


def test_dqn_predictor():
    """Test the DQN predictor"""
    print("=" * 60)
    print("Testing DQN Predictor")
    print("=" * 60)
    
    try:
        import dqn_predictor
        import prediction_engine
        
        # Load test data
        test_file = 'kenoData/kenoNum01-2015/kenoNum01-08-2015.txt'
        historical_data = prediction_engine.load_historical_data_from_file(test_file)
        
        # Test DQN predictor
        predictor = dqn_predictor.DQNKenoPredictor()
        if predictor.model is not None:
            print("✓ TensorFlow available - Full DQN functionality")
        else:
            print("⚠ TensorFlow not available - Using fallback method")
        
        predictions = predictor.predict_numbers(historical_data, num_picks=4)
        print(f"✓ DQN Predictions: {predictions}")
        
        print("✅ DQN Predictor: PASSED\n")
        return True
    
    except Exception as e:
        print(f"❌ DQN Predictor: FAILED - {e}\n")
        return False


def test_api_module():
    """Test the API module"""
    print("=" * 60)
    print("Testing API Module")
    print("=" * 60)
    
    try:
        import api
        
        # Test data loading
        data = api.load_data('latest')
        print(f"✓ Loaded {len(data)} draws from latest data file")
        
        if data:
            # Test statistics calculation
            stats = api.calculate_statistics(data)
            print(f"✓ Statistics calculated:")
            print(f"  - Total draws: {stats['total_draws']}")
            print(f"  - Most common: {stats['most_common'][0]['number']}")
            print(f"  - Hot numbers: {len(stats['hot_numbers'])}")
        
        print("✅ API Module: PASSED\n")
        return True
    
    except Exception as e:
        print(f"❌ API Module: FAILED - {e}\n")
        return False


def test_original_code():
    """Test the original codebase still works"""
    print("=" * 60)
    print("Testing Original Codebase Compatibility")
    print("=" * 60)
    
    try:
        import analyzeKenoData
        import betCalculator
        
        # Test betCalculator
        payout = betCalculator.matchPayout(4, 3)
        print(f"✓ Bet calculator works: 4 spots, 3 matches = ${payout}")
        
        # Test analyzeKenoData
        test_file = 'kenoData/kenoNum01-2015/kenoNum01-08-2015.txt'
        if os.path.exists(test_file):
            numCount = analyzeKenoData.numFreq(test_file, 0, 100)
            print(f"✓ Number frequency analysis works")
            
            common = analyzeKenoData.mostFreq(numCount)
            print(f"✓ Most frequent numbers: {common[:3]}")
        
        print("✅ Original Codebase: PASSED\n")
        return True
    
    except Exception as e:
        print(f"❌ Original Codebase: FAILED - {e}\n")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + " " * 15 + "KENO ANALYZER PRO TEST SUITE" + " " * 15 + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    results = []
    
    # Run all tests
    results.append(("Prediction Engine", test_prediction_engine()))
    results.append(("DQN Predictor", test_dqn_predictor()))
    results.append(("API Module", test_api_module()))
    results.append(("Original Codebase", test_original_code()))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:30} {status}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
