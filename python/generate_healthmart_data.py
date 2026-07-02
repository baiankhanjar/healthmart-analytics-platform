from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw_sources"

RAW_DIR.mkdir(parents=True, exist_ok=True)

print("HealthMart data generation started...")
print(f"Raw files will be saved to: {RAW_DIR}")