"""
Quick test of app_lay_0x1.py without running Streamlit
"""
import pandas as pd
from strategy_v4 import Lay0x1StrategyV4

print("Loading consolidated data...")
df = pd.read_csv("data_total/dados_consolidado_v2.csv", sep=";")
print(f"✓ Loaded: {df.shape[0]} games, {df.shape[1]} columns")

print("\nLoading strategy V4...")
strategy = Lay0x1StrategyV4()
print("✓ Strategy loaded")

print("\nTesting evaluation...")
result = strategy.evaluate_score("Osasuna", "Real Madrid", 1.58, 8.6)
print(f"✓ Score: {result['total_score']}/110 - {result['recommendation']}")

print("\nTesting historical stats...")
stats = strategy.get_historical_stats()
print(f"✓ Historical win rate: {stats['lay_0x1_winrate']:.1f}%")

print("\n✅ All tests passed!")
