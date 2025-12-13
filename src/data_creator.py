import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# Path to save CSV
data_dir = Path('/Users/ocarmeli/dev/First_project/data')
data_dir.mkdir(parents=True, exist_ok=True)  # ensure the folder exists

file_path = data_dir / 'ads_events_200_edgecases.csv'

rows = []

for i in range(1, 201):
    # Generate user_id (duplicates allowed)
    user_id = random.randint(1, 180)
    
    # Generate ad_id (including fake ad for edge case)
    ad_id = random.choice([1, 2, 3, 4, 5, 999])
    
    # Base impression timestamp
    base_time = datetime(2025, 12, 1, 8, 0, 0)
    impression_offset = random.randint(-60, 500)  # negative offset to simulate wrong data
    impression_ts = base_time + timedelta(minutes=impression_offset)
    
    # Randomly set missing impression
    if random.random() < 0.05:
        impression_ts = None
    
    # Generate click timestamp
    if random.random() < 0.35:
        click_offset = random.randint(-10, 60)  # can be negative → click before impression
        click_ts = None if not impression_ts else impression_ts + timedelta(minutes=click_offset)
        # Randomly set click as missing
        if random.random() < 0.05:
            click_ts = None
    else:
        click_ts = None
    
    # Generate purchase value
    if click_ts:
        purchase_value = random.choice([0, 20, 50, 100, 200, -10, None])  # include negative and null
    else:
        purchase_value = None
    
    rows.append([user_id, ad_id, impression_ts, click_ts, purchase_value])

# Create DataFrame
df = pd.DataFrame(rows, columns=['user_id', 'ad_id', 'impression_ts', 'click_ts', 'purchase_value'])

# Shuffle rows to simulate real-world data
df = df.sample(frac=1).reset_index(drop=True)

# Save CSV to specified path
df.to_csv(file_path, index=False)

print(f"CSV generated: {file_path}")
print(df.head(10))
