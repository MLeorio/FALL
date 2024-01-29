from logging import info
import uvicorn
from main import app
from config import Settings

setting = Settings()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=setting.PORT, log_level="info")
