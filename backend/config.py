import os
from pathlib import Path

# Mode: "LOCAL" (MVP) or "S3" (future)
STORAGE_MODE = os.getenv("STORAGE_MODE", "LOCAL")

if STORAGE_MODE == "LOCAL":
    DATA_DIR = Path("../ml/data/raw")
else:
    DATA_DIR = "s3://your-bucket-name/raw"

print(f"Using storage mode: {STORAGE_MODE}")
print(f"Data location: {DATA_DIR}")
