import uvicorn
from app.main import app  # Asegúrate de que esto coincida con tu estructura de archivos

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
