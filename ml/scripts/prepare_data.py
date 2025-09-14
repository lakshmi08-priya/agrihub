from pathlib import Path
import splitfolders  # pip install split-folders
from collections import Counter
import os

# Paths
RAW_DIR = Path("ml/data/raw/PlantVillage")
OUT_DIR = Path("ml/data/processed")

def count_images(directory):
    """Count images per class in a given directory."""
    counts = {}
    for root, dirs, files in os.walk(directory):
        if files:
            class_name = Path(root).name
            counts[class_name] = len(files)
    return counts

def print_distribution():
    """Print dataset distribution for train/val/test."""
    for split in ["train", "val", "test"]:
        split_dir = OUT_DIR / split
        counts = count_images(split_dir)
        print(f"\n📊 {split.upper()} distribution:")
        for cls, n in sorted(counts.items()):
            print(f"  {cls}: {n}")

def main():
    # Split only if not already done
    if not OUT_DIR.exists() or not any(OUT_DIR.iterdir()):
        print("🔄 Splitting dataset into train/val/test...")
        splitfolders.ratio(RAW_DIR, output=OUT_DIR, seed=42, ratio=(0.8, 0.1, 0.1))
    else:
        print("✅ Processed dataset already exists, skipping split.")
    
    # Show distribution
    print_distribution()

if __name__ == "__main__":
    main()
