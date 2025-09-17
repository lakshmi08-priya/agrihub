from fastapi import APIRouter
import json, os

router = APIRouter()

@router.get("/")
def soil_index():
    f = "ml/output/soil_data.json"
    if os.path.exists(f):
        with open(f) as fh:
            return json.load(fh)
    return {"message": "soil data not available yet"}
