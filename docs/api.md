# 🌱 Agriculture Backend — API Documentation

Base URLs
- Local: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Authentication
- Not implemented in skeleton. Later: JWT or Firebase Auth.

---

## POST /predict/disease
**Description:** Predict crop disease from an uploaded image.

**Request:** `multipart/form-data`  
- `file` — image file (jpg/png)

**Response (200):**
```json
{
  "disease": "Leaf Blight",
  "confidence": 0.87,
  "filename": "image.jpg"
}
