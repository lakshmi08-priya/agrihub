from config import DATA_DIR
import pandas as pd

# Make sure the folder exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Create a small test dataset
df = pd.DataFrame({
    "crop": ["wheat", "rice", "maize"],
    "yield": [3000, 4500, 5200],
    "region": ["North", "East", "West"]
})

# Save dataset to CSV inside ml/data/raw/
file_path = DATA_DIR / "sample_dataset.csv"
df.to_csv(file_path, index=False)

print(f"✅ Dataset saved at: {file_path}")

# Load it back
df_loaded = pd.read_csv(file_path)
print("📊 Loaded dataset:")
print(df_loaded)
